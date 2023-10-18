# -- coding: utf-8 --
"""
Spyder Editor

lista relação de arquivos na página de dados públicos da receita federal
e faz o download
"""
from bs4 import BeautifulSoup
import requests, wget, os, sys, time, glob
from datetime import datetime
import pytz

url = "https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/dados-publicos-cnpj"
url = "http://200.152.38.155/CNPJ/"


pasta_compactados = r"dados-publicos-zip"  # local dos arquivos zipados da Receita

page = requests.get(url)
data = page.text
soup = BeautifulSoup(data)
lista = []
print("Relação de Arquivos em " + url)
for link in soup.find_all("a"):
    if str(link.get("href")).endswith(".zip"):
        cam = link.get("href")
        # if cam.startswith('http://http'):
        #     cam = 'http://' + cam[len('http://http//'):]
        if not cam.startswith("http"):
            # print(url+cam)
            lista.append(
                [cam, url + cam]
            )  # armazena na lista um vetor com o nome do arquivo e o link do arquivo
        else:
            # print(cam)
            # tratar aqui os casos em que já vem com a URL
            lista.append(cam)


arquivos = os.listdir(
    pasta_compactados
)  # LÊ TODOS OS ARQUIVOS QUE ESTAO NA PASTA DE DOWNLOAD E ESCREVE NA LISTA CHAMADA arquivos


def bar_progress(current, total, width=80):
    if total >= 2**20:
        tbytes = "Megabytes"
        unidade = 2**20
    else:
        tbytes = "kbytes"
        unidade = 2**10
    progress_message = f"Baixando: %d%% [%d / %d] {tbytes}" % (
        current / total * 100,
        current // unidade,
        total // unidade,
    )
    # Don't use print() as it will print in new line every time.
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()


count_baixados = 0
for k, url in enumerate(lista):
    if url[0] in arquivos:
        # print('encontrou o arquivo', url[0])
        response = requests.head(url[1])
        caminho_arquivo = os.path.join(pasta_compactados, url[0])
        if os.path.isfile(caminho_arquivo):
            data_modificacao_zip = os.path.getmtime(caminho_arquivo)
            data_modificacao_zip_number = datetime.fromtimestamp(data_modificacao_zip)
        else:
            data_modificacao_zip_number = 0

        if response.status_code == 200:
            last_modified = response.headers.get("Last-Modified")
            if last_modified:
                last_modified_web = datetime.strptime(
                    last_modified, "%a, %d %b %Y %H:%M:%S %Z"
                )
                if last_modified_web < data_modificacao_zip_number:
                    print(f"Arquivo já havia sido baixado ", url[0])
                else:
                    print(
                        "Precisa deletar o arquivo que já existe e baixar o novo",
                        url[0],
                    )
                    os.remove(caminho_arquivo)
                    wget.download(
                        url[1],
                        out=os.path.join(pasta_compactados, url[0]),
                        bar=bar_progress,
                    )
                    count_baixados += 1
            else:
                print(
                    "Não foi possível encontrar a data da última alteração nos cabeçalhos HTTP do arquivo."
                )
        else:
            print("Falha ao acessar o arquivo. Código de status:", response.status_code)
    else:
        print("Precisa baixar o arquivo ", url[0])
        wget.download(
            url[1], out=os.path.join(pasta_compactados, url[0]), bar=bar_progress
        )
        count_baixados += 1

print(
    "\n\n"
    + time.asctime()
    + f" Finalizou a verificação e download dos zips. Baixou {count_baixados} arquivos."
)
if count_baixados > 0:
    print("chamar aqui a função para criar a base")
