@echo off
REM Script para converter o arquivo Python em EXE
REM Este script instala as dependências necessárias e cria o executável

echo.
echo ========================================
echo  Criando Executavel da Automacao
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao foi encontrado!
    echo Por favor, instale Python primeiro.
    pause
    exit /b 1
)

echo [1/3] Instalando PyInstaller...
pip install pyinstaller --quiet

if errorlevel 1 (
    echo ERRO ao instalar PyInstaller!
    pause
    exit /b 1
)

echo [2/3] Removendo build anterior...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
if exist "main.spec" del main.spec

echo [3/3] Convertendo para EXE...
pyinstaller --onefile --windowed --icon=NONE --name="Mover_PDFs" main.py

if errorlevel 1 (
    echo ERRO ao criar executavel!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Executavel criado com sucesso!
echo ========================================
echo.
echo Arquivo: dist\Mover_PDFs.exe
echo.
pause



