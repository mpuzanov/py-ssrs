"""

"""
from pydantic import BaseModel
from typing import Optional, List, Union


class ParamReport(BaseModel):
    """
    Структура одной записи в файле параметров
    """
    name: Optional[str]
    ssrs_folder: str
    ssrs_report_name: str
    params: Optional[str]
    to_path: Optional[str] = None
    to_email: Optional[str] = None
    blocked: Optional[Union[int, str]] = None
    format: Optional[str] = "EXCEL"
    file_name: Optional[str] = None


class ParamReports(BaseModel):
    """
    Структура для хранения файла с параметрами
    """
    params: List[ParamReport]  # список параметров
