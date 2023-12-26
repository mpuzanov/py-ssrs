import queue
import sys
import os
import time
import threading

from ssrs.excel import read_xlsx_file
from ssrs.request_api import get_ssrs_file
from ssrs.mail import send_email, get_body_text
from ssrs.config import logger


def worker_email(queue_file):
    while True:
        item = queue_file.get()
        if item.to_email and item.file_name:
            logger.info(f"отправляем файл {item.file_name} по адресу - {item.to_email}")
            full_name = os.path.join(item.to_path, item.file_name)
            subject = f'{item.file_name}'
            body_text = get_body_text(item.file_name)
            if send_email(item.to_email, body_text, subject, full_name):
                logger.info(f"отправка файла {item.file_name} по адресу {item.to_email} - успешна")
            else:
                logger.error(f"ошибка отправки файла {item.file_name} по адресу {item.to_email}")
            queue_file.task_done()


def main():
    if len(sys.argv) < 2:
        sys.exit("Файл с параметрами на задан")

    file_param = sys.argv[1]
    params = read_xlsx_file(file_param)
    if len(params) == 0:
        sys.exit("параметров для выполнения отчётов нет")

    queue_file = queue.Queue(5)  # очередь для отправки файлов по email

    thread_email = threading.Thread(target=worker_email, args=(queue_file,), name="email", daemon=True)
    thread_email.start()

    get_ssrs_file(params, queue_file)

    queue_file.join()


if __name__ == '__main__':
    start_time = time.perf_counter()
    main()
    logger.info(f"Выполнено за: {(time.perf_counter() - start_time): .3f} сек.")
