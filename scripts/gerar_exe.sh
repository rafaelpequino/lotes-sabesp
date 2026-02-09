#!/bin/bash

# Script para gerar EXE no WSL

echo ""
echo "========================================"
echo "  GERANDO EXECUTAVEL - Mover_PDFs.exe"
echo "========================================"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ ERRO: Python3 não foi encontrado!"
    echo "Por favor, instale Python3 primeiro."
    exit 1
fi

echo "[1/3] Verificando dependências..."
pip3 install pyinstaller --quiet

if [ $? -ne 0 ]; then
    echo "❌ ERRO ao instalar PyInstaller!"
    exit 1
fi

echo "[2/3] Limpando arquivos antigos..."
rm -rf dist build mover_pdfs_gui.spec 2>/dev/null

echo "[3/3] Gerando executável... (isso pode levar 1-2 minutos)"
echo ""

pyinstaller \
  --onefile \
  --windowed \
  --name="Mover_PDFs" \
  --icon=NONE \
  --distpath="dist" \
  mover_pdfs_gui.py

# Verificar se foi criado com sucesso
if [ -f "dist/Mover_PDFs.exe" ]; then
  echo ""
  echo "========================================"
  echo "    ✅ SUCESSO! EXE criado!"
  echo "========================================"
  echo ""
  echo "Caminho: dist/Mover_PDFs.exe"
  echo ""
  echo "Para testar, execute no PowerShell (Windows):"
  echo "   .\dist\Mover_PDFs.exe"
  echo ""
else
  echo ""
  echo "========================================"
  echo "    ❌ ERRO! Não foi possível criar o EXE"
  echo "========================================"
  echo ""
fi



