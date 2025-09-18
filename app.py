from flask import Flask, render_template, request
from logica import AnalisadorLogico

app = Flask(__name__)

# TODO: Fazer um botão iterativo pra só mostrar o alfabeto utilizado quando clicar em algum botão
@app.route("/", methods=["GET", "POST"])
def index():
    analisador = None
    
    if request.method == "POST":
        entrada = request.form.get("sequencia", "")
        analisador = AnalisadorLogico(entrada)
        analisador.analisar_expressao()
        if analisador.resultado:
            analisador.traduz_expressao()
            analisador.converte_notacao_polonesa()
            analisador.gerar_tabela_verdade()
            analisador.verifica_propriedade_semantica()

    return render_template("index.html", analisador=analisador, alfabeto=AnalisadorLogico)

if __name__ == "__main__":
    app.run(debug=True)