#!/usr/bin/python3
#-*- encoding: utf-8 -*-
#Copyright (C) 2016  Saullo Oliveira
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Classes relacionadas a obtenção das proposições a partir dos Web Services da
Câmara dos Deputados.

A documentação oficial da câmara está **ERRADA** e não corresponde ao resultado
dos Web Services. Então, verifique a documentação de cada método.
"""
__author__ = "Saullo Oliveira"
__copyright__ = "Copyright 2016"
__credits__ = ["Saullo Oliveira"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Saullo Oliveira"
__email__ = "shgo@dca.fee.unicamp.br"
__status__ = "Development"


class TipoAutor:
    """
    Classe dos tipos de autores de proposição.
    """


    def __init__(self, id_, descricao):
        """
        Método construtor.
        Args:
            id_ (int): id do tipo de autor.
            descricao (str): descrição do tipo de autor.
        """
        self.id_ = id_
        self.descricao = descricao


class SiglaTipoProposicao:
    """
    Classe das siglas dos tipos de proposição.
    """


    def __init__(self, sigla, descricao, ativa, genero):
        """
        Método construtor.
        Args:
            sigla (str): sigla do tipo de proposição (espécie da proposição).
            descricao (str): descrição do tipo de proposição.
            ativa (str): indica se é uma sigla ativa. 1 = Ativa; 2 = Inativa.
            genero (str): indicador do gênero da sigla da proposição.
        """
        self.sigla = sigla
        self.descricao = descricao
        self.ativa = ativa
        self.genero = genero


class Orgao:
    """
    Classe que indica o órgão de uma situação.
    Sempre será atributo de Situação.
    """


    def __init__(self, id_, sigla):
        """
        Método construtor.
        Args:
            id_ (int)
            sigla (str)
        """
        self.id_ = id_
        self.sigla = sigla


class SituacaoProposicao:
    """
    Classe que representa a situação de uma proposição.
    Sempre será atributo de Proposicao.
    """


    def __init__(self, id_, descricao):
        """
        Método construtor.
        Args:
            id_ (int)
            descricao (str)
        """
        self.id_ = id_
        self.descricao = descricao
        self.orgao = None
        self.prop_principal = None


    def set_orgao(self, orgao):
        """
        Seta o órgão da situação.
        Args:
            orgao (Orgao)
        """
        assert isinstance(orgao, Orgao), \
                'orgao não é um Orgao'
        self.orgao = orgao


    def set_prop_principal(self, principal):
        """
        Seta a proposição principal da proposição nesse órgao.
        Pelo menos é assim que tá na estrutura do XML.
        Args:
            principal (cod_prop_principal, prop_principal)
        """
        self.prop_principal = principal


class Autor:
    """
    Classe que representa o autor de uma proposição.
    Sempre será atributo de Proposicao.
    """


    def __init__(self, nome, ide_cadastro, cod_partido, sigla_partido, uf_):
        """
        Método construtor.
        Args:
            nome (str)
            ide_cadastro (str)
            cod_partido (str)
            sigla_partido (str)
            uf_ (str)
        """
        self.nome = nome
        self.ide_cadastro = ide_cadastro
        self.cod_partido = cod_partido
        self.sigla_partido = sigla_partido
        self.uf_ = uf_


class OrgaoNumerador:
    """
    Classe que indica o órgão numerador de uma proposição.
    Sempre será atributo de Proposicao.
    """


    def __init__(self, id_, sigla, nome):
        """
        Método construtor.
        Args:
            id_ (int)
            sigla (str)
            nome (str)
        """
        self.id_ = id_
        self.sigla = sigla
        self.nome = nome


class UltimoDespacho:
    """
    Classe com dados do último despacho de uma proposição.
    Sempre será atributo de Proposicao.
    """


    def __init__(self, data, texto):
        """
        Método construtor.
        Args:
            data (str)
            texto (str)
        """
        self.data = data
        self.texto = texto


class Regime:
    """
    Classe que indica o regime de transição da proposição.
    Sempre será atributo de Proposicao.
    """


    def __init__(self, id_, descricao):
        """
        Método construtor.
        Args:
            id_ (int)
            descricao (str)
        """
        self.id_ = id_
        self.descricao = descricao


class TipoProposicao:
    """
    Classe que indica o tipo da proposição.
    Sempre será atributo de Proposicao.
    """


    def __init__(self, id_, sigla, nome):
        """
        Método construtor.
        Args:
            id_ (int)
            sigla (str)
            nome (str)
        """
        self.id_ = id_
        self.sigla = sigla
        self.nome = nome


class Apreciacao:
    """
    Classe que representa a apreciação de uma proposição.
    Sempre será atributo de Proposicao.
    """


    def __init__(self, id_, descricao):
        """
        Método construtor.
        Args:
            id_ (int)
            descricao (str)
        """
        self.id_ = id_
        self.descricao = descricao


class Proposicao:
    """
    Classe que representa uma proposição de lei.

    Os seus atributos correspondem aos campos do xml retornado pelo Web Service,
    que são ligeiramente diferentes da documentação da página da câmara.

    Os atributos podem ser obtidos por dois WS, são eles:
        ListarProposicoes - LP
        ObterProposicaoPorID - PID
    Nesse caso, ao final da descrição de cada atributo essas siglas irão
    indicar qual dos WS é a fonte do valor.
    """


    def __init__(self, id_, nome, numero, ano, data_apresentacao, ementa,
                 exp_ementa, qtde_autores, ind_genero, qtd_orgaos_com_estado):
        """
        Método construtor.
        Args:
            id_ (int) - id da proposição. LP PID
            nome (str) - nome da proposição. LP PID
            numero (int) - número da proposição. LP
            ano (int) - ano da apresentação da proposição. LP
            data_apresentacao (str) - data da apresentação da proposição. LP PID
            ementa (str) - ementa da proposição. LP PID
            exp_ementa (str) - explicação da ementa da proposição. LP PID
            qtde_autores (int) - qtde de autores que subscreveram a prop. LP
            ind_genero (int) - não há descrição. LP
            qtd_orgaos_com_estado (int) - não há descrição. LP
        """
        self.id_ = id_
        self.nome = nome
        self.numero = numero
        self.ano = ano
        self.data_apresentacao = data_apresentacao
        self.ementa = ementa
        self.exp_ementa = exp_ementa
        self.qtde_autores = qtde_autores
        self.ind_genero = ind_genero
        self.qtd_orgaos_com_estado = qtd_orgaos_com_estado
        self.tipo_proposicao = None
        self.orgao_numerador = None
        self.regime = None
        self.apreciacao = None
        self.autor1 = None
        self.ultimo_despacho = None
        self.situacao = None
        self.indices = None
        self.tema = None
        self.link_inteiro_teor = None
        self.apensadas = []


    def __str__(self):
        """
        Formata a impressão do objeto quando print(self) é invocado.
        """
        texto = ("Proposição de lei:\n"
                 "\tid: {}\n"
                 "\tnome: {}\n"
                 "\tnumero: {}\n"
                 "\tano: {}\n"
                 "\tdata de apresentação: {}\n"
                 "\tementa: {}\n"
                 "\texplicação da ementa: {}\n"
                 "\tqtde de autores: {}\n"
                 "\tind genero: {}\n"
                 "\tqtde orgaos com estado: {}\n")
        return texto.format(self.id_, self.nome, self.numero, self.ano,
                             self.data_apresentacao, self.ementa,
                             self.exp_ementa, self.qtde_autores,
                             self.ind_genero, self.qtd_orgaos_com_estado)


    def add_apensada(self, apensada):
        """Adiciona proposição apensada.
        A lista de apensadas é obtida no WS LP
        Args:
            apensada (nome_proposicao, cod_proposicao): proposição apensada.
        """
        self.apensadas.append(apensada)


    def set_tema(self, tema):
        """
        Seta o tema da proposição. Informação do WS PID.
        Args:
            tema (str): tema da proposição.
        """
        self.tema = tema


    def set_link_inteiro_teor(self, link):
        """
        Seta o link para o inteiro teor da proposição. Informação do WS PID.
        Args:
            link (str): link para o arquivo que contém o inteiro teor.
        """
        self.link_inteiro_teor = link


    def set_tipo_proposicao(self, tipo_proposicao):
        """
        Seta o tipo da proposição. Informação obtida nos WS LP e PID.
        Args:
            tipo_proposicao (TipoProposicao)
        """
        assert isinstance(tipo_proposicao, TipoProposicao),\
                'tipo_proposicao não é um TipoProposicao.'
        self.tipo_proposicao = tipo_proposicao


    def set_orgao_numerador(self, orgao_numerador):
        """
        Seta o órgão numerador. Informação obtida no WS LP.
        Args:
            orgao_numerador (OrgaoNumerador)
        """
        assert isinstance(orgao_numerador, OrgaoNumerador),\
                'orgao_numerador não é um OrgaoNumerador'
        self.orgao_numerador = orgao_numerador


    def set_regime(self, regime):
        """
        Seta o regime da proposição. Informação obtida no WS LP.
        Args:
            regime (Regime)
        """
        assert isinstance(regime, Regime),\
                'regime não é um Regime.'
        self.regime = regime


    def set_apreciacao(self, apreciacao):
        """
        Seta a apreciação da proposição. Informação obtida no WS LP.
        Args:
            apreciacao (Apreciacao)
        """
        assert isinstance(apreciacao, Apreciacao),\
                'apreciacao não é uma Apreciação.'
        self.apreciacao = apreciacao


    def set_autor1(self, autor1):
        """
        Seta o autor da proposição. Informação obtida no WS LP.
        Args:
            autor1 (Autor)
        """
        assert isinstance(autor1, Autor),\
                'autor1 não é um Autor.'
        self.autor1 = autor1


    def set_ultimo_despacho(self, ultimo_despacho):
        """
        Seta o último despacho da proposição. Informação obtida nos WS LP e PID.
        Args:
            ultimo_despacho (UltimoDespacho)
        """
        assert isinstance(ultimo_despacho, UltimoDespacho),\
                'ultimo_despacho não é um UltimoDespacho.'
        self.ultimo_despacho = ultimo_despacho


    def set_indexacao(self, indices):
        """
        Seta os índices relacionados a proposição. Informação obtida no WS PID.
        Args:
            indices (list): lista de palavras chave relacionadas a proposição.
        """
        self.indices = indices


    def set_situacao(self, situacao):
        """
        Seta a situação da proposição. Informação obtida no WS LP.
        Args:
            situacao (SituacaoProposicao)
        """
        self.situacao = situacao


