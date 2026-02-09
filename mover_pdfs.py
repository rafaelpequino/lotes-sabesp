import os
import shutil
from pathlib import Path

def mover_pdfs_por_lista(pasta_origem, pasta_destino, lista_numeros):
    """
    Copia PDFs de uma pasta para outra baseado em uma lista de números.
    
    Args:
        pasta_origem (str): Caminho da pasta contendo os PDFs
        pasta_destino (str): Caminho da pasta de destino
        lista_numeros (list): Lista de números (ex: ['400006', '400009', '400010'])
    """
    
    # Converter para Path para melhor manipulação
    pasta_origem = Path(pasta_origem)
    pasta_destino = Path(pasta_destino)
    
    # Verificar se a pasta de origem existe
    if not pasta_origem.exists():
        print(f"❌ Erro: A pasta de origem não existe: {pasta_origem}")
        return
    
    # Criar pasta de destino se não existir
    if not pasta_destino.exists():
        pasta_destino.mkdir(parents=True, exist_ok=True)
        print(f"📁 Pasta de destino criada: {pasta_destino}")
    
    # Converter lista de números para strings e criar um conjunto para busca rápida
    lista_numeros_str = {str(num).strip() for num in lista_numeros}
    
    # Contar arquivos movidos e não movidos
    arquivos_movidos = 0
    arquivos_nao_encontrados = 0
    arquivos_totais = 0
    
    print(f"\n🔍 Procurando PDFs com os números: {', '.join(sorted(lista_numeros_str))}")
    print(f"📂 Pasta de origem: {pasta_origem}")
    print(f"📂 Pasta de destino: {pasta_destino}")
    print("-" * 80)
    
    # Listar todos os arquivos PDF na pasta de origem (case-insensitive)
    arquivos_encontrados = list(pasta_origem.glob("*.[pP][dD][fF]"))
    
    for arquivo in arquivos_encontrados:
        arquivos_totais += 1
        
        # Obter o nome do arquivo sem extensão
        nome_arquivo = arquivo.stem
        
        # Extrair o número inicial do nome (antes do primeiro underscore ou hífen)
        numero = nome_arquivo.split('_')[0]
        
        # Verificar se o número está na lista
        if numero in lista_numeros_str:
            try:
                # Copiar arquivo para pasta de destino
                caminho_destino = pasta_destino / arquivo.name
                shutil.copy2(str(arquivo), str(caminho_destino))
                print(f"✅ Copiado: {arquivo.name}")
                arquivos_movidos += 1
            except Exception as e:
                print(f"❌ Erro ao copiar {arquivo.name}: {e}")
        else:
            arquivos_nao_encontrados += 1
    
    # Resumo
    print("-" * 80)
    print(f"\n📊 Resumo da operação:")
    print(f"   Total de PDFs na pasta: {arquivos_totais}")
    print(f"   Arquivos copiados: {arquivos_movidos}")
    print(f"   Arquivos não correspondentes: {arquivos_nao_encontrados}")
    print(f"   Números procurados: {len(lista_numeros_str)}")


def main():
    """Função principal com configurações"""
    
    # CONFIGURAR AQUI:
    # Caminho da pasta com os PDFs
    pasta_origem = r"C:\Users\rafae\Downloads\pasta01"
    
    # Caminho da pasta de destino
    pasta_destino = r"C:\Users\rafae\Downloads\destino"
    
    # Lista de números desejados
    lista_numeros = ['400006', '400496', '400010']
    
    # ========================================
    # Executar a operação
    mover_pdfs_por_lista(pasta_origem, pasta_destino, lista_numeros)
    
    print("\n✨ Operação concluída!")


if __name__ == "__main__":
    main()

