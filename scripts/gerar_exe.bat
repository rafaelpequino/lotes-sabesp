@echo off
REM ========================================
REM Script rapido para gerar EXE
REM ========================================

echo.
echo ========================================
echo   GERANDO EXECUTAVEL - Mover_PDFs.exe
echo ========================================
echo.

REM Instalar PyInstaller se nao estiver
echo [1/3] Verificando dependencias...
pip install pyinstaller --quiet

REM Limpar builds anteriores
echo [2/3] Limpando arquivos antigos...
if exist "dist" rmdir /s /q dist 2>nul
if exist "build" rmdir /s /q build 2>nul
if exist "mover_pdfs_gui.spec" del mover_pdfs_gui.spec 2>nul

REM Criar o EXE
echo [3/3] Gerando executavel... (isso pode levar 1-2 minutos)
echo.

pyinstaller ^
  --onefile ^
  --windowed ^
  --name="Mover_PDFs" ^
  --icon=NONE ^
  --manifest=build_config\Mover_PDFs.manifest ^
  --distpath="dist" ^
  mover_pdfs_gui.py

REM Verificar se foi criado com sucesso
if exist "dist\Mover_PDFs.exe" (
  echo.
  echo ========================================
  echo    SUCESSO! EXE criado!
  echo ========================================
  echo.
  echo Caminho: dist\Mover_PDFs.exe
  echo.
  echo Para testar, execute:
  echo   .\dist\Mover_PDFs.exe
  echo.
) else (
  echo.
  echo ========================================
  echo    ERRO! Nao foi possivel criar o EXE
  echo ========================================
  echo.
)

pause

