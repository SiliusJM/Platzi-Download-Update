@echo off
title Platzi Downloader
color 0A

echo ====================================================
echo          PLATZI DOWNLOADER - Setup ^& Run
echo ====================================================
echo.

:: Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no encontrado.
    echo         Instala Python 3.10+ desde https://python.org
    echo         Asegurate de marcar "Add Python to PATH" al instalar.
    echo.
    pause
    exit /b 1
)

:: Verificar FFmpeg
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] FFmpeg no encontrado o no esta en el PATH.
    echo         Ve las instrucciones de instalacion en el README.md
    echo         o ejecuta: winget install Gyan.FFmpeg
    echo.
    pause
    exit /b 1
)

:: Moverse a la carpeta donde esta el .bat
cd /d "%~dp0"

:: Si main.py ya existe, saltamos la clonacion
if exist "main.py" (
    echo [OK] Proyecto encontrado. Saltando clonacion...
    goto :install
)

:: Clonar repositorio
echo [INFO] Clonando repositorio de GitHub...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git no encontrado. Instala Git desde https://git-scm.com
    pause
    exit /b 1
)

git clone https://github.com/SiliusJM/Platzi-Download-Update.git
if %errorlevel% neq 0 (
    echo [ERROR] No se pudo clonar el repositorio.
    echo         Verifica tu conexion a internet.
    pause
    exit /b 1
)

cd Platzi-Download-Update

:install
:: Instalar dependencias
echo.
echo [INFO] Instalando/verificando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Fallo al instalar dependencias.
    echo         Intenta ejecutar manualmente: pip install -r requirements.txt
    pause
    exit /b 1
)

:: Ejecutar el programa
echo.
echo [INFO] Iniciando Platzi Downloader...
echo ====================================================
echo.
python main.py

echo.
echo ====================================================
echo  El programa ha terminado. Presiona cualquier tecla para salir.
pause >nul
