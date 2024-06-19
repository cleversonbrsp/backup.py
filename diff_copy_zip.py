import os
import shutil
import json
from zipfile import ZipFile
from datetime import datetime

# Função para listar arquivos em um diretório com suas datas de modificação
def listar_arquivos(diretorio):
    arquivos = {}
    for root, dirs, files in os.walk(diretorio):
        for file in files:
            caminho_completo = os.path.join(root, file)
            arquivos[caminho_completo] = os.path.getmtime(caminho_completo)
    return arquivos

# Função para copiar arquivos novos ou modificados, mantendo a estrutura de pastas
def copiar_arquivos_novos_ou_diferentes(arquivos_atual, arquivos_antigo, destino, source_dir):
    arquivos_copiados = []
    for arquivo, mtime in arquivos_atual.items():
        caminho_destino = os.path.join(destino, os.path.relpath(arquivo, start=source_dir))
        os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)

        # Copia apenas se o arquivo não existir no destino ou se for diferente (com base na data de modificação)
        if arquivo not in arquivos_antigo or mtime > arquivos_antigo[arquivo]:
            shutil.copy2(arquivo, caminho_destino)
            arquivos_copiados.append(arquivo)
    return arquivos_copiados

# Função para compactar uma pasta
def compactar_pasta(pasta, nome_zip):
    with ZipFile(nome_zip, 'w') as zipf:
        for root, dirs, files in os.walk(pasta):
            for file in files:
                caminho_completo = os.path.join(root, file)
                zipf.write(caminho_completo, os.path.relpath(caminho_completo, start=pasta))

# Função para carregar o estado anterior dos arquivos de um arquivo JSON
def carregar_estado_anterior(arquivo_registro):
    if os.path.exists(arquivo_registro):
        with open(arquivo_registro, 'r') as f:
            return json.load(f)
    return {}

# Função para salvar o estado atual dos arquivos em um arquivo JSON
def salvar_estado_atual(arquivo_registro, estado_atual):
    with open(arquivo_registro, 'w') as f:
        json.dump(estado_atual, f)

# Etapa 1: Solicita ao usuário para informar o diretório a ser analisado
def etapa1():
    source_dir = input("Digite o caminho do diretório que será analisado: ")
    if not os.path.exists(source_dir):
        print("O diretório informado não existe. Encerrando o script.")
        exit()
    return source_dir

# Etapa 2: Carrega o estado anterior dos arquivos e lista os arquivos novos ou modificados
def etapa2(source_dir):
    arquivo_registro = os.path.join(source_dir, 'arquivo_registro.json')
    estado_anterior = carregar_estado_anterior(arquivo_registro)
    estado_atual = listar_arquivos(source_dir)
    arquivos_diferentes = {k: v for k, v in estado_atual.items() if k not in estado_anterior or estado_anterior[k] != v}
    if not arquivos_diferentes:
        print("Nenhum arquivo novo ou modificado encontrado no diretório informado.")
        exit()
    print(f"Arquivos novos ou modificados encontrados no diretório {source_dir}:")
    for arquivo in arquivos_diferentes:
        print(arquivo)
    return estado_anterior, estado_atual, arquivos_diferentes, arquivo_registro

# Etapa 3: Solicita ao usuário para informar o diretório de destino e criar nova pasta
def etapa3():
    destination_dir = input("Digite o caminho do diretório onde os arquivos serão replicados: ")
    new_folder = input("Digite o nome da nova pasta onde os arquivos serão colados: ")
    new_destination = os.path.join(destination_dir, new_folder)
    os.makedirs(new_destination, exist_ok=True)
    print(f"Pasta {new_folder} criada em {destination_dir}.")
    return new_destination

# Etapa 4: Copia os arquivos novos ou modificados para o novo diretório
def etapa4(arquivos_diferentes, estado_anterior, new_destination, source_dir):
    arquivos_copiados = copiar_arquivos_novos_ou_diferentes(arquivos_diferentes, estado_anterior, new_destination, source_dir)
    if not arquivos_copiados:
        print("Nenhum arquivo novo ou modificado encontrado para copiar.")
    else:
        print(f"Arquivos novos ou modificados copiados para {new_destination}:")
        for arquivo in arquivos_copiados:
            print(arquivo)
    return arquivos_copiados

# Etapa 5: Compacta a pasta no formato .zip
def etapa5(new_destination):
    zip_file = f"{new_destination}.zip"
    compactar_pasta(new_destination, zip_file)
    print(f"A pasta foi compactada como {zip_file}.")

# Etapa 6: Salva o estado atual dos arquivos no arquivo de registro
def etapa6(arquivo_registro, estado_atual):
    salvar_estado_atual(arquivo_registro, estado_atual)
    print(f"O estado atual dos arquivos foi salvo em {arquivo_registro}.")

# Execução das etapas
def main():
    source_dir = etapa1()
    estado_anterior, estado_atual, arquivos_diferentes, arquivo_registro = etapa2(source_dir)
    new_destination = etapa3()
    arquivos_copiados = etapa4(arquivos_diferentes, estado_anterior, new_destination, source_dir)
    etapa5(new_destination)
    etapa6(arquivo_registro, estado_atual)

if __name__ == "__main__":
    main()
