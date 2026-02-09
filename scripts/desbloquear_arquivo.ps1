# Script PowerShell para desbloquear Mover_PDFs.exe

Write-Host ""
Write-Host "========================================"
Write-Host "    Desbloqueando Mover_PDFs.exe"
Write-Host "========================================"
Write-Host ""

$arquivo = Join-Path $PSScriptRoot "dist\Mover_PDFs.exe"

if (-not (Test-Path $arquivo)) {
    Write-Host ""
    Write-Host "ERRO: O arquivo nao foi encontrado em:"
    Write-Host $arquivo
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit 1
}

try {
    Unblock-File -Path $arquivo -ErrorAction Stop
    Write-Host ""
    Write-Host "========================================"
    Write-Host "    SUCESSO! Arquivo desbloqueado!"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "Agora pode executar o arquivo normalmente:"
    Write-Host $arquivo
    Write-Host ""
    Write-Host "Para iniciar o programa, execute:"
    Write-Host "& '$arquivo'"
    Write-Host ""
} catch {
    Write-Host ""
    Write-Host "AVISO: Nao foi possivel desbloquear automaticamente."
    Write-Host "Por favor, desbloquear manualmente:"
    Write-Host "1. Clique com botao direito em Mover_PDFs.exe"
    Write-Host "2. Selecione 'Propriedades'"
    Write-Host "3. Marque 'Desbloqueado'"
    Write-Host "4. Clique 'Aplicar' e 'OK'"
    Write-Host ""
    Write-Host "Erro: $_"
    Write-Host ""
}

Read-Host "Pressione Enter para sair"



