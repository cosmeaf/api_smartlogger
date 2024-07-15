import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

class Logger:
    _header_added = False  # Variável de classe para verificar se o cabeçalho já foi adicionado

    def __init__(self, log_name="smartlogger"):
        self.log_name = log_name
        self.logger = self._get_logger()

    def _get_logger(self):
        # Define o caminho do diretório do projeto
        project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        # Define o diretório de logs dentro do projeto
        LOG_DIR = os.path.join(project_path, 'logs')
        
        # Cria o diretório de logs se não existir
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
        
        # Define o nome do arquivo de log
        log_filename = os.path.join(LOG_DIR, f'{self.log_name}.log')

        # Configura o logger
        logger = logging.getLogger(self.log_name)
        logger.setLevel(logging.INFO)
        
        # Certifica-se de que o handler seja adicionado apenas uma vez
        if not logger.hasHandlers():
            handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=30)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        # Adiciona o cabeçalho uma vez por inicialização do servidor
        if not Logger._header_added:
            logger.info("========================================")
            logger.info("Projeto: Smart Logger")
            logger.info(f"Data de inicialização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info("Empresa: Injetec Automação Eletrônica")
            logger.info("Desenvolvedor: Lexlam Electronics of Brasil")
            logger.info("Autor: Cosme Alves")
            logger.info("Contato: cosme.alex@gmail.com")
            logger.info("========================================")
            Logger._header_added = True  # Marca o cabeçalho como adicionado
        
        return logger

    def get_logger(self):
        return self.logger
