# Configurações de Build

Esta pasta contém os arquivos de configuração para a geração dos executáveis.

## Arquivos .spec

Os arquivos `.spec` são arquivos de configuração do **PyInstaller**, usados para definir como o executável será construído.

### Arquivos disponíveis:

- **Mover_PDFs.spec** - Configuração para gerar o executável `Mover_PDFs.exe`
  - Define o ícone da aplicação
  - Configura modo GUI (sem console)
  - Inclui o manifest
  
- **AutomacoesEPC.spec** - Configuração para gerar o executável `AutomacoesEPC.exe`
  - Configuração alternativa do mesmo projeto
  - Modo GUI sem console

- **Mover_PDFs.manifest** - Arquivo manifest do Windows para configurações de compatibilidade e permissões

## Como usar

Para gerar o executável usando um arquivo .spec:

```bash
pyinstaller build_config/Mover_PDFs.spec
```

Ou utilize os scripts disponíveis na pasta `scripts/`.
