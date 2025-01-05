from flask import Flask, request, jsonify, render_template
from crawler import crawler_aulete, crawler_portal, detalhes_portal # Importa o módulo do crawler

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # Página principal do front-end

@app.route("/buscar", methods=["POST"])
def buscar():
    data = request.json  # Recebe os dados enviados pelo front-end
    palavras = data.get("palavras", [])  # Pega a lista de palavras
    
    if not palavras:
        return jsonify({"error": "Nenhuma palavra enviada!"}), 400

    resultados = crawler_aulete(palavras)  # Usa as palavras recebidas
    return jsonify(resultados)

@app.route("/buscar_portal", methods=["POST"])
def buscar_portal():
    data = request.json
    palavra = data.get("palavra")
    if not palavra:
        return jsonify({"error": "Palavra não fornecida"}), 400

    links = crawler_portal(palavra)
    detalhes = [detalhes_portal(link) for link in links]
    return jsonify({"detalhes": detalhes})

if __name__ == "__main__":
    app.run(debug=True)
