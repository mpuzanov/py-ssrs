import sys
import os
import time

from ssrs.excel import read_xlsx_file
from ssrs.request_api import get_ssrs_file
from ssrs.mail import send_email, get_body_text
from ssrs.config import logger


def main():
    if len(sys.argv) < 2:
        sys.exit("Файл с параметрами на задан")

    file_param = sys.argv[1]
    params = read_xlsx_file(file_param)
    if len(params) == 0:
        sys.exit("параметров для выполнения отчётов нет")

    get_ssrs_file(params)
    for item in params:
        if item.to_email and item.file_name:
            logger.info(f"отправляем отчёт по почте - {item.to_email}")
            full_name = os.path.join(item.to_path, item.file_name)
            subject = f'{item.file_name}'
            body_text = get_body_text(item.file_name)
            if send_email(item.to_email, body_text, subject, full_name):
                logger.info("отправка успешна")
            else:
                logger.error("ошибка отправки отчёта")


if __name__ == '__main__':
    start_time = time.time()
    main()
    logger.info(f"Выполнено за: {(time.time() - start_time): .3f} сек.")
