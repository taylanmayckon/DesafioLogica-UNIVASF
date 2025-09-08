from flask import Flask, render_template, request
from logica import AnalisadorLogico

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = ""
    
    if request.method == "POST":
        entrada = request.form.get("sequencia", "")

        analisador = AnalisadorLogico(entrada)
        resultado = analisador.analisar_expressao()
        analisador.traduz_expressao()
        return render_template("index.html", resultado=resultado, 
                           erros=analisador.erros, 
                           formula_traduzida=analisador.formula_traduzida)

    return render_template("index.html", resultado=None, 
                           erros=None, 
                           formula_traduzida=None)

if __name__ == "__main__":
    app.run(debug=True)