# Получение отчетов с сайта с SQL Server Reporting Services (SSRS)

## Входные параметры для выполнения отчета в SSRS

Файл в формате Excel:

1) name - имя для идентификации запроса отчёта
2) folder	- папка с отчетом в SSRS
3) report_name - имя отчета в SSRS
4) params - строка с параметрами разделённых ';' (tip_str=137,140,142;sup_id=0)
5) to_path	- путь для сохранения готовых отчётов
6) to_email - список email для отправки файлов (разделитель - ;)
7) blocked - признак блокировки выполнения (если Пустое поле то выполняем)	
8) format - формат файла (EXCEL или CSV)

## Пример запуска

```shell
py ssrs/main.py files_params/ssrs_reports_mfc.xlsx

poetry run py ssrs/main.py files_params/ssrs_reports_mfc.xlsx
poetry run run-main files_params/ssrs_reports_mfc.xlsx
```

## Настройка виртуального окружения

```shell

# чтобы виртуальное окружение находилось в папке проекта
poetry config virtualenvs.in-project true

# в папке проекта в prod
poetry install --without dev --sync

```
