import itertools

class Node:
    """
    Classe para geração dos nós da Expression Binary Tree.
    """
    def __init__(self, info):
        self.info = info
        self.left = None
        self.right = None



class ExpressionBinaryTree:
    """
    Árvore binária para representar e avaliar expressões lógicas.
    """
    CONECTIVOS = ['¬', '∧', 'v', '→', '↔']

    def __init__(self, expression_list):
        self.expression = expression_list # Expressão em notaçao polonesa
        self.index = [0] # "Ponteiro" para a posição atual na lista
        self.root = self.build_tree_recursive() # Constroi a arvore

    # CONSTRUÇAO DA ÁRVORE -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def is_operator(self, token):
        """
        Verifica se um token é conectivo lógico.
        """
        return token in self.CONECTIVOS

    def build_tree_recursive(self):
        """
        Constrói recursivamente a árvore a partir da expressão em notação polonesa.
        """
        token = self.expression[self.index[0]]
        self.index[0] += 1
        node = Node(token)
        if self.is_operator(token):
            if token == '¬':  # unário
                node.left = self.build_tree_recursive()
            else:             # binário
                node.left = self.build_tree_recursive()
                node.right = self.build_tree_recursive()
        return node
    
    def debug_binary_tree(self, node=None):
        """
        Retorna os nós da árvore ena notaçao polonesa (para depuração).
        """
        if node is None:
            node = self.root
        result = []

        result.append(node.info)

        if node.left:
            result.extend(self.debug_binary_tree(node.left))
        if node.right:
            result.extend(self.debug_binary_tree(node.right))

        return result
    
    # AVALIAÇAO DAS EXPRESSÕES -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def evaluate(self, node, values):
        """
        Avalia recursivamente uma subárvore dado um dicionário de valores.
        """
        if not node:
            return None
        if node.info not in self.CONECTIVOS:
            if node.info == "V":  # Verdadeiro
                return True
            elif node.info == "F":  # Falso
                return False
            return values[node.info]
        if node.info == '¬':
            return not self.evaluate(node.left, values)
        elif node.info == '∧':
            return self.evaluate(node.left, values) and self.evaluate(node.right, values)
        elif node.info == 'v':
            return self.evaluate(node.left, values) or self.evaluate(node.right, values)
        elif node.info == '→':
            return (not self.evaluate(node.left, values)) or self.evaluate(node.right, values)
        elif node.info == '↔':
            return self.evaluate(node.left, values) == self.evaluate(node.right, values)

    def to_string(self, node):
        """
        Converte uma subárvore em string representando a subexpressão.
        """
        if not node:
            return ""
        if node.info not in self.CONECTIVOS:
            return node.info
        if node.info == '¬':
            return f"(¬{self.to_string(node.left)})"
        else:
            left_str = self.to_string(node.left)
            right_str = self.to_string(node.right)
            return f"({left_str} {node.info} {right_str})"
        
    # AVALIAÇAO DAS EXPRESSÕES -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def coletar_subexpressoes(self, node):
        """
        Retorna lista de subexpressões em ordem (da mais simples à completa).
        """
        if not node:
            return []
        
        subexpressoes = []
        if node.left:
            subexpressoes.extend(self.coletar_subexpressoes(node.left))
        if node.right:
            subexpressoes.extend(self.coletar_subexpressoes(node.right))
        
        subexpressoes.append(self.to_string(node))  # o nó atual por último
        return subexpressoes

    def mapear_subexpressoes(self, node, mapa):
        """
        Preenche um dicionário {subexpressao: node}
        """
        if not node:
            return
        if node.left:
            self.mapear_subexpressoes(node.left, mapa)
        if node.right:
            self.mapear_subexpressoes(node.right, mapa)
        mapa[self.to_string(node)] = node
    




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
        self.formula_traduzida = ""
        self.formula_polonesa = ""
        self.binary_tree = None

    # ANÁLISE E CONVERSÕES -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def analisar_expressao(self):
        """
        Analisa se é uma expressão lógica válida
        """

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
        """
        Traduz para os símbolos utilizados na lógica proposicional
        """
        self.formula_traduzida = self.formula
        for key, value in self.CORRESPONDENTE_ORIGINAL.items():
            self.formula_traduzida = self.formula_traduzida.replace(key, value)

    def converte_notacao_polonesa(self):
        """
        Converte a expressão para a notação polonesa
        """
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
            if char in self.VARIAVEIS or char in self.LOGICOS:
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
        self.binary_tree = ExpressionBinaryTree(self.formula_polonesa)
    
    # TABELA VERDADE -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def gerar_tabela_verdade(self) -> list:
        """Gera a tabela verdade com valores de todas as subexpressões."""
        variaveis = sorted(set(c for c in self.formula_traduzida if c in self.VARIAVEIS))
        combinacoes = list(itertools.product([False, True], repeat=len(variaveis)))

        subexpressoes = self.binary_tree.coletar_subexpressoes(self.binary_tree.root)
        mapa = {}
        self.binary_tree.mapear_subexpressoes(self.binary_tree.root, mapa)

        tabela = []
        for comb in combinacoes:
            valores = dict(zip(variaveis, comb))
            linha = dict(valores)
            for expr in subexpressoes:
                linha[expr] = self.binary_tree.evaluate(mapa[expr], valores)
            tabela.append(linha)

        return tabela


    


# Para teste por fora da interface Web
# Cria a Classe referente a expressao logica
# a = AnalisadorLogico("((PvQ)>R)<>P")
a = AnalisadorLogico("P>F")
a.analisar_expressao()
# Verifica se é expressão lógica
if a.resultado:
    # Se for, converte para notaçao polonesa
    print("✅ Fórmula válida")
    a.traduz_expressao()
    print(f"Formula analisada: {a.formula_traduzida}")
    a.converte_notacao_polonesa()
    print(f"Notação polonesa: {a.formula_polonesa}")
    # Aloca a notaçao polonesa na Expression Binary Tree
    print(f"[DEBUG] Conteudo da Binary Tree: {a.binary_tree.debug_binary_tree()}")
    # Print da tabela verdade
    tabela = a.gerar_tabela_verdade()
    for linha in tabela:
        print(linha)
    

else:
    # Se nao for interrompe execuçao e mostra os erros encontrados
    print("❌ Erros encontrados:")
    for erro in a.erros:
        print("-", erro)