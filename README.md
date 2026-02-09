# Organizar RPCMs por lote - EPC

Sistema para organização automática de arquivos PDF de RPCMs por lote.

## 🚀 Como usar

### Executar o programa

```bash
python main.py
```

### Ou usar o executável (se já foi gerado)

```bash
.\dist\Mover_PDFs.exe
```

## 📦 Gerar Executável

Para criar o arquivo `.exe`:

```bash
.\scripts\gerar_exe.bat
```

O executável será gerado em: `dist\Mover_PDFs.exe`

## 📋 Requisitos

```bash
pip install -r requirements.txt
```

## 📁 Estrutura do Projeto

```
📁 AutomacaoLotes/
├── main.py              ← Arquivo principal (interface gráfica)
├── mover_pdfs.py        ← Funções de cópia (versão CLI)
├── criar_icone.py       ← Script para criar ícone
├── app_icon.ico         ← Ícone da aplicação
├── requirements.txt     ← Dependências Python
├── 📁 scripts/          ← Scripts de build (.bat, .sh, .ps1)
├── 📁 build_config/     ← Arquivos de configuração (.spec, .manifest)
├── 📁 build/            ← Arquivos temporários do PyInstaller
└── 📁 dist/             ← Executável final
```

## 🔧 Funcionalidades

- ✅ Copiar arquivos PDF do Banco para Lotes específicos
- ✅ Verificar quais RPCMs estão presentes no Lote
- ✅ Detectar arquivos faltantes e excedentes
- ✅ Identificar números duplicados
- ✅ Interface gráfica intuitiva

## 📝 Como funciona

1. Selecione a **Pasta de Origem (Banco)** - onde estão todos os PDFs
2. Selecione a **Pasta de Destino (Lote)** - para onde serão copiados
3. Insira os **Números das RPCMs** que deseja organizar
4. Clique em **Verificar Destino** para conferir o que já existe
5. Clique em **Organizar Lote** para copiar os arquivos

---

Desenvolvido para EPC - Sabesp
