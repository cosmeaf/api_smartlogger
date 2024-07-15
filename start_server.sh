#!/bin/bash

# ###########################################
# vi /etc/systemd/system/gunicorn.service
# vi /etc/systemd/system/celery_worker.service
# vi /etc/systemd/system/celery_beat.service
# vi /etc/systemd/system/smartlogger.service
# sqlite3 /var/www/smartlogger/db.sqlite3 "DELETE FROM api_equipament; VACUUM;"
# find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
# find . -path "*/migrations/*.pyc"  -delete
# Obtém o caminho do diretório do script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Define o caminho para o arquivo de controle
CONTROL_FILE="/tmp/django_celery_control"
VENV_PATH="$SCRIPT_DIR/venv"
LOG_FILE="$SCRIPT_DIR/logs/django.log"

# Obtém o hostname de forma dinâmica
HOSTNAME=$(hostname)

# Cores para mensagens
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'  # Sem cor

# Função para iniciar o Celery e o servidor Django
start() {
    # Ativa o ambiente virtual
    source "$VENV_PATH/bin/activate"

    # Instala as dependências do requirements.txt
    pip install --upgrade django > /dev/null 2>&1 &
    pip install -r "$SCRIPT_DIR/requirements.txt" > /dev/null 2>&1 &

    # Limpa e coleta os arquivos estáticos
    python manage.py collectstatic --clear --noinput > /dev/null 2>&1 &
    python manage.py collectstatic --noinput > /dev/null 2>&1 &

    # Inicia o worker do Celery em segundo plano com hostname dinâmico
    celery -A app worker --loglevel=info --hostname=${HOSTNAME} --concurrency=4 > /dev/null 2>&1 &
    CELERY_WORKER_PID=$!
    echo $CELERY_WORKER_PID > "$CONTROL_FILE"

    # Inicia o Celery Beat em segundo plano
    celery -A app beat --loglevel=info >> "$LOG_FILE" 2>&1 &
    CELERY_BEAT_PID=$!
    echo $CELERY_BEAT_PID >> "$CONTROL_FILE"

    # Inicia o servidor Django e redireciona o log para smartlogger.log
    python manage.py runserver 0.0.0.0:7070 --insecure >> "$LOG_FILE" 2>&1 &
    DJANGO_PID=$!
    echo $DJANGO_PID >> "$CONTROL_FILE"

    # Executa a tarefa de monitoramento de logs
    python manage.py shell -c "from api.monitor.converter import process_log_data; process_log_data.delay()" >> "$LOG_FILE" 2>&1

    echo -e "${GREEN}Serviços iniciados com sucesso.${NC}"
}

# Função para parar o Celery e o servidor Django
stop() {
    if [ -f "$CONTROL_FILE" ]; then
        PIDS=$(cat "$CONTROL_FILE")
        for PID in $PIDS; do
            if [[ -n "$PID" ]] && [[ "$PID" =~ ^[0-9]+$ ]]; then
                kill "$PID" 2>/dev/null
                if [ $? -eq 0 ]; then
                    echo -e "${GREEN}Processo $PID parado com sucesso.${NC}"
                else
                    echo -e "${RED}Falha ao parar processo $PID.${NC}"
                fi
            fi
        done
        rm "$CONTROL_FILE"

        # Adiciona um comando pkill para garantir que todos os processos Celery sejam interrompidos
        pkill -f 'celery worker'
        pkill -f 'celery beat'
        pkill -f 'python manage.py runserver'

        PIDS=$(ps -ef | grep celery | grep -v grep | awk '{print $2}')
        if [ -n "$PIDS" ]; then
            echo "Matando os seguintes PIDs do Celery: $PIDS"
            echo $PIDS | xargs kill -9
        else
            echo "Nenhum processo Celery encontrado."
        fi

        # Novo comando para interromper o processo Django
        DJANGO_PIDS=$(ps -ef | grep django | grep -v grep | awk '{print $2}')
        if [ -n "$DJANGO_PIDS" ]; then
            echo "Matando PIDs do Django: $DJANGO_PIDS"
            echo $DJANGO_PIDS | xargs kill -9
        else
            echo "Nenhum processo Django encontrado."
        fi

        echo -e "${GREEN}Serviços parados com sucesso.${NC}"
    else
        echo -e "${RED}Arquivo de controle não encontrado. Nenhum processo para parar.${NC}"
    fi
}

# Função para reiniciar o Celery e o servidor Django
refresh() {
    stop
    sleep 2  # Espera 2 segundos para garantir que todos os processos sejam encerrados
    start
    
}

# Verifica o argumento passado para o script
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    refresh)
        refresh
        ;;
    *)
        echo "Uso: $0 {start|stop|refresh}"
        exit 1
        ;;
esac
