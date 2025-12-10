import ezdxf
import os
from datetime import datetime
import regiao as r

class Prancha:
    def __init__(self, largura, altura, nome_obra):
        self.largura = largura
        self.altura = altura
        self.nome_obra = nome_obra
        self.margem = 10
        self.largura_selo = 180
        self.altura_selo = 60

    def criar_prancha(self, msp):
        selo_x = self.largura - self.largura_selo - self.margem
        selo_y = self.margem

        moldura = [
            (self.margem, self.margem),
            (self.largura - self.margem, self.margem),
            (self.largura - self.margem, self.altura - self.margem),
            (self.margem, self.altura - self.margem),
            (self.margem, self.margem)
        ]
        msp.add_lwpolyline(moldura, dxfattribs={'layer': 'Prancha'})

        selo = [
            (selo_x, selo_y),
            (selo_x + self.largura_selo, selo_y),
            (selo_x + self.largura_selo, selo_y + self.altura_selo),
            (selo_x, selo_y + self.altura_selo),
            (selo_x, selo_y)
        ]
        msp.add_lwpolyline(selo, dxfattribs={'layer': 'Legenda'})

        msp.add_line((selo_x, selo_y + 20), (selo_x + self.largura_selo, selo_y + 20), dxfattribs={'layer': 'Legenda'})
        msp.add_line((selo_x, selo_y + 40), (selo_x + self.largura_selo, selo_y + 40), dxfattribs={'layer': 'Legenda'})
        msp.add_line((selo_x + 60, selo_y), (selo_x + 60, selo_y + self.altura_selo), dxfattribs={'layer': 'Legenda'})
        msp.add_line((selo_x + 120, selo_y), (selo_x + 120, selo_y + self.altura_selo), dxfattribs={'layer': 'Legenda'})

        msp.add_text('Projeto do Canteiro de Obras',
                     dxfattribs={
                         'layer': 'Legenda',
                         'height': 5,
                         'style': 'Standard',
                         'insert': (selo_x + 5, selo_y + 45)
                     })
        msp.add_text('Nome da Obra:',
                     dxfattribs={
                         'layer': 'Legenda',
                         'height': 4,
                         'style': 'Standard',
                         'insert': (selo_x + 5, selo_y + 25)
                     })
        msp.add_text(self.nome_obra,
                     dxfattribs={
                         'layer': 'Legenda',
                         'height': 4,
                         'style': 'Standard',
                         'insert': (selo_x + 65, selo_y + 25)
                     })
        msp.add_text('Data:',
                     dxfattribs={
                         'layer': 'Legenda',
                         'height': 4,
                         'style': 'Standard',
                         'insert': (selo_x + 5, selo_y + 5)
                     })
        msp.add_text(datetime.now().strftime("%d/%m/%Y"),
                     dxfattribs={
                         'layer': 'Legenda',
                         'height': 4,
                         'style': 'Standard',
                         'insert': (selo_x + 65, selo_y + 5)
                     })
        msp.add_text('Escala:',
                     dxfattribs={
                         'layer': 'Legenda',
                         'height': 4,
                         'style': 'Standard',
                         'insert': (selo_x + 125, selo_y + 25)
                     })
        msp.add_text('1:100',
                     dxfattribs={
                         'layer': 'Legenda',
                         'height': 4,
                         'style': 'Standard',
                         'insert': (selo_x + 125, selo_y + 5)
                     })
        msp.add_text('Desenhado por:',
                     dxfattribs={
                         'layer': 'Legenda',
                         'height': 4,
                         'style': 'Standard',
                         'insert': (selo_x + 65, selo_y + 45)
                     })
        msp.add_text('Seu Nome',
                     dxfattribs={
                         'layer': 'Legenda',
                         'height': 4,
                         'style': 'Standard',
                         'insert': (selo_x + 125, selo_y + 45)
                     })


class ProjetoCanteiro:
    def __init__(self, dir, nome_obra, tamanho_canteiro, pessoas, blocos_selecionados):
        self.nome_obra = nome_obra
        self.tamanho_canteiro = tamanho_canteiro
        self.pessoas = pessoas
        self.canteiro = r.Canteiro(tamanho_canteiro, pessoas, blocos_selecionados)

    def calcular_escala(self, largura_prancha_util, altura_prancha_util):
        escala_x = largura_prancha_util / self.tamanho_canteiro[0]
        escala_y = altura_prancha_util / self.tamanho_canteiro[1]
        return min(escala_x, escala_y)

    def executar(self, dir):
        pasta = dir
        if not os.path.exists(pasta):
            os.makedirs(pasta)

        self.canteiro.get_pontos_regioes()

        dxf = ezdxf.new(dxfversion='R2010')
        dxf.layers.new(name='Canteiro', dxfattribs={'color': 3})
        dxf.layers.new(name='Prancha', dxfattribs={'color': 1})
        dxf.layers.new(name='Legenda', dxfattribs={'color': 5})

        prancha = Prancha(420, 297, self.nome_obra)
        msp = dxf.modelspace()
        prancha.criar_prancha(msp)

        largura_prancha_util = prancha.largura - prancha.margem * 2 - prancha.largura_selo
        altura_prancha_util = prancha.altura - prancha.margem * 2

        escala = self.calcular_escala(largura_prancha_util, altura_prancha_util)

        #desenhar canteiro
        limites = [(limite[0] * escala + prancha.margem, limite[1] * escala + prancha.margem) for limite in self.canteiro.limites]
        msp.add_lwpolyline(limites + [limites[0]], dxfattribs={'layer': 'Canteiro'})

        #desenhar blocos
        for regiao in self.canteiro.regioes:
            pontos = [(ponto[0] * escala + prancha.margem, ponto[1] * escala + prancha.margem) for ponto in regiao.get_pontos()]
            msp.add_lwpolyline(pontos + [pontos[0]], dxfattribs={'layer': 'Canteiro'})
            msp.add_text(regiao.get_nome(),
                         dxfattribs={
                             'layer': 'Canteiro',
                             'height': 2.5,
                             'style': 'Standard',
                             'insert': (pontos[0][0] + 1, pontos[0][1] + 1)
                         })
            
            ponto_medio = [(pontos[0][0] + pontos[2][0]) / 2, (pontos[0][1] + pontos[2][1]) / 2]

            msp.add_text(f'{regiao.get_area()} m2',
                         dxfattribs={
                             'layer': 'Canteiro',
                             'height': 2.5,
                             'style': 'Standard',
                             'insert': (ponto_medio[0] - 5, ponto_medio[1]),
                         })


        caminho_arquivo = os.path.join(pasta, f'{self.nome_obra}.dxf')
        dxf.saveas(caminho_arquivo)
        print(f'Arquivo DXF salvo em: {caminho_arquivo}')
