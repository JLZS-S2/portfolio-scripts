@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: ========================================================
:: CONFIGURAÇÕES DO PROJETO
:: ========================================================
set "PROJECT_NAME=JSON TO CSV AUTOMATION"
:: ========================================================

title %PROJECT_NAME%
color 0A

echo ========================================
echo %PROJECT_NAME%
echo ========================================
echo.

echo Instalando/Atualizando dependencias...
python -m pip install -r requirements.txt --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ERRO: Falha ao instalar dependencias.
    echo 1. Verifique se Python 3.12+ esta instalado
    echo 2. Verifique sua conexao com a internet
    echo 3. Leia o arquivo LEIAME.txt
    echo.
    pause
    exit /b
)

cls
color 0A
echo ========================================
echo %PROJECT_NAME%
echo ========================================
echo.

:: Verifica se a pasta ENTRADA existe
if not exist "ENTRADA\" (
    color 0E
    echo ERRO: Pasta ENTRADA nao encontrada.
    echo Crie a pasta ENTRADA e coloque seus arquivos JSON la.
    echo.
    pause
    exit /b
)

echo Iniciando menu interativo...
echo.
python launcher.py

if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ERRO NA EXECUCAO DO LAUNCHER.
    echo Verifique os logs na pasta result\ ou leia o LEIAME.txt
) else (
    color 0A
    echo.
    echo ========================================
    echo CONCLUIDO! Verifique a pasta result\
    echo ========================================
)
echo.
pause
