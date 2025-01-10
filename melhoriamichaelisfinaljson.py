# -*- coding: utf-8 -*-
"""MelhoriaMichaelisFinalJSON.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16MX8-FQKrLHXlSpCmDIeLrrd6OcyOgm_
"""

import json
import re
import requests
from bs4 import BeautifulSoup

# Definição dos parâmetros
URL = "https://michaelis.uol.com.br/moderno-portugues/busca/portugues-brasileiro/mesa"
HEADERS = {
    "User-Agent": "Chrome/114.0.0.0"
}

# Função para obter o objeto BeautifulSoup com tratamento de erros
def get_soup(url, headers=None, params=None):
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao acessar a página: {e}")

# Função para formatar o conteúdo principal das definições
def format_definition_content(content):
    formatted_lines = []
    lines = content.split("\n")
    current_line = ""

    for line in lines:
        if line.strip().startswith(tuple(str(i) for i in range(1, 200))):  # Suporte para até 200 definições
            if current_line:
                formatted_lines.append(current_line.strip())
            current_line = line.strip()
        else:
            current_line += f" {line.strip()}"

    if current_line:
        formatted_lines.append(current_line.strip())

    return formatted_lines

# Função para processar definições, ignorando a primeira linha das definições
def process_definitions(formatted_content):
    definitions = []
    num_palavras = len(formatted_content[0].split())
    if num_palavras == 3:
        formatted_content = formatted_content[1:]
    else:
        formatted_content = formatted_content[2:]

    for line in formatted_content: # Pula a primeira linha de "Definições"
        if "EXPRESSÕES" in line:  # Interrompe no início de "EXPRESSÕES"
            break
        clean_line = re.sub(r"\s+", " ", line).strip()
        definitions.append(clean_line)
    return definitions

# Função para extrair seções como EXPRESSÕES e ETIMOLOGIA
def extract_section(content, section_name):
    start_idx = content.find(section_name)
    if start_idx != -1:
        section_content = content[start_idx + len(section_name):].strip()
        next_section_start = section_content.find("\n\n")
        if next_section_start != -1:
            section_content = section_content[:next_section_start].strip()
        sentences = section_content.split(".")
        formatted_sentences = [
            sentence.replace("\n", " ").strip() + "." for sentence in sentences if sentence.strip()
        ]
        return formatted_sentences
    return []

# Função principal para extrair e exibir os dados no terminal
def extract_and_display_content(url, headers, output_file="resultado.json"):  # Adicionando output_file como parâmetro
    try:
        soup = get_soup(url, headers)
        definition_block = soup.find("div", class_="verbete bs-component")

        if not definition_block:
            print("Nenhuma definição encontrada.")
            return

        content = definition_block.get_text(separator="\n", strip=True)
        formatted_content = format_definition_content(content)

        # Estrutura para armazenar os dados
        result = {}

        # Processar palavra, ortografia e gramática
        if formatted_content:
            words = re.findall(r'\S+', formatted_content[0])
            if len(words) >= 3:
                result["palavra"] = words[0]
                result["ortografia"] = words[1]
                result["gramatica"] = words[2]
            elif len(words) == 1:
                words_indice = re.findall(r'\S+', formatted_content[1])
                result["palavra"] = formatted_content[0]
                result["ortografia"] = words_indice[1]
                result["gramatica"] = words_indice[2]
            else:
                raise ValueError("Formato inesperado na primeira linha.")

        # Processar definições e remover a primeira linha
        result["definicoes"] = process_definitions(formatted_content)

        # Processar seções de EXPRESSÕES e ETIMOLOGIA
        expressoes = extract_section(content, "EXPRESSÕES")
        result["expressoes"] = [
            re.sub(r"\s+", " ", expression).strip()
            for expression in expressoes
            if "ETIMOLOGIA" not in expression  # Exclui linhas que contêm "ETIMOLOGIA"
        ]

        result["etimologia"] = [
            re.sub(r"\s+", " ", etymology).strip()
            for etymology in extract_section(content, "ETIMOLOGIA")
        ]

        # Exibir os resultados no terminal
        print("\n--- Resultados Extraídos ---")
        print(f"Palavra: {result['palavra']}")
        print(f"Ortografia: {result['ortografia']}")
        print(f"Gramática: {result['gramatica']}")
        print("Definições:")
        for definicao in result["definicoes"]:
            print(f"- {definicao}")
        print("Expressões:")
        for expressao in result["expressoes"]:
            print(f"- {expressao}")
        print("Etimologia:")
        for etimologia in result["etimologia"]:
            print(f"- {etimologia}")

        # Salvar os resultados em um arquivo JSON
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(result, json_file, ensure_ascii=False, indent=4)
        print(f"Dados salvos em {output_file}")

    except Exception as e:
        print(f"Erro ao processar os dados: {e}")

# Executar a extração e exibir os resultados no terminal
extract_and_display_content(URL, HEADERS)   # Não precisa mais definir output_file aqui, o parâmetro tem valor padrão