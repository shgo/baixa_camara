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
Classes relacionadas a obtenção dos Deputados a partir dos Web Services da
Câmara dos Deputados.

A documentação oficial da câmara nem sempre corresponde ao xml resultante das
chamadas. Então, verifique a documentação de cada método.
"""
__author__ = "Saullo Oliveira"
__copyright__ = "Copyright 2016"
__credits__ = ["Saullo Oliveira"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Saullo Oliveira"
__email__ = "shgo@dca.fee.unicamp.br"
__status__ = "Development"


class Bloco:
    """
    Bloco de partidos. No site da câmara essa classe é representada por
    ObterPartidosBlocoCD.
    """
    def __init__(self, id_bloco, nome_bloco, sigla_bloco, data_criacao_bloco,
                 data_extincao_bloco):
        """Método construtor do bloco.
        Args:
            id_bloco (int): ID do bloco.
            nome_bloco (str): Nome do bloco. Ex.: PV, PPS.
            sigla_bloco (str): Sigla do bloco.
            data_criacao_bloco (str): Data de criação do bloco.
            data_extincao_bloco (str): Data de extinção do bloco.
        """
        self.id_bloco = id_bloco
        self.nome_bloco = nome_bloco
        self.sigla_bloco = sigla_bloco
        self.data_criacao_bloco = data_criacao_bloco
        self.data_extincao_bloco = data_extincao_bloco
        self.partidos = []

    def __str__(self):
        """
        Formata a impressão do objeto quando print(self) é invocado.
        """
        text = "{} - {} - (sigla: {}). Criado em {}, extinto em {}.\n"\
                .format(self.id_bloco,
                        self.nome_bloco,
                        self.sigla_bloco,
                        self.data_criacao_bloco,
                        self.data_extincao_bloco)
        text += "O bloco contém {} partidos:\n".format(len(self.partidos))
        for partido in self.partidos:
            text += "\t{}\n".format(partido.sigla_partido)
        return text


    def add_partido(self, partido_bloco):
        """Método que adiciona um partido ao bloco.
        Args:
            partido_bloco (PartidoBloco)
        """
        assert isinstance(partido_bloco, PartidoBloco), \
                'partido_bloco não é um PartidoBloco.'
        self.partidos.append(partido_bloco)


class PartidoBloco():
    """
    Partido que participa de um bloco.
    
    No site da câmara é representado por listaPartido. Essa classe sempre será
    usada como atributo de Bloco.
    """


    def __init__(self, id_partido, sigla_partido, nome_partido,
                 data_adesao_partido, data_desligamento_partido):
        """Método construtor do PartidoBloco.
        Args:
            id_partido (str): id do partido.
            sigla_partido (str): sigla do partido.
            nome_partido (str): nome do partido.
            data_adesao_partido (str): data de adesão do partido nesse bloco.
            data_desligamento_partido (str): data de desligamento do partido
                desse bloco.
        """
        self.id_partido = id_partido
        self.sigla_partido = sigla_partido
        self.nome_partido = nome_partido
        self.data_adesao_partido = data_adesao_partido
        self.data_desligamento_partido = data_desligamento_partido


class Partido:
    """
    Partido com representação na Câmara dos Deputados.
    """


    def __init__(self, id_partido, sigla_partido, nome_partido,\
                 data_criacao=None,\
                 data_extincao=None):
        """Método construtor do partido.
        Args:
            id_partido (str): ID do partido. Ex.: PT.
            sigla_partido (str): sigla do partido.
            nome_partido (str): nome do partido por extenso.
            data_criacao (str): data de criação do partido.
            data_extincao (str): data de extinção do partido.
        """
        self.id_partido = id_partido #local da instancia
        self.sigla_partido = sigla_partido
        self.nome_partido = nome_partido
        self.data_criacao = data_criacao
        self.data_extincao = data_extincao


    def __str__(self):
        """
        Formata a impressão do objeto quando print(self) é invocado.
        """
        return "{} - {}\nCriado em {} e extinto em {}. O id do Partido é {}."\
            .format(self.sigla_partido,
                    self.nome_partido,
                    self.data_criacao,
                    self.data_extincao,
                    self.id_partido)


class DeputadoLideranca:
    """
    Classe que sempre será atributo da classe Bancada.
    """

    def __init__(self, nome, ide_cadastro, partido, uf):
        """
        Método construtor.
        Args:
            nome (str)
            ide_cadastro (str)
            partido (str)
            uf (str)
        """
        self.nome = nome
        self.ide_cadastro = ide_cadastro
        self.partido = partido
        self.uf = uf


class Bancada:
    """
    No site da câmara essa classe é representada por ObterLideresBancadas.
    É a única classe que deixei diferente do que esta lá no xml.
    """


    def __init__(self, sigla, nome):
        """
        Método construtor.
        Args:
            sigla (str)
            nome (str)
        """
        self.sigla = sigla
        self.nome = nome
        self.lider = None
        self.vice_lideres = []
        self.representantes = []


    def set_lider(self, lider):
        """Método que seta o lider da Bancada.
        Args:
            lider (DeputadoLideranca)
        """
        assert isinstance(lider, DeputadoLideranca),\
                'lider não é um DeputadoLideranca'
        self.lider = lider
    def add_vice_lider(self, vice_lider):
        """
        Método que adiciona um vice-lider à Bancada.
        Args:
            vice_lider (DeputadoLideranca)
        """
        assert isinstance(vice_lider, DeputadoLideranca), \
                'viceLider não é um DeputadoLideranca'
        self.vice_lideres.append(vice_lider)


    def add_representante(self, representante):
        """
        Adiciona um representante da bancada
        Args:
            representante (DeputadoLideranca)
        """
        assert isinstance(representante, DeputadoLideranca), \
                'representante não é um DeputadoLideranca'
        self.representantes.append(representante)


class Comissao:
    """Comissão que um deputado participa.
    
    Sempre estará como objeto em DetalhesDeputado.
    """
    def __init__(self, id_orgao_legislativo_cd, sigla_comissao, nome_comissao,
                 condicao_membro, data_entrada, data_saida):
        """
        Args:
            id_orgao_legislativo_cd (str)
            sigla_comissao (str)
            nome_comissao (str)
            condicao_membro (str)
            data_entrada (str)
            data_saida (str)
        """
        self.id_orgao_legislativo_cd = id_orgao_legislativo_cd
        self.sigla_comissao = sigla_comissao
        self.nome_comissao = nome_comissao
        self.condicao_membro = condicao_membro
        self.data_entrada = data_entrada
        self.data_saida = data_saida


class Comissoes:
    """Classe que armazena a lista de comissões que o deputado participa como
    titular e como suplente.

    Sempre será objeto da classe Deputado.
    """
    def __init__(self):
        """
        Construtor vazio.
        """
        self.titular = []
        self.suplente = []


    def add_titular(self, comissao):
        """Adiciona uma comissão na lista de comissões que o deputado
        participou como titular.
        Args:
            comissao (Comissao): objeto Comissao que o deputado foi titular.
        """
        assert isinstance(comissao, Comissao), \
                'comissao não é da classe Comissao'
        self.titular.append(comissao)


    def add_suplente(self, comissao):
        """Adiciona uma comissão na lista de comissões que o deputado
        participou como suplente.
        Args:
            comissao (Comissao): objeto Comissao que o deputado foi suplente.
        """
        assert isinstance(comissao, Comissao), \
                'comissao não é da classe Comissão'
        self.suplente.append(comissao)


class Deputado():
    """Representa um deputado.
    
    A maior parte dos detalhes não está nessa classe, mas no atributo
    detalhes_deputado. Essa modelagem foi uma escolha para representar os dados
    da forma mais semelhante possível à estrutura dos Web Services.
    """
    def __init__(self, ide_cadastro, condicao, nome, nome_parlamentar,
                 url_foto, sexo, uf, partido, gabinete, anexo, fone, email):
        """
        Args:
            ide_cadastro (str)
            condicao (str)
            nome (str)
            nome_parlamentar (str)
            url_foto (str)
            sexo (str)
            uf (str)
            partido (str)
            gabinete (str)
            anexo (str)
            fone (str)
            email (str)
            situacao_na_legislatura_atual (str)
        """
        self.ide_cadastro = ide_cadastro
        self.condicao = condicao
        self.nome = nome
        self.nome_parlamentar = nome_parlamentar
        self.url_foto = url_foto
        self.sexo = sexo
        self.uf = uf
        self.partido = partido
        self.gabinete = gabinete
        self.anexo = anexo
        self.fone = fone
        self.email = email
        self.comissoes = []
        self.detalhes_deputado = None


    def add_comissao(self, comissoes):
        """lista de comissões que esse deputado participa
        Args:
            comissoes (Comissoes)
        """
        assert isinstance(comissoes, Comissoes),\
               'comissoes não é um Comissoes'
        self.comissoes.append(comissoes)


    def set_detalhes_deputado(self, detalhes_deputado):
        """detalhes do deputado.
        Args:
            detalhes_deputado (DetalhesDeputado)
        """
        assert isinstance(detalhes_deputado, DetalhesDeputado),\
                'detalhes_deputado não é um DetalhesDeputado.'
        self.detalhes_deputado = detalhes_deputado


class FiliacaoPartidaria:
    """Classe que armazena uma troca de filiação partidária.

    Sempre será atributo de DetalhesDeputado.
    """
    def __init__(self, id_partido_anterior, sigla_partido_anterior,
                 nome_partido_anterior, id_partido_posterior,
                 sigla_partido_posterior, nome_partido_posterior,
                 data_filiacao_partido_posterior):
        """
        Args:
            id_partido_anterior (str)
            sigla_partido_anterior (str)
            nome_partido_anterior (str)
            id_partido_posterior (str)
            sigla_partido_posterior (str)
            nome_partido_posterior (str)
            data_filiacao_partido_posterior (str)
        """
        self.id_partido_anterior = id_partido_anterior
        self.sigla_partido_anterior = sigla_partido_anterior
        self.nome_partido_anterior = nome_partido_anterior
        self.id_partido_posterior = id_partido_posterior
        self.sigla_partido_posterior = sigla_partido_posterior
        self.nome_partido_posterior = nome_partido_posterior
        self.data_filiacao_partido_posterior = data_filiacao_partido_posterior


class Gabinete:
    """
    Classe que representa um Gabinete Parlamentar.

    Ela sempre será atribute de um DetalhesDeputado.
    """
    def __init__(self, numero, anexo, telefone):
        """
        Método construtor.
        Args:
            numero (str)
            anexo (str)
            telefone (str)
        """
        self.numero = numero
        self.anexo = anexo
        self.telefone = telefone


class PeriodoExercicio:
    """
    Classe que representa um período de exercício do Deputado.
    """


    def __init__(self, sigla_uf_representacao, situacao_exercicio, data_inicio,
                 data_fim, id_causa_fim_exercicio, descricao_causa_fim_exercicio,
                 id_cadastro_parlamentar_anterior):
        """
        Args:
            sigla_uf_representacao (str)
            situacao_exercicio (str)
            data_inicio (str)
            data_fim (str)
            id_causa_fim_exercicio (str)
            descricao_causa_fim_exercicio (str)
            id_cadastro_parlamentar_anterior (str)
        """
        self.sigla_uf_representacao = sigla_uf_representacao
        self.situacao_exercicio = situacao_exercicio
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.id_causa_fim_exercicio = id_causa_fim_exercicio
        self.descricao_causa_fim_exercicio = descricao_causa_fim_exercicio
        self.id_cadastro_parlamentar_anterior = id_cadastro_parlamentar_anterior


class CargoComissoes:
    """Classe que representa o cargo de um deputado numa comissão."""


    def __init__(self, id_orgao_legislativo_cd, sigla_comissao, nome_comissao,
                 id_cargo, nome_cargo, data_entrada, data_saida):
        """
        Args:
            id_orgao_legislativo_cd (str)
            sigla_comissao (str)
            nome_comissao (str)
            id_cargo (str)
            nome_cargo (str)
            data_entrada (str)
            data_saida (str)
        """
        self.id_orgao_legislativo_cd = id_orgao_legislativo_cd
        self.sigla_comissao = sigla_comissao
        self.nome_comissao = nome_comissao
        self.id_cargo = id_cargo
        self.nome_cargo = nome_cargo
        self.data_entrada = data_entrada
        self.data_saida = data_saida


class HistoricoLider:
    """Armazena uma liderança que o deputado foi num mandato.

    Sempre será atributo na classe DetalhesDeputado.
    """


    def __init__(self,
                 id_historico_lider,
                 id_cargo_lideranca,
                 descricao_cargo_lideranca,
                 num_ordem_cargo,
                 data_designacao,
                 data_termino,
                 codigo_unidade_lideranca,
                 sigla_unidade_lideranca,
                 id_bloco_partidario):
        """
        Args:
            id_historico_lider (str)
            id_cargo_lideranca (str)
            descricao_cargo_lideranca (str)
            num_ordem_cargo (str)
            data_designacao (str)
            data_termino (str)
            codigo_unidade_lideranca (str)
            sigla_unidade_lideranca (str)
            id_bloco_partidario (str)
        """
        self.id_historico_lider = id_historico_lider
        self.id_cargo_lideranca = id_cargo_lideranca
        self.descricao_cargo_lideranca = descricao_cargo_lideranca
        self.num_ordem_cargo = num_ordem_cargo
        self.data_designacao = data_designacao
        self.data_termino = data_termino
        self.codigo_unidade_lideranca = codigo_unidade_lideranca
        self.sigla_unidade_lideranca = sigla_unidade_lideranca
        self.id_bloco_partidario = id_bloco_partidario


class DetalhesDeputado:
    """
    Classe que contém diversos detalhes dos deputados.

    Sempre será atributo de um Deputado.
    """


    def __init__(self, ide_cadastro, email, nome_profissao, data_nascimento,
                 data_falecimento, uf_representacao_atual,
                 situacao_na_legislatura_atual, nome_parlamentar_atual,
                 nome_civil, sexo):
        """
        Método construtor.
        Args:
            ide_cadastro (str)
            email (str)
            nome_profissao (str)
            data_nascimento (str)
            data_falecimento (str)
            uf_representacao_atual (str)
            situacao_na_legislatura_atual (str)
            nome_parlamentar_atual (str)
            nome_civil (str)
            sexo (str)
        """
        self.ide_cadastro = ide_cadastro
        self.email = email
        self.nome_profissao = nome_profissao
        self.data_nascimento = data_nascimento
        self.data_falecimento = data_falecimento
        self.uf_representacao_atual = uf_representacao_atual
        self.situacao_na_legislatura_atual = situacao_na_legislatura_atual
        self.nome_parlamentar_atual = nome_parlamentar_atual
        self.nome_civil = nome_civil
        self.sexo = sexo
        self.partido_atual = None
        self.gabinete = []
        self.comissoes = []
        self.cargo_comissoes = []
        self.periodos_exercicio = []
        self.historico_nome_parlamentar = []
        self.filiacoes_partidarias = []
        self.historico_lider = []


    def set_partido_atual(self, partido):
        """
        Configura o partido atual do objeto.
        Args:
            partido (Partido)
        """
        assert isinstance(partido, Partido), \
                'partido não é um Partido.'
        self.partido_atual = partido


    def add_gabinete(self, gabinete):
        """
        Adiciona um gabinete ao deputado.
        Args:
            gabinete (Gabinete)
        """
        assert isinstance(gabinete, Gabinete), 'gabinete não é um Gabinete.'
        self.gabinete.append(gabinete)


    def add_comissao(self, comissao):
        """
        Adiciona uma comissao aos detalhes do deputado.
        Args:
            comissao (Comissao)
        """
        assert isinstance(comissao, Comissao),\
                'comissao não é uma Comissao.'
        self.comissoes.append(comissao)


    def add_cargo_comissoes(self, cargo_comissoes):
        """
        Adiciona um cargo em comissão ao deputado.
        Args:
            cargo_comissoes (cargo_comissoes)
        """
        assert isinstance(cargo_comissoes, CargoComissoes),\
               'cargo_comissoes não é um CargoCommissoes'
        self.cargo_comissoes.append(cargo_comissoes)


    def add_periodo_exercicio(self, periodo_exercicio):
        """
        Adiciona um Periodo de Exercício parlamentar ao Deputado.
        Args:
            periodoExercicio (PeriodoExercicio)
        """
        assert isinstance(periodo_exercicio, PeriodoExercicio),\
               'periodo_exercicio não é um PeriodoExercicio'
        self.periodos_exercicio.append(periodo_exercicio)


    def add_historico_nome_parlamentar(self, nome_parlamentar):
        """
        Adiciona um nome parlamentar ao histórico do rato.
        Args:
            nome_parlamentar (str)
        """
        assert isinstance(nome_parlamentar, HistoricoNome),\
                'nome_parlamentar não é um HistoricoNome'
        self.historico_nome_parlamentar.append(nome_parlamentar)


    def add_filiacoes_partidarias(self, filiacao_partidaria):
        """
        Adiciona uma filiação partidária ao deputado.
        Args:
            filiacao_partidaria (FiliacaoPartidaria)
        """
        assert isinstance(filiacao_partidaria, FiliacaoPartidaria),\
                'filiacao_partidaria não é uma FiliacaoPartidaria.'
        self.filiacoes_partidarias.append(filiacao_partidaria)


    def add_historico_lider(self, historico_lider):
        """
        Adiciona uma liderança ao histórico do deputado.
        Args:
            historico_lider (HistoricoLider)
        """
        assert isinstance(historico_lider, HistoricoLider),\
                'historico_lider não é um HistoricoLider.'
        self.historico_lider.append(historico_lider)


class HistoricoNome:
    """
    Classe que armazena a troca de nome parlamentar.

    Sempre será parte de atributo em DetalhesDeputado.
    """


    def __init__(self, nome_parlamentar_anterior, nome_parlamentar_posterior,
                 data_inicio_vigencia_nome_posterior):
        """
        Método construtor.
        Args:
            nome_parlamentar_anterior (str)
            nome_parlamentar_posterior (str)
            data_inicio_vigencia_nome_posterior (str)
        """
        self.nome_parlamentar_anterior = nome_parlamentar_anterior
        self.nome_parlamentar_posterior = nome_parlamentar_posterior
        self.data_inicio_vigencia_nome_posterior =\
                data_inicio_vigencia_nome_posterior


    def __str__(self):
        """
        Formata a impressão do objeto quando print(self) é invocado.
        """
        return "{} -> {} em {}".format(self.nome_parlamentar_anterior,
                                       self.nome_parlamentar_posterior,
                                       self.data_inicio_vigencia_nome_posterior)

