:: Отключаем все лишние фразы кроме нашего скрипта
@echo off

:: Вызываем виртуальное окружение
call %~dp0venv/scripts/activate

:: Переходим в папку со скриптом
cd %~dp0

python loader.py
pause