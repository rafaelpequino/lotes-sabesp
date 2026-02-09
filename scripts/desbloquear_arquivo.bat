@echo off
REM Script para desbloquear o arquivo Mover_PDFs.exe

echo.
echo ========================================
echo    Desbloqueando Mover_PDFs.exe
echo ========================================
echo.

REM Obter o caminho do arquivo
set "arquivo=%~dp0dist\Mover_PDFs.exe"

if not exist "%arquivo%" (
    echo.
    echo ERRO: O arquivo nao foi encontrado em:
    echo %arquivo%
    echo.
    pause
    exit /b 1
)

REM Executar comando para desbloquear
powershell -Command "Unblock-File -Path '%arquivo%'" 2>nul

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    SUCESSO! Arquivo desbloqueado!
    echo ========================================
    echo.
    echo Agora pode executar o arquivo normalmente:
    echo %arquivo%
    echo.
) else (
    echo.
    echo AVISO: Nao foi possivel desbloquear automaticamente.
    echo Por favor, desbloquear manualmente:
    echo 1. Clique com botao direito em Mover_PDFs.exe
    echo 2. Selecione "Propriedades"
    echo 3. Marque "Desbloqueado"
    echo 4. Clique "Aplicar" e "OK"
    echo.
)

pause



