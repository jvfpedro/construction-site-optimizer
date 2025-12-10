import random

class Canteiro:
    def __init__(self, dim, pessoas, blocos_selecionados):
        self.x_max = dim[0]
        self.y_max = dim[1]
        self.limites = [
            [0, 0],
            [self.x_max, 0],
            [self.x_max, self.y_max],
            [0, self.y_max]
        ]
        self.regioes = []
        self.pessoas = pessoas
        self.entrada_obra = [self.x_max / 2, 0]  # Definindo a entrada da obra no centro da parte de baixo do canteiro

        # Tamanhos conforme NR18
        self.tamanhos_blocos = {
            'Deposito': (10, 10),
            'Elevador': (5, 5) if self.pessoas > 30 else (3, 3),
            'Banheiro': (2.45 * (self.pessoas // 20 + 1), 2.45),
            'Refeitorio': (10, self.pessoas / 10),  # 1m² para cada trabalhador, assumindo largura de 10 metros
            'Almoxarifado': (10, 10),
            'Bebedouro': (1 * (self.pessoas // 25 + 1), 1),
            'Vestiario': (13.72 * (self.pessoas // 25 + 1), 13.72)
        }

        self.tamanhos_blocos = {bloco: tamanho for bloco, tamanho in self.tamanhos_blocos.items() if bloco in blocos_selecionados}

        # Parâmetros do Algoritmo Genético
        self.population_size = 100
        self.mutation_rate = 0.05
        self.generations = 3000

        # Criação dos blocos utilizando algoritmo genético
        self.best_layout, self.best_score = self.gen([0, 0], dim, list(self.tamanhos_blocos.items()))

    def create_individual(self, dim, blocos):
        layout = []
        for bloco_nome, (largura, altura) in blocos:
            while True:
                x = random.uniform(0, self.x_max - largura)
                y = random.uniform(0, self.y_max - altura)
                novo_bloco = Bloco(bloco_nome, largura, altura, [x, y])
                if all(not self.overlaps(novo_bloco, bloco) for bloco in layout):
                    layout.append(novo_bloco)
                    break
        return layout

    def create_population(self, size, dim, blocos):
        return [self.create_individual(dim, blocos) for _ in range(size)]

    def select_parents(self, population, scores, k=3):
        selected = random.choices(population, k=k, weights=scores)
        return max(selected, key=lambda layout: self.score(layout))

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, len(parent1) - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child

    def mutate(self, layout):
        for bloco in layout:
            if random.random() < self.mutation_rate:
                bloco.set_origem(
                    random.uniform(0, self.x_max - bloco.largura),
                    random.uniform(0, self.y_max - bloco.altura)
                )
        return layout

    def gen(self, origem, dim, blocos):
        population = self.create_population(self.population_size, dim, blocos)
        best_score = -1
        best_layout = None

        for generation in range(self.generations):
            scores = [self.score(layout) for layout in population]
            current_best_score = max(scores)
            current_best_layout = population[scores.index(current_best_score)]

            print(f"Generation {generation+1} Best Score: {current_best_score}")

            if current_best_score > best_score:
                best_score = current_best_score
                best_layout = current_best_layout

            if best_score == 70:  # Melhor score possível, por exemplo
                break

            if sum(scores) == 0:  # Verificação para evitar erro
                print("Todas as pontuações são zero. Verifique a função de pontuação.")
                break

            next_generation = []
            for _ in range(self.population_size):
                parent1 = self.select_parents(population, scores)
                parent2 = self.select_parents(population, scores)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                next_generation.append(child)
            population = next_generation

        self.regioes = best_layout
        print(f"O melhor score é: {best_score}")
        return best_layout, best_score

    def score(self, layout):
        score = 0
        vestiario = None
        refeitorio = None
        deposito = None
        elevador = None
        almoxarifado = None
        
        for bloco in layout:
            if bloco.get_nome() == 'Deposito':
                deposito = bloco
                for outro_bloco in layout:
                    if outro_bloco.get_nome() == 'Banheiro':
                        dist = self.distance(bloco.get_origem(), outro_bloco.get_origem())
                        if dist > 10:
                            score += 10

            if bloco.get_nome() == 'Vestiario':
                vestiario = bloco
                dist_entrada = self.distance(bloco.get_origem(), self.entrada_obra)
                if dist_entrada < 10:
                    score += 10

            if bloco.get_nome() == 'Banheiro' and vestiario:
                if self.overlaps(bloco, vestiario):
                    score += 10

            if bloco.get_nome() == 'Refeitorio':
                refeitorio = bloco

            if bloco.get_nome() == 'Elevador':
                elevador = bloco
                if any(self.distance(bloco.get_origem(), limite) < 10 for limite in self.limites):
                    score += 10

            if bloco.get_nome() == 'Almoxarifado':
                almoxarifado = bloco

        if vestiario and refeitorio:
            dist_refeitorio = self.distance(vestiario.get_origem(), refeitorio.get_origem())
            if dist_refeitorio > 50:
                score += 10

        if deposito and elevador:
            dist = self.distance(deposito.get_origem(), elevador.get_origem())
            if dist < 10:
                score += 10

        if almoxarifado and refeitorio:
            dist = self.distance(almoxarifado.get_origem(), refeitorio.get_origem())
            if dist > 10:
                score += 10

        return score

    def overlaps(self, bloco1, bloco2):
        return not (
            bloco1.origem[0] + bloco1.largura <= bloco2.origem[0] or
            bloco1.origem[0] >= bloco2.origem[0] + bloco2.largura or
            bloco1.origem[1] + bloco1.altura <= bloco2.origem[1] or
            bloco1.origem[1] >= bloco2.origem[1] + bloco2.altura
        )

    def distance(self, origem1, origem2):
        return ((origem1[0] - origem2[0]) ** 2 + (origem1[1] - origem2[1]) ** 2) ** 0.5

    def get_limites(self):
        return self.limites

    def get_largura(self):
        return self.x_max

    def get_altura(self):
        return self.y_max

    def add_regiao(self, regiao):
        self.regioes.append(regiao)

    def get_pontos_regioes(self):
        for regiao in self.regioes:
            print(f'Regiao:{regiao.get_nome()}\nPontos:{regiao.get_pontos()}')

class Bloco:
    def __init__(self, nome, largura, altura, origem):
        self.nome = nome
        self.largura = largura
        self.altura = altura
        self.origem = origem
        self.pontos = [
            origem,
            [origem[0] + self.largura, origem[1]],
            [origem[0] + self.largura, origem[1] + self.altura],
            [origem[0], origem[1] + self.altura]
        ]

    def set_tamanho(self, largura, altura):
        self.largura = largura
        self.altura = altura

    def set_origem(self, x, y):
        self.origem = [x, y]
        self.pontos = [
            self.origem,
            [self.origem[0] + self.largura, self.origem[1]],
            [self.origem[0] + self.largura, self.origem[1] + self.altura],
            [self.origem[0], self.origem[1] + self.altura]
        ]

    def get_tamanho(self):
        return self.largura, self.altura
    
    def get_area(self):
        return self.largura*self.altura

    def get_origem(self):
        return self.origem

    def get_nome(self):
        return self.nome

    def get_pontos(self):
        return self.pontos

class Entrada:
    def __init__(self, entrada, tamanho=1):
        self.entrada = [entrada, entrada + tamanho]

    def get_entrada(self):
        return self.entrada