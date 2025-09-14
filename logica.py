class Node:
    def __init__(self, info):
        info = self.info
        left = None
        right = None


class ExpressionBinaryTree:
    def __init__(self):
        self.root = None
        

class AnalisadorLogico():
    VARIAVEIS = "ABCDEGHIJKLMNOPQRSTUWXYZ"
    CONECTIVOS = "^v~><"
    PONTUACAO = {")": "(", 
                 "]": "[", 
                 "}": "{"}
    LOGICOS = "FV" 
    ALFABETO =  set(VARIAVEIS) | set(CONECTIVOS) | set(PONTUACAO.keys()) | set(PONTUACAO.values()) |  set(LOGICOS)
    
    CORRESPONDENTE_ORIGINAL = {"~": "¬", 
                               "^": "∧",
                               "<>": "↔",
                               ">": "→"}

    def __init__(self, formula: str):
        self.formula = formula
        self.erros = []
        self.resultado = None
        self.formula_traduzida = None
        self.formula_polonesa = None

    def analisar_expressao(self):
        self.erros.clear()

        # Pilha para paranteses, colchetes e chaves
        pilha = []

        for i, c in enumerate(self.formula):
            # Verificando se tem símbolo que não pertence ao meu "alfabeto"
            if c not in self.ALFABETO:
                self.erros.append(f"Caracter inválido '{c}' na posição {i}.")

            # Verificaçao dos parenteses
            elif c in self.PONTUACAO.values(): # Abertura
                pilha.append((c, i))
            elif c in self.PONTUACAO.keys(): # Fechamento
                if not pilha:
                    self.erros.append(f"Bracket '{c}' na posição {i} sem abertura correta.")
                else:
                    abertura, pos = pilha.pop()
                    if self.PONTUACAO[c] != abertura:
                        self.erros.append(f"Bracket '{c}' na posição {i} não compatível com a abertura {abertura} na posição {pos}.")

            # Verificando se tem conectivo "solto"
            elif c in self.CONECTIVOS:
                if c == "~":
                    if i == 0:
                        continue
                    elif self.formula[i-1] in self.CONECTIVOS or self.formula[i-1] in self.PONTUACAO.values():
                        continue
                    else:
                        self.erros.append(f"Negaçao '~' na posição {i} está em posição inválida.")
                else:
                    if i == 0: # Abertura da fórmula
                        self.erros.append(f"Conectivo '{c}' no início da fórmula, o que não é permitido.")
                    elif self.formula[i-1] in self.CONECTIVOS: # Sequencia de conectivos
                        if not (self.formula[i-1] in "<" and self.formula[i] == ">"): # Identificando o bi-implica
                            self.erros.append(f"Dois conectivos seguidos nas posições {i} e {i-1}")
                    elif (i+1 < len(self.formula)) and self.formula[i+1] in self.PONTUACAO.keys(): # Quando vem antes de fechamento de brackets
                        self.erros.append(f"Conectivo '{c}' na posição {i} não forma sub-expressão válida.")

            # Verificando posicionamento de variáveis 
            elif c in self.VARIAVEIS:
                if (i>0) and self.formula[i-1] in self.VARIAVEIS:
                    self.erros.append(f"Variável '{c}' na posição {i} seguida de outra variável ({self.formula[i-1]}).")
                elif (i>0) and self.formula[i-1] in self.LOGICOS:
                    self.erros.append(f"Variável '{c}' na posição {i} após um símbolo lógico ({self.formula[i-1]}).")
                elif (i+1 < len(self.formula)) and (self.formula[i+1] in self.PONTUACAO.values()):
                    self.erros.append(f"Variável '{c}' na posição {i} não pode preceder {self.formula[i+1]}.")
                elif (i>0) and (self.formula[i-1] in self.PONTUACAO.keys()):
                    self.erros.append(f"Variável '{c}' na posição {i} não pode vir após {self.formula[i-1]}.")
            
            # Verificando posicionamento dos simbolos logicos
            elif c in self.LOGICOS:
                if (i>0) and self.formula[i-1] in self.VARIAVEIS:
                    self.erros.append(f"Lógico '{c}' na posição {i} após uma variável ({self.formula[i-1]}).")
                elif (i>0) and self.formula[i-1] in self.LOGICOS:
                    self.erros.append(f"Lógico '{c}' na posição {i} seguido de outro símbolo lógico ({self.formula[i-1]}).")
                elif (i+1 < len(self.formula)) and (self.formula[i+1] in self.PONTUACAO.values()):
                    self.erros.append(f"Lógico '{c}' na posição {i} não pode preceder {self.formula[i+1]}.")
                elif (i>0) and (self.formula[i-1] in self.PONTUACAO.keys()):
                    self.erros.append(f"Lógico '{c}' na posição {i} não pode vir após {self.formula[i-1]}.")
        
        # Brackets que terminaram "abertos"
        for abertura, pos in pilha:
            self.erros.append(f"Bracket '{c}' na posição {i} sem fechamento.")

        if not len(self.erros):
            self.resultado = True
        else:
            self.resultado = False
    
    def traduz_expressao(self):
        # Traduz para os símbolos utilizados na lógica proposicional
        self.formula_traduzida = self.formula
        for key, value in self.CORRESPONDENTE_ORIGINAL.items():
            self.formula_traduzida = self.formula_traduzida.replace(key, value)

    def converte_notacao_polonesa(self):
        # Converte a expressão para a notação polonesa
        precedencia = {
            '¬': 4,  # Negação
            '∧': 3,  # Conjunção (E)
            'v': 2,  # Disjunção (OU)
            '→': 1,  # Implicação
            '↔': 0   # Bicondicional
        }
        operadores = set(precedencia.keys())

        pilha_operadores = []
        fila_saida = []

        # O algoritmo de Shunting Yard precisa que inverta a expressão para converter para Notação Polonesa
        expressao_invertida = self.formula_traduzida[::-1]

        for char in expressao_invertida:
            if char in self.VARIAVEIS:
                fila_saida.append(char)
            
            elif char in operadores:
                while(pilha_operadores and pilha_operadores[-1] in operadores and precedencia[pilha_operadores[-1]] > precedencia[char]):
                    fila_saida.append(pilha_operadores.pop())
                pilha_operadores.append(char)
            
            elif char == ')':
                pilha_operadores.append(char)

            elif char == '(':
                while pilha_operadores and pilha_operadores[-1] != ')':
                    fila_saida.append(pilha_operadores.pop())

                    if pilha_operadores:
                        pilha_operadores.pop()
        
        while pilha_operadores:
            fila_saida.append(pilha_operadores.pop())
        
        self.formula_polonesa = "".join(fila_saida[::-1])
    
    

# Para teste por fora da interface Web
a = AnalisadorLogico("((PvQ)>R)<>P")
a.analisar_expressao()
if a.resultado:
    print("✅ Fórmula válida")
    a.traduz_expressao()
    print(f"Formula analisada: {a.formula_traduzida}")
    a.converte_notacao_polonesa()
    print(f"Notação polonesa: {a.formula_polonesa}")
else:
    print("❌ Erros encontrados:")
    for erro in a.erros:
        print("-", erro)