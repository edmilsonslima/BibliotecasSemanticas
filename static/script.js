// Função para buscar no Dicionário Aulette
document.getElementById("form-palavras").addEventListener("submit", async (e) => {
    e.preventDefault();

    const palavras = document.getElementById("palavras").value
        .split(",")
        .map((palavra) => palavra.trim())
        .filter((palavra) => palavra.length > 0);

    if (palavras.length === 0) {
        alert("Por favor, insira pelo menos uma palavra.");
        return;
    }

    const outputElement = document.getElementById("output");
    outputElement.textContent = "Buscando no Dicionário Aulette...";

    try {
        const response = await fetch("/buscar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ palavras }), // Envia a lista de palavras
        });

        if (!response.ok) {
            const error = await response.json();
            outputElement.textContent = `Erro: ${error.error}`;
            return;
        }

        const resultados = await response.json();
        outputElement.textContent = JSON.stringify(resultados, null, 2); // Exibe os resultados
    } catch (error) {
        outputElement.textContent = `Erro ao buscar palavras no Aulette: ${error.message}`;
    }
});

// Função para buscar no Portal da Língua Portuguesa
async function buscarPortal() {
    const palavra = document.getElementById("palavra-portal").value.trim();
    if (!palavra) {
        alert("Por favor, insira uma palavra!");
        return;
    }

    const outputPortal = document.getElementById("output-portal");
    outputPortal.textContent = "Buscando no Portal da Língua Portuguesa...";

    try {
        const response = await fetch("/buscar_portal", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ palavra }), // Envia a palavra ao backend
        });

        if (response.ok) {
            const data = await response.json();
            outputPortal.textContent = JSON.stringify(data.detalhes, null, 2); // Exibe os resultados
        } else {
            const error = await response.json();
            outputPortal.textContent = `Erro: ${error.error}`;
        }
    } catch (error) {
        outputPortal.textContent = `Erro ao buscar palavra no Portal: ${error.message}`;
    }
}

// Função para buscar simultaneamente no Dicionário Aulette e no Portal da Língua Portuguesa
async function buscarCombinado() {
    const palavra = document.getElementById("palavra-combinada").value.trim();
    if (!palavra) {
        alert("Por favor, insira uma palavra!");
        return;
    }

    const output = document.getElementById("output");
    const outputPortal = document.getElementById("output-portal");
    output.textContent = "Buscando no Dicionário Aulette...";
    outputPortal.textContent = "Buscando no Portal da Língua Portuguesa...";

    try {
        // Faz a busca no Dicionário Aulette
        const responseAulette = await fetch("/buscar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ palavras: [palavra] }),
        });

        // Faz a busca no Portal da Língua Portuguesa
        const responsePortal = await fetch("/buscar_portal", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ palavra }),
        });

        if (responseAulette.ok && responsePortal.ok) {
            const dataAulette = await responseAulette.json();
            const dataPortal = await responsePortal.json();

            output.textContent = JSON.stringify(dataAulette, null, 2); // Resultados do Aulette
            outputPortal.textContent = JSON.stringify(dataPortal.detalhes, null, 2); // Resultados do Portal
        } else {
            const errorAulette = responseAulette.ok ? null : await responseAulette.json();
            const errorPortal = responsePortal.ok ? null : await responsePortal.json();

            output.textContent = errorAulette ? `Erro Aulette: ${errorAulette.error}` : "";
            outputPortal.textContent = errorPortal ? `Erro Portal: ${errorPortal.error}` : "";
        }
    } catch (error) {
        output.textContent = `Erro ao buscar no Aulette: ${error.message}`;
        outputPortal.textContent = `Erro ao buscar no Portal: ${error.message}`;
    }
}