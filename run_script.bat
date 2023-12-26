@echo off
cd %~dp0

poetry run py ssrs/main.py files_params/ssrs_reports_spdu.xlsx
