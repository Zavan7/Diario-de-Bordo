from config.logging_config import setup_logging
from utils.backup import BackupGenerator
import logging

setup_logging()

def service():
    backup = BackupGenerator()
    PATH_FILE_ORGINAL = r'A:\02 - Control Desk\00 - Equipe\31. Sthefany Reis\12 - DIARIO DE BORDO\diario_bordo_volks\Diario de Bordo.xlsx'
    backup.generate_backup(PATH_FILE_ORGINAL)
    logging.info ('✅ Backup finbalizado com sucesso')
if __name__ == '__main__':
    try:
        service()

    except ValueError as e:
        print(f'Error {e}')