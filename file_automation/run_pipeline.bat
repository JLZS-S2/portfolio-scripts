@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: ========================================================
:: CONFIGURAÇÕES DO PROJETO
:: ========================================================
set "PROJECT_NAME=FILE ORGANIZER PIPELINE"
:: ========================================================

title %PROJECT_NAME%
color 0A

echo ========================================
echo %PROJECT_NAME%
echo ========================================
echo.

echo Instalando/Atualizando dependências...
python -m pip install -r requirements.txt --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ERRO: Falha ao instalar dependências.
    echo 1. Verifique se Python 3.12+ está instalado
    echo 2. Verifique sua conexão com a internet
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

:: Verifica se há pelo menos uma pasta dentro de ENTRADA
dir /b /ad "ENTRADA\" >nul 2>&1
if %errorlevel% neq 0 (
    color 0E
    echo ERRO: Nenhuma pasta encontrada dentro de ENTRADA.
    echo Coloque sua pasta desorganizada dentro de ENTRADA e tente novamente.
    echo.
    pause
    exit /b
)

echo.
echo Você pode configurar os mapeamentos de extensões:
echo - Editando o arquivo extension.json
echo - Ou definindo manualmente pelo menu interativo
echo.

echo Iniciando menu interativo...
echo.
python launcher.py

if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ERRO NA EXECUÇÃO DO LAUNCHER.
    echo Verifique os logs na pasta result\ ou leia o LEIAME.txt
) else (
    color 0A
    echo.
    echo ========================================
    echo CONCLUÍDO! Verifique a pasta result\
    echo ========================================
)
echo.
pause
