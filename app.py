from flask import Flask, render_template, request
from logica import AnalisadorLogico

app = Flask(__name__)

# TODO: Implementa AJAX pra não ficar recarregando toda hora a página
@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    
    if request.method == "POST":
        entrada = request.form.get("sequencia", "")
        analisador = AnalisadorLogico(entrada)
        resultado = analisador.analisar_expressao()
    return render_template("index.html", resultado=resultado, erros=analisador.erros)

if __name__ == "__main__":
    app.run(debug=True)