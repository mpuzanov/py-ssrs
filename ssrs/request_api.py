import queue
from datetime import datetime
import urllib3
import os.path
from urllib.parse import quote
from ssrs.models import ParamReport
from ssrs.config import settings, logger


def get_ssrs_file(params: list[ParamReport], queue_result: queue.Queue):
    """Делаем запрос к сайту SSRS для получения файла с отчётом"""
    global response  # noqa
    headers = urllib3.make_headers(basic_auth=f'{settings.SSRS_USER}:{settings.SSRS_PASS}')
    timeout = urllib3.util.Timeout(connect=2.0, read=None)
    http = urllib3.PoolManager(timeout=timeout)
    for item in params:
        if item.blocked:
            continue

        logger.info(f'{item.name=} {item.ssrs_report_name=} {item.params=}')
        url = settings.SSRS_BASE_URL + quote(item.ssrs_folder + "/" + item.ssrs_report_name)
        url += create_get_params(item)
        logger.debug(url)
        try:
            response = http.request("GET",
                                    url=url,
                                    headers=headers,
                                    preload_content=False,
                                    )
            if response.status != 200:
                raise Exception(f"{response.status=}")
            resp_headers = response.headers
            logger.debug(f"{resp_headers.get('Content-Disposition')=}")
        except urllib3.exceptions.MaxRetryError as e:
            logger.exception(e.args[0])
            return
        except urllib3.exceptions.HTTPError as e:
            logger.exception('Request failed:', e.args[0])
            return
        except Exception as e:
            logger.exception(f"exception: {e.args[0]}")
            raise e
        # print(response.data.decode('utf-8'))

        item.file_name = create_filename(item)
        # создание каталога для файла
        if not os.path.exists(item.to_path):
            os.makedirs(item.to_path)

        local_filename = os.path.join(item.to_path, item.file_name)
        with open(local_filename, 'wb') as f:
            for chunk in response.stream(1024):
                f.write(chunk)
        response.release_conn()

        if os.path.exists(local_filename):
            if os.path.getsize(local_filename) == 0:
                logger.debug(f"файл {local_filename} пустой!")
                os.remove(local_filename)
                item.file_name = None
            else:
                logger.info(f"отчёт получен и сохранён: {local_filename}")
                queue_result.put(item)
                logger.info(f'добавлен в очередь {item}')


def create_get_params(item: ParamReport) -> str:
    """Формирование строки с параметрами для GET запроса"""
    s = ""
    if item.params:
        params_lst = [x.strip() for x in item.params.split(";") if x.strip() != '']
        s += '&' + '&'.join(params_lst)
    if item.format:
        format_param = "EXCELOPENXML" if item.format == "EXCEL" else item.format
        s += f'&rs:Format={format_param}'
    return s


def create_filename(item: ParamReport) -> str:
    """Формирование имени файла на основе параметров"""
    match item.format:
        case "EXCEL":
            ext = ".xlsx"
        case "CSV":
            ext = ".csv"
        case _:
            ext = ".xlsx"

    return get_valid_filename(f'{item.name} ({item.ssrs_report_name}) {datetime.now():%Y-%m-%d}') + ext


def get_valid_filename(filename: str) -> str:
    """
    Оставляем в имени файла разрешённые символы
    """
    return "".join(c for c in filename if c.isalnum() or c in [" ", "-", "_", "(", ")"])
