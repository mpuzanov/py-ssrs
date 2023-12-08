@echo off
cd %CD%

poetry run py ssrs/main.py files_params/ssrs_reports_spdu.xlsx
