import requests
import textwrap
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import chardet

# Configuração do site Aulette
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

    try:
        # Palavra
        palavra = soup.find("h2").text.strip()

        # Ortografia
        ortografia = soup.find("span", class_="silabas separacao-silaba")
        ortografia_texto = ortografia.text.strip() if ortografia else "Ortografia não encontrada"

        # Fonética
        fonetica = soup.find("span", class_="ort")
        fonetica_texto = fonetica.text.strip() if fonetica else "Não encontrada"

        # Gramática
        gramatica = soup.find("p", class_="classificacao1")
        gramatica_texto = gramatica.text.strip() if gramatica else "Não encontrada"

        # Definições
        definicoes = soup.find_all("p")
        lista_definicoes = [def_.text.strip() for def_ in definicoes if def_]

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
            "ortografia": ortografia_texto,
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


# Função para o Portal da Língua Portuguesa
def crawler_portal(palavra):
    url_base = "http://www.portaldalinguaportuguesa.org/?action=terminology&query="
    url_completa = url_base + palavra
    response = requests.get(url_completa)
    response.encoding = 'utf-8'

    resultados = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        ul_tag = soup.find("ul", style="margin-top: 0px; margin-bottom: 20px;")
        if ul_tag:
            links = ul_tag.find_all("a")
            for tag in links:
                texto = tag.get_text(strip=True)
                link = tag.get("href")
                if palavra in texto:
                    resultados.append(urljoin(url_base, link))
    return resultados


# Função para buscar terminologia detalhada
def detalhes_portal(link):
    response = requests.get(link)

    # Detectar a codificação correta
    detected_encoding = chardet.detect(response.content)["encoding"]
    response.encoding = detected_encoding if detected_encoding else "utf-8"

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        titulo1 = soup.find("h1").get_text(strip=True) if soup.find("h1") else "Título 1 não encontrado"
        titulo2 = soup.find("h2").get_text(strip=True) if soup.find("h2") else "Título 2 não encontrado"
        classificacao = soup.find("table", cellpadding="5")
        classificacao_texto = classificacao.get_text(strip=True) if classificacao else "Classificação não encontrada"
        texto = soup.find("div",
                          style="margin: 15px; padding: 10px; border: 1px solid #dedede; background-color: #eeeeee")
        texto_formatado = textwrap.fill(texto.get_text(strip=True),
                                        width=80) if texto else "Texto explicativo não encontrado"

        return {
            "titulo1": titulo1,
            "titulo2": titulo2,
            "classificacao": classificacao_texto,
            "texto": texto_formatado
        }
    return {}