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
Obtém dados dos deputados federais consumindo os Web Services da Câmara.

Os dados são armazenados em classes e listas de classes definidas no arquivo
classes_deputados.py, e são salvos em arquivos pickle.
"""
__author__ = "Saullo Oliveira"
__copyright__ = "Copyright 2016"
__credits__ = ["Saullo Oliveira"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Saullo Oliveira"
__email__ = "shgo@dca.fee.unincamp.br"
__status__ = "Development"


import argparse
import os.path
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
import pickle as pkl
from classes_deputados import Bloco
from classes_deputados import Partido
from classes_deputados import PartidoBloco
from classes_deputados import Deputado
from classes_deputados import Bancada
from classes_deputados import DeputadoLideranca
from classes_deputados import DetalhesDeputado
from classes_deputados import Gabinete
from classes_deputados import Comissao
from classes_deputados import CargoComissoes
from classes_deputados import PeriodoExercicio
from classes_deputados import FiliacaoPartidaria
from classes_deputados import HistoricoLider
from classes_deputados import HistoricoNome

def obter_partidos():
    """
    Obtém a lista de partidos pelo webservice da câmara.
    O resultado é salvo no arquivo partidos.pkl.
    """
    #1 - obter lista de partidos
    partido_url = ("http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/"
                   "ObterPartidosCD")
    if not os.path.isfile('down_files/partidos.pkl'):
        partidos = []
        with urllib.request.urlopen(partido_url) as res:
            data = ET.fromstring(res.read())
            for item in data:
                partido = Partido(item.find('idPartido').text,
                                  item.find('siglaPartido').text,
                                  item.find('nomePartido').text,
                                  item.find('dataCriacao').text,
                                  item.find('dataExtincao').text)
                partidos.append(partido)
        with open('down_files/partidos.pkl', 'wb') as arq:
            pkl.dump(partidos, arq)

def obter_partidos_blocos(num_legislatura=55):
    """
    Obtém os blocos de partidos a partir do webservice da câmara.
    O resultado é salvo no arquivo blocosPartido.pkl.
    Args:
        num_legislatura (int)
    """
    #2 - obter blocos e relacoes com partidos
    partidos_bloco_url = ("http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/"
                          "ObterPartidosBlocoCD?%s")

    params = urllib.parse.urlencode({
        'idBloco': '',
        'numLegislatura': num_legislatura})
    if not os.path.isfile('down_files/blocosPartido.pkl'):
        blocos = []
        with urllib.request.urlopen(partidos_bloco_url % params) as res:
            data = ET.fromstring(res.read())
            for item in data:
                bloco = Bloco(
                    item.find('idBloco').text,
                    item.find('nomeBloco').text,
                    item.find('siglaBloco').text,
                    item.find('dataCriacaoBloco').text,
                    item.find('dataExtincaoBloco').text)
                for ptd in item.find('Partidos'):
                    partido_bloco = PartidoBloco(
                        ptd.find('idPartido').text,
                        ptd.find('siglaPartido').text,
                        ptd.find('nomePartido').text,
                        ptd.find('dataAdesaoPartido').text,
                        ptd.find('dataDesligamentoPartido').text)
                    bloco.add_partido(partido_bloco)
                blocos.append(bloco)
        with open('down_files/blocos.pkl', 'wb') as arq:
            pkl.dump(blocos, arq)

def obter_bancadas():
    """
    Obtém as bancadas a partir do webservice da câmara.
    O resultado é salvo no arquivo bancadas.pkl.
    Args:
        num_legislatura (int)
    """
    bancadas_url = ("http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/"
                    "ObterLideresBancadas")
    if not os.path.isfile('down_files/bancadas.pkl'):
        bancadas = []
        with urllib.request.urlopen(bancadas_url) as res:
            data = ET.fromstring(res.read())
            for item in data:
                bancada = Bancada(item.get('sigla'), item.get('nome'))
                for child in item:
                    if child.tag == 'lider':
                        ldr = item.find('lider')
                        lider = DeputadoLideranca(ldr.find('nome').text,
                                                  ldr.find('ideCadastro').text,
                                                  ldr.find('partido').text,
                                                  ldr.find('uf').text)
                        bancada.set_lider(lider)
                    elif child.tag == 'vice_lider':
                        vice_lider = DeputadoLideranca(
                            child.find('nome').text,
                            child.find('ideCadastro').text,
                            child.find('partido').text,
                            child.find('uf').text)
                        bancada.add_vice_lider(vice_lider)
                    elif child.tag == 'representante':
                        repres = DeputadoLideranca(
                            child.find('nome').text,
                            child.find('ideCadastro').text,
                            child.find('partido').text,
                            child.find('uf').text)
                        bancada.add_representante(repres)
                    else:
                        print('erro de tag', child.tag, bancada.nome)
                        input()
                bancadas.append(bancada)
        with open('down_files/bancadas.pkl', 'wb') as arq:
            pkl.dump(bancadas, arq)

def obter_deputados(num_legislatura=55):
    """
    Obtém a lista de deputados com os detalhes a partir do webservice da camara.
    O resultado é salvo no arquivo deputados.pkl
    Args:
        num_legislatura (int)
    """
    deputado_url = ("http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/"
                    "ObterDeputados")
    deputados = []
    if not os.path.isfile('down_files/deputados.pkl'):
        with urllib.request.urlopen(deputado_url) as res:
            data = ET.fromstring(res.read())
            for item in data:
                deputado = Deputado(
                    item.find('ideCadastro').text,
                    item.find('condicao').text,
                    item.find('nome').text,
                    item.find('nomeParlamentar').text,
                    item.find('urlFoto').text,
                    item.find('sexo').text,
                    item.find('uf').text,
                    item.find('partido').text,
                    item.find('gabinete').text,
                    item.find('anexo').text,
                    item.find('fone').text,
                    item.find('email').text)
                ## comissoes está sempre vazio, portanto não será usado aqui.
                detalhes = obter_detalhes_deputado(deputado, num_legislatura)
                deputado.set_detalhes_deputado(detalhes)
                deputados.append(deputado)
                print('Deputado {} adicionado!'.format(deputado.nome))
        with open('down_files/deputados.pkl', 'wb') as arq:
            pkl.dump(deputados, arq)

def obter_detalhes_deputado(deputado, num_legislatura):
    """
    Método chamado a partir de obter_deputados, para cada deputado.
    Obtém os detalhes de um deputado a partir do webservice da camara.
    Args:
        deputado (Deputado): deputado a se buscar os detalhes
        num_legislatura (int)
    """
    assert isinstance(deputado, Deputado), \
            'deputado não é um Deputado'
    assert deputado.ide_cadastro, \
            'deputado não possui ide_cadastro'
    detalhes_url = ("http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/"
                    "ObterDetalhesDeputado?%s")
    params = urllib.parse.urlencode({
        'ideCadastro': deputado.ide_cadastro,
        'numLegislatura': num_legislatura})
    with urllib.request.urlopen(detalhes_url % params) as res:
        data = ET.fromstring(res.read())
        dep = data.find('Deputado')
        detalhes = DetalhesDeputado(
            dep.find('ideCadastro').text,
            dep.find('email').text,
            dep.find('nomeProfissao').text,
            dep.find('dataNascimento').text,
            dep.find('dataFalecimento').text,
            dep.find('ufRepresentacaoAtual').text,
            dep.find('situacaoNaLegislaturaAtual').text,
            dep.find('nomeParlamentarAtual').text,
            dep.find('nomeCivil').text,
            dep.find('sexo').text)
        #montando o partidoAtual
        pta = dep.find('partidoAtual')
        partido_atual = Partido(
            pta.find('idPartido').text,
            pta.find('sigla').text,
            pta.find('nome').text)
        detalhes.set_partido_atual(partido_atual)
        #montando os gabinetes
        for gbn in dep.findall('gabinete'):
            gabinete = Gabinete(
                gbn.find('numero').text,
                gbn.find('anexo').text,
                gbn.find('telefone').text)
            detalhes.add_gabinete(gabinete)
        #montando as comissoes que o deputado participa
        for comissao in dep.find('comissoes'):
            com = Comissao(
                comissao.find('idOrgaoLegislativoCD').text,
                comissao.find('siglaComissao').text,
                comissao.find('nomeComissao').text,
                comissao.find('condicaoMembro').text,
                comissao.find('dataEntrada').text,
                comissao.find('dataSaida').text)
            detalhes.add_comissao(com)
        #montando cargoComissoes
        cargos_comissoes = dep.find('cargosComissoes')
        for cargo in cargos_comissoes:
            cg_com = CargoComissoes(
                cargo.find('idOrgaoLegislativoCD').text,
                cargo.find('siglaComissao').text,
                cargo.find('nomeComissao').text,
                cargo.find('idCargo').text,
                cargo.find('nomeCargo').text,
                cargo.find('dataEntrada').text,
                cargo.find('dataSaida').text)
            detalhes.add_cargo_comissoes(cg_com)
        #montando periodosExercicio
        periodos_exercicio = dep.find('periodosExercicio')
        for periodo in periodos_exercicio:
            per = PeriodoExercicio(
                periodo.find('siglaUFRepresentacao').text,
                periodo.find('situacaoExercicio').text,
                periodo.find('dataInicio').text,
                periodo.find('dataFim').text,
                periodo.find('idCausaFimExercicio').text,
                periodo.find('descricaoCausaFimExercicio').text,
                periodo.find('idCadastroParlamentarAnterior').text)
            detalhes.add_periodo_exercicio(per)
        #montando historicoNomeParlamentar
        historico_nome = dep.find('historicoNomeParlamentar')
        for nome in historico_nome:
            print('Temos um historico nome parlamentar para o deputado {}'\
                    .format(deputado.ide_cadastro))
            hnome = HistoricoNome(
                nome.find('nomeParlamentarAnterior').text,
                nome.find('nomeParlamentaPosterior').text,
                nome.find('dataInicioVigenciaNomePosterior').text)
            detalhes.add_historico_nome_parlamentar(hnome)
        #montando filiacoesPartidarias
        filiacoes = dep.find('filiacoesPartidarias')
        for filiacao in filiacoes:
            fil = FiliacaoPartidaria(
                filiacao.find('idPartidoAnterior').text,
                filiacao.find('siglaPartidoAnterior').text,
                filiacao.find('nomePartidoAnterior').text,
                filiacao.find('idPartidoPosterior').text,
                filiacao.find('siglaPartidoPosterior').text,
                filiacao.find('nomePartidoPosterior').text,
                filiacao.find('dataFiliacaoPartidoPosterior').text)
            detalhes.add_filiacoes_partidarias(fil)
        #montando historicoLideranca
        historico_lider = dep.find('historicoLider')
        for lider in historico_lider:
            lid = HistoricoLider(
                lider.find('idHistoricoLider').text,
                lider.find('idCargoLideranca').text,
                lider.find('descricaoCargoLideranca').text,
                lider.find('numOrdemCargo').text,
                lider.find('dataDesignacao').text,
                lider.find('dataTermino').text,
                lider.find('codigoUnidadeLideranca').text,
                lider.find('siglaUnidadeLideranca').text,
                lider.find('idBlocoPartido').text)
            detalhes.add_historico_lider(lid)
        return detalhes

def main():
    #tratando os argumentos da linha de comando
    parser = argparse.ArgumentParser(
            description="""Baixa deputados do site da câmara dos deputados e
                        salva o resultado em arquivos pickle.""",
            epilog="""Ex. de uso: ...""")
    parser.add_argument('-d', type=str, nargs='*',
                        help="""baixa dados da câmara relacionados a deputados.
                             As opções são:
                             \tp - partidos
                             \tb - blocos
                             \tba - bancadas
                             \td - deputados com seus detalhes. Nesse caso,
                             \t\tpassar o argumento -n.
                             """,
                        choices=['p', 'b', 'ba', 'd'])
    parser.add_argument('-n', type=int, nargs='*',
                        help=""" indica a legislatura que os dados de deputados
                             devem ser baixados.""")
    args = vars(parser.parse_args())
    licensa = ("baixa_camara  Copyright (C) 2016  Saullo Oliveira\n"
               "This program comes with ABSOLUTELY NO WARRANTY;\n"
               "This is free software, and you are welcome to redistribute it\n"
               "under certain conditions; See COPYING file for more"
               "information.\n"
               "Type ENTER to continue...")
    print(licensa)
    input()
    if args['d']:
        if 'p' in args['d']:
            print('obtendo partidos')
            obter_partidos()
        if 'b' in args['d']:
            print('obtendo blocos')
            obter_partidos_blocos()
        if 'ba' in args['d']:
            print('obtendo bancadas')
            obter_bancadas()
        if 'd' in args['d']:
            if not args['n']:
                print('Legislatura não informada. Use o parametro -n.')
            print('obtendo deputados')
            obter_deputados(args['n'])

if __name__ == '__main__':
    main()
