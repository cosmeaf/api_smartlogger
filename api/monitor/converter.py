import subprocess
import re
import time
import binascii
from celery import shared_task
from django.db import transaction
from api.models import Device
from api.monitor.get_logger import Logger

logger = Logger("smartlogger")

comando = 'tail -f /opt/traccar/logs/tracker-server.log'

def calcular_soc(tensao, V_cheio=4.2, V_vazio=3.0):
    if tensao >= V_cheio: return 100
    if tensao <= V_vazio: return 0
    faixa_tensao = V_cheio - V_vazio
    if tensao > V_cheio - 0.2 * faixa_tensao: return round(75 + 25 * (tensao - (V_cheio - 0.2 * faixa_tensao)) / (0.2 * faixa_tensao), 2)
    if tensao > V_cheio - 0.5 * faixa_tensao: return round(50 + 25 * (tensao - (V_cheio - 0.5 * faixa_tensao)) / (0.3 * faixa_tensao), 2)
    if tensao > V_cheio - 0.8 * faixa_tensao: return round(25 + 25 * (tensao - (V_cheio - 0.8 * faixa_tensao)) / (0.3 * faixa_tensao), 2)
    return round(0 + 25 * (tensao - V_vazio) / (0.2 * faixa_tensao), 2)

def calcular_y(ADC):
    ADC = float(ADC)
    return round(0.1856 * ADC**6 - 4.8729 * ADC**5 + 51.867 * ADC**4 - 285.27 * ADC**3 + 853.52 * ADC**2 - 1305 * ADC + 793.79, 2)

def save_or_update_device_data(device_data):
    try:
        device_id = device_data.get("device_id")
        if not device_id:
            logger.error(f"device_id não encontrado na mensagem combinada: {device_data}")
            return

        with transaction.atomic():
            # Verifica se o dispositivo já existe
            existing_device = Device.objects.filter(device_id=device_id).first()
            if existing_device:
                # Atualiza apenas os campos permitidos
                for key, value in device_data.items():
                    setattr(existing_device, key, value)
                existing_device.save()
                logger.info(f"Dispositivo atualizado: {device_id}")
            else:
                # Cria um novo registro
                Device.objects.create(**device_data)
                logger.info(f"Novo dispositivo salvo: {device_id}")

    except Exception as e:
        logger.error(f"Erro ao salvar dados no banco: {e}")

def process_line(line):
    parts = line.split(' ')
    if len(parts) > 2:
        raw_data = parts[-1]
        if raw_data.startswith('5354'):  # Protocolo STT
            try:
                decoded_data = binascii.unhexlify(raw_data).decode('utf-8', errors='ignore')
                process_stt_data(decoded_data)
            except binascii.Error as e:
                logger.error(f"Erro na decodificação STT: {e}")
        elif raw_data.startswith('414C'):  # Protocolo ALT
            try:
                decoded_data = binascii.unhexlify(raw_data).decode('utf-8', errors='ignore')
                process_alt_data(decoded_data)
            except binascii.Error as e:
                logger.error(f"Erro na decodificação ALT: {e}")
        elif raw_data.startswith('5545'):  # Protocolo UEX
            try:
                decoded_data = binascii.unhexlify(raw_data).decode('utf-8', errors='ignore')
                process_uex_data(decoded_data)
            except binascii.Error as e:
                logger.error(f"Erro na decodificação UEX: {e}")

def process_stt_data(data):
    dados = data.split(";")
    if len(dados) >= 33:
        device_data = {
            "HDR": dados[0], "device_id": dados[1], "report_map": dados[2], "model": dados[3],
            "software_version": dados[4], "message_type": dados[5], "data": dados[6], "hora": dados[7],
            "latitude": dados[8], "longitude": dados[9], "speed_gps": dados[10], "course": dados[11],
            "satellites": dados[12], "fix_status": dados[13], "in_state": dados[14], "out_state": dados[15],
            "mode": dados[16], "report_type": dados[17], "message_number": dados[18], "reserved": dados[19],
            "assign_map": dados[20], "power_voltage": float(dados[21]), "bateria_suntech": float(dados[22]),
            "connection_rat": dados[23], "acceleration_x": round((float(dados[24]) / 256) ** 2, 2),
            "acceleration_y": round((float(dados[25]) / 256) ** 2, 2), "acceleration_z": round((float(dados[26]) / 256) ** 2, 2),
            "ADC": dados[27], "GPS_odometer": dados[28], "trip_distance": dados[29], "horimeter": dados[30],
            "trip_horimeter": dados[31], "idle_time": dados[32], "impact": round((round((float(dados[24]) / 256) ** 2, 2) +
            round((float(dados[25]) / 256) ** 2, 2) + round((float(dados[26]) / 256) ** 2, 2)) ** 0.5, 2),
            "SoC_battery_voltage": calcular_soc(float(dados[22])), "temperatura": calcular_y(dados[27])
        }
        save_or_update_device_data(device_data)

def process_alt_data(data):
    dados = data.split(";")
    if len(dados) >= 33:
        device_data = {
            "HDR": dados[0], "device_id": dados[1], "report_map": dados[2], "model": dados[3],
            "software_version": dados[4], "message_type": dados[5], "data": dados[6], "hora": dados[7],
            "latitude": dados[8], "longitude": dados[9], "speed_gps": dados[10], "course": dados[11],
            "satellites": dados[12], "fix_status": dados[13], "in_state": dados[14], "out_state": dados[15],
            "alert_id": dados[16], "alert_modifier": dados[17], "alert_data": dados[18], "reserved": dados[19],
            "assign_map": dados[20], "power_voltage": float(dados[21]), "bateria_suntech": float(dados[22]),
            "connection_rat": dados[23], "acceleration_x": round((float(dados[24]) / 256) ** 2, 2),
            "acceleration_y": round((float(dados[25]) / 256) ** 2, 2), "acceleration_z": round((float(dados[26]) / 256) ** 2, 2),
            "ADC": dados[27], "GPS_odometer": dados[28], "trip_distance": dados[29], "horimeter": dados[30],
            "trip_horimeter": dados[31], "idle_time": dados[32], "impact": round((round((float(dados[24]) / 256) ** 2, 2) +
            round((float(dados[25]) / 256) ** 2, 2) + round((float(dados[26]) / 256) ** 2, 2)) ** 0.5, 2),
            "SoC_battery_voltage": calcular_soc(float(dados[22])), "temperatura": calcular_y(dados[27])
        }
        save_or_update_device_data(device_data)

def process_uex_data(data):
    dados = data.split(";")
    if len(dados) >= 22:
        device_data = {
            "HDR": dados[0], "device_id": dados[1], "report_map": dados[2], "model": dados[3],
            "software_version": dados[4], "message_type": dados[5], "data": dados[6], "hora": dados[7],
            "latitude": dados[8], "longitude": dados[9], "speed_gps": dados[10], "course": dados[11],
            "satellites": dados[12], "fix_status": dados[13], "in_state": dados[14], "out_state": dados[15],
            "data_length": dados[16], "RFID": dados[17], "velocidade_instantanea": dados[18],
            "velocidade_pico": dados[19], "temperatura_instantanea": dados[20], "temperatura_pico": dados[21]
        }
        save_or_update_device_data(device_data)

@shared_task
def process_log_data():
    process = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        while True:
            linha = process.stdout.readline().decode('utf-8')
            if not linha:
                time.sleep(0.1)
                continue

            if 'suntech' in linha:
                parts = linha.split()
                if len(parts) <= 7:  # Verifique se há pelo menos 8 partes
                    logger.error(f"Linha incompleta: {linha.strip()}")
                    continue
                
                hex_string = parts[7].strip()
                hex_string = re.sub('[^0-9a-fA-F]', '', hex_string)
                if not hex_string:
                    logger.error(f"String hexadecimal inválida: {linha.strip()}")
                    continue
                
                if hex_string.startswith(('535454', '554558', '414c56', '414c54')):
                    try:
                        ascii_string = "".join([chr(int(hex_string[i:i+2], 16)) for i in range(0, len(hex_string), 2)])
                        dados = ascii_string.split(";")
                        device_data = {}

                        if hex_string.startswith('554558') and len(dados) >= 22:
                            device_data.update({
                                "HDR": dados[0], "device_id": dados[1], "report_map": dados[2], "model": dados[3],
                                "software_version": dados[4], "message_type": dados[5], "data": dados[6], "hora": dados[7],
                                "latitude": dados[8], "longitude": dados[9], "speed_gps": dados[10], "course": dados[11],
                                "satellites": dados[12], "fix_status": dados[13], "in_state": dados[14], "out_state": dados[15],
                                "data_length": dados[16], "RFID": dados[17], "velocidade_instantanea": dados[18],
                                "velocidade_pico": dados[19], "temperatura_instantanea": dados[20], "temperatura_pico": dados[21]
                            })
                        elif hex_string.startswith('535454') and len(dados) >= 33:
                            device_data.update({
                                "HDR": dados[0], "device_id": dados[1], "report_map": dados[2], "model": dados[3],
                                "software_version": dados[4], "message_type": dados[5], "data": dados[6], "hora": dados[7],
                                "latitude": dados[8], "longitude": dados[9], "speed_gps": dados[10], "course": dados[11],
                                "satellites": dados[12], "fix_status": dados[13], "in_state": dados[14], "out_state": dados[15],
                                "mode": dados[16], "report_type": dados[17], "message_number": dados[18], "reserved": dados[19],
                                "assign_map": dados[20], "power_voltage": float(dados[21]), "bateria_suntech": float(dados[22]),
                                "connection_rat": dados[23], "acceleration_x": round((float(dados[24]) / 256) ** 2, 2),
                                "acceleration_y": round((float(dados[25]) / 256) ** 2, 2), "acceleration_z": round((float(dados[26]) / 256) ** 2, 2),
                                "ADC": dados[27], "GPS_odometer": dados[28], "trip_distance": dados[29], "horimeter": dados[30],
                                "trip_horimeter": dados[31], "idle_time": dados[32], "impact": round((round((float(dados[24]) / 256) ** 2, 2) +
                                round((float(dados[25]) / 256) ** 2, 2) + round((float(dados[26]) / 256) ** 2, 2)) ** 0.5, 2),
                                "SoC_battery_voltage": calcular_soc(float(dados[22])), "temperatura": calcular_y(dados[27])
                            })
                        elif hex_string.startswith('414c54') and len(dados) >= 33:
                            device_data.update({
                                "HDR": dados[0], "device_id": dados[1], "report_map": dados[2], "model": dados[3],
                                "software_version": dados[4], "message_type": dados[5], "data": dados[6], "hora": dados[7],
                                "latitude": dados[8], "longitude": dados[9], "speed_gps": dados[10], "course": dados[11],
                                "satellites": dados[12], "fix_status": dados[13], "in_state": dados[14], "out_state": dados[15],
                                "alert_id": dados[16], "alert_modifier": dados[17], "alert_data": dados[18], "reserved": dados[19],
                                "assign_map": dados[20], "power_voltage": float(dados[21]), "bateria_suntech": float(dados[22]),
                                "connection_rat": dados[23], "acceleration_x": round((float(dados[24]) / 256) ** 2, 2),
                                "acceleration_y": round((float(dados[25]) / 256) ** 2, 2), "acceleration_z": round((float(dados[26]) / 256) ** 2, 2),
                                "ADC": dados[27], "GPS_odometer": dados[28], "trip_distance": dados[29], "horimeter": dados[30],
                                "trip_horimeter": dados[31], "idle_time": dados[32], "impact": round((round((float(dados[24]) / 256) ** 2, 2) +
                                round((float(dados[25]) / 256) ** 2, 2) + round((float(dados[26]) / 256) ** 2, 2)) ** 0.5, 2),
                                "SoC_battery_voltage": calcular_soc(float(dados[22])), "temperatura": calcular_y(dados[27])
                            })
                        else:
                            logger.error(f"Dados insuficientes ou inválidos na linha: {linha.strip()}. Campos recebidos: {dados}")
                            continue

                        # Verifica se o device_id está presente na mensagem
                        if "device_id" not in device_data or not device_data["device_id"]:
                            logger.error(f"device_id não encontrado na mensagem: {device_data}. Linha original: {linha.strip()}")
                            continue

                        # Salva ou atualiza os dados do dispositivo no banco de dados
                        save_or_update_device_data(device_data)
                    except ValueError as e:
                        logger.error(f"Erro de conversão de dados na linha: {linha.strip()} - Campos recebidos: {dados} - Erro: {e}")
                    except Exception as e:
                        logger.error(f"Erro ao processar a linha: {linha.strip()} - Erro: {e}")
                else:
                    logger.error("Linha incompleta: {}".format(linha.strip()))
    except Exception as e:
        process.terminate()
        logger.error(f"Processo interrompido devido a erro: {e}")
        logger.info("========================================")
        logger.info("Processo interrompido pelo sistema.")
        logger.info("========================================")