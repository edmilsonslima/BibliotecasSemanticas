# -*- coding: utf-8 -*-
"""webcrawlervAuletefinal1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kOC_iS9JNTTMClqXz78ptHAZqINVoGrg
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# Configuração do site
BASE_URL = "https://www.aulete.com.br"
HEADERS = {
    "User-Agent": "Chrome/114.0.0.0"
}

# Função para obter o conteúdo HTML da página
def get_soup(url):
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        else:
            print(f"Erro ao acessar {url}: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
        return None

# Função para extrair a microestrutura de uma palavra
def extrair_microestrutura(url):
    soup = get_soup(url)
    if not soup:
        return None

    print(f"\nExtraindo microestrutura de: {url}\n")

    try:

        # Palavra
        palavra = soup.find("h2").text.strip()  # Nome da palavra

        # Ortogáfica
        ortografia = soup.find("span", class_="silabas separacao-silaba").text.strip()  # Nome da ortográfia
        ortografia_texto = ortografia.strip() if ortografia else "ortografia não encontrada"
        # Fonética
        #fonetica = soup.find("span", class_="ort").text.strip()  # Nome da fonética
        #fonetica_texto = fonetica.strip() if fonetica else fonetica = "não encontrada"

        # Fonética
        fonetica = soup.find("span", class_="ort")
        if fonetica:
          fonetica_texto = fonetica.text.strip()
        else:
          fonetica_texto = "não encontrada"

        # Gramática
        gramatica = soup.find("p", class_="classificacao1")
        if gramatica:
          gramatica_texto = gramatica.text.strip()
        else:
          gramatica_texto = "não encontrada"

        # Definições
        #definicoes = soup.find_all("p", class_=["numdef", "rub", "textodef","abon", "underline", "cochete", "ex", "uso","notaverb","marginNoloc"])
        definicoes = soup.find_all("p")
        lista_definicoes = [def_.text.strip() for def_ in definicoes if def_]
        #lista_definicoes = [def_.text.strip() for def_ in definicoes] if definicoes else []

        # Exemplos
        exemplos = soup.find_all("div", class_="exemplo")
        lista_exemplos = [ex.text.strip() for ex in exemplos] if exemplos else []

        # Sinônimos
        sinonimos = soup.find("div", class_="sinonimos")
        lista_sinonimos = (
            sinonimos.text.strip().replace("Sinônimos:", "").split(",") if sinonimos else []
        )

        return {
            "palavra": palavra,
            "ortografia": ortografia,
            "fonetica": fonetica_texto,
            "gramatica": gramatica_texto,
            "definicoes": lista_definicoes,
            "exemplos": lista_exemplos,
            "sinonimos": [s.strip() for s in lista_sinonimos],
        }
    except Exception as e:
        print(f"Erro ao extrair microestrutura: {e}")
        return None

# Função principal do crawler para várias palavras
def crawler_aulete(lista_palavras):
    resultados = {}
    for palavra in lista_palavras:
        url_palavra = f"{BASE_URL}/{palavra}"
        print(f"Processando palavra: {palavra} - URL: {url_palavra}")
        microestrutura = extrair_microestrutura(url_palavra)
        if microestrutura:
            resultados[palavra] = microestrutura
        else:
            print(f"Falha ao processar a palavra: {palavra}")
        time.sleep(1)  # Respeitar o servidor com um intervalo entre as requisições
    return resultados

# Lista de palavras para busca
palavras = ["terra"]

# Iniciar o crawler
resultado_microestrutura = crawler_aulete(palavras)

# Exibir os resultados
for palavra, dados in resultado_microestrutura.items():
    print(f"\nPalavra: {dados['palavra']}")
    print(f"Ortogáfica: {dados['ortografia']}")
    print(f"Fonética: {dados['fonetica']}")
    print(f"Gramática: {dados['gramatica']}")
    print("Definições:")
    for definicao in dados['definicoes']:
      if definicao != dados['ortografia'] and definicao != dados['gramatica']:
        print(f"- {definicao}")
    #print("Exemplos:")
    #for exemplo in dados['exemplos']:
        #print(f"- {exemplo}")
    #print("Sinônimos:")
    #print(", ".join(dados['sinonimos']) if dados['sinonimos'] else "Nenhum")