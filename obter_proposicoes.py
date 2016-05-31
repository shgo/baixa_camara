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
Obtém proposições de lei consumindo os Web Services da Câmara.

Os dados são armazenados em classes e listas de classes definidas no arquivo
classes_proposicoes.py, e são salvos em arquivos pickle.

O conteúdo do inteiro teor de cada proposição não é processado aqui, já que não
é disponibilizado nos Web Services. No entanto, o arquivo obter_inteiro_teor.py
faz esse serviço, processando os documentos em formato .pdf e .doc.

A pasta doc também contém um diagrama de classes explicando os dados e relacio-
namentos.

Possíveis melhorias:
    * tratar erros de HTTP e fazer o script continuar a aquisição a partir do
      erro.
"""
__author__ = "Saullo Oliveira"
__copyright__ = "Copyright 2016"
__credits__ = ["Saullo Oliveira"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Saullo Oliveira"
__email__ = "shgo@dca.fee.unicamp.br"
__status__ = "Development"


import argparse
import os.path
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
import pickle as pkl
from classes_proposicoes import SiglaTipoProposicao
from classes_proposicoes import SituacaoProposicao
from classes_proposicoes import TipoAutor
from classes_proposicoes import Proposicao
from classes_proposicoes import TipoProposicao
from classes_proposicoes import OrgaoNumerador
from classes_proposicoes import Regime
from classes_proposicoes import Apreciacao
from classes_proposicoes import Autor
from classes_proposicoes import UltimoDespacho
from classes_proposicoes import Orgao


def obter_siglas_tipo():
    """
    Obtém as siglas dos tipos de proposição.
    """
    siglas_url = ("http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/"
                  "ListarSiglasTipoProposicao")
    if not os.path.isfile('down_files/prop_siglas.pkl'):
        siglas = []
        with urllib.request.urlopen(siglas_url) as res:
            data = ET.fromstring(res.read())
            for item in data:
                sigla = SiglaTipoProposicao(
                    item.get('tipoSigla'),
                    item.get('descricao'),
                    item.get('ativa'),
                    item.get('genero'))
                siglas.append(sigla)
        with open('down_files/prop_siglas.pkl', 'wb') as arq:
            pkl.dump(siglas, arq)
        return siglas
    else:
        with open('down_files/prop_siglas.pkl', 'rb') as arq:
            return pkl.load(arq)

def obter_situacoes():
    """Obtém a lista de situações para proposições."""
    situacoes_url = ("http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/"
                     "ListarSituacoesProposicao")
    if not os.path.isfile('down_files/prop_situacoes.pkl'):
        situacoes = []
        with urllib.request.urlopen(situacoes_url) as res:
            data = ET.fromstring(res.read())
            for item in data:
                situacao = SituacaoProposicao(
                    item.get('id'),
                    item.get('descricao'),
                    item.get('ativa'))
                situacoes.append(situacao)
        with open('down_files/prop_situacoes.pkl', 'wb') as arq:
            pkl.dump(situacoes, arq)
        return situacoes
    else:
        with open('down_files/prop_situacoes.pkl', 'rb') as arq:
            return pkl.load(arq)

def obter_tipos_autores():
    """Obtém a lista de tipos de autores das proposições."""
    tipos_url = ("http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/"
                 "ListarTiposAutores")
    if not os.path.isfile('down_files/prop_tipos_autores.pkl'):
        tipos = []
        with urllib.request.urlopen(tipos_url) as res:
            data = ET.fromstring(res.read())
            for item in data:
                tipo = TipoAutor(
                    item.get('id'),
                    item.get('descricao'))
                tipos.append(tipo)
        with open('down_files/prop_tipos_autores.pkl', 'wb') as arq:
            pkl.dump(tipos, arq)
        return tipos
    else:
        with open('down_files/prop_tipos_autores.pkl', 'rb') as arq:
            return pkl.load(arq)

def monta_proposicao(item):
    """
    Monta as proposições recuperadas em data.
    Args:
        item (ElementTree): ElementTree de uma proposição do xml da camara.
    Return:
        prop (Proposicao): proposição.
    """
    prop_det_url = ("http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/"
                    "ObterProposicaoPorID?%s")
    prop = Proposicao(
        item.find('id').text,
        item.find('nome').text,
        item.find('numero').text,
        item.find('ano').text,
        item.find('datApresentacao').text,
        item.find('txtEmenta').text,
        item.find('txtExplicacaoEmenta').text,
        item.find('qtdAutores').text,
        item.find('indGenero').text,
        item.find('qtdOrgaosComEstado').text)

    #setando o tipo de proposicao
    tipo_prop = item.find('tipoProposicao')
    prop.set_tipo_proposicao(TipoProposicao(
        tipo_prop.find('id').text,
        tipo_prop.find('sigla').text,
        tipo_prop.find('nome').text))

    #setando o orgao numerador
    orgao_num = item.find('orgaoNumerador')
    prop.set_orgao_numerador(OrgaoNumerador(
        orgao_num.find('id').text,
        orgao_num.find('sigla').text,
        orgao_num.find('nome').text))

    #setando o regime
    regime = item.find('regime')
    prop.set_regime(Regime(
        regime.find('codRegime').text,
        regime.find('txtRegime').text))

    #setando a apreciacao
    apre = item.find('apreciacao')
    prop.set_apreciacao(Apreciacao(
        apre.find('id').text,
        apre.find('txtApreciacao').text))

    #setando autor1
    autor1 = item.find('autor1')
    prop.set_autor1(Autor(
        autor1.find('txtNomeAutor').text,
        autor1.find('idecadastro').text,
        autor1.find('codPartido').text,
        autor1.find('txtSiglaPartido').text,
        autor1.find('txtSiglaUF').text))

    #setando o último despacho
    ult_des = item.find('ultimoDespacho')
    prop.set_ultimo_despacho(UltimoDespacho(
        ult_des.find('datDespacho').text,
        ult_des.find('txtDespacho').text))

    #setando situacao
    sit = item.find('situacao')
    sit_prop = SituacaoProposicao(sit.find('id').text,
                                  sit.find('descricao').text)
    org = sit.find('orgao')
    orgao = Orgao(org.find('codOrgaoEstado').text,
                  org.find('siglaOrgaoEstado').text)
    sit_prop.set_orgao(orgao)

    principal = sit.find('principal')
    princ = {
        'cod_prop_principal':
            principal.find('codProposicaoPrincipal').text,
        'prop_principal':
            principal.find('proposicaoPrincipal').text}
    sit_prop.set_prop_principal(princ)
    prop.set_situacao(sit_prop)

    params_det = urllib.parse.urlencode({'IdProp': prop.id_})
    with urllib.request.urlopen(prop_det_url % params_det) as res_d:
        detalhes = ET.fromstring(res_d.read())
        prop.set_tema(detalhes.find('tema').text)
        prop.set_indexacao(
            detalhes.find('Indexacao').text.split(','))
        prop.set_link_inteiro_teor(
            detalhes.find('LinkInteiroTeor').text)
        apensadas = detalhes.find('apensadas')
        for apensada in apensadas:
            apens = (apensada.find('nomeProposicao').text,\
                 apensada.find('codProposicao').text)
            prop.add_apensada(apens)

    return prop

def obter_proposicoes(sigla, anos, apensadas=False):
    """Obtém a lista de proposições que satisfaçam os argumentos.
    Args:
        sigla (str) - Padrão 'PL'
        anos (list) - Lista dos anos. Padrão [2011].
        apensadas (boolean) - Se deve ou não buscar as proposições apensadas.
        siglas (list) - lista dos tipos para buscas as proposições apensadas.
    """
    prop_url = ("http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/"
                "ListarProposicoes?numero=&datApresentacaoIni=&"
                "datApresentacaoFim=&idTipoAutor=&parteNomeAutor=&"
                "siglaPartidoAutor=&siglaUFAutor=&generoAutor=&"
                "codEstado=&codOrgaoEstado=&emTramitacao=&%s")
    for ano in anos:
        if not os.path.isfile('down_files/prop_props_{}_{}.pkl'.format(sigla,
                                                                       ano)):
            props = []
            numeros = []
            print('Obtendo proposições do tipo {} no ano {}'.format(sigla, ano))
            params = urllib.parse.urlencode({'sigla': sigla, 'ano': ano})
            with urllib.request.urlopen(prop_url % params) as res:
                data = ET.fromstring(res.read())
                for item in data:
                    prop = monta_proposicao(item)
                    props.append(prop)
                    numeros.append(prop.numero)
                    print('{} - {} {} (id: {})'.format(len(props),
                                                       prop.nome,
                                                       prop.ano,
                                                       prop.id_))
                    if apensadas and len(prop.apensadas) > 0:
                        apens = obter_apensadas(prop.apensadas, numeros)
                        for apen in apens:
                            props.append(apen)

            with open('down_files/prop_props_{}_{}_apens_{}.pkl'\
                    .format(sigla, ano, apensadas),
                      'wb') as arq:
                pkl.dump((props, numeros), arq)

def obter_apensadas(apensadas, numeros):
    """
    Método que obtem as proposições apensadas de prop.
    Args:
        apensadas (list): lista de apensadas para baixar.
        numeros (list): número das proposições que já foram baixadas.
    Return:
        props (list): lista das proposicoes apensadas de prop.
    """
    prop_url = ("http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/"
                "ListarProposicoes?datApresentacaoIni=&"
                "datApresentacaoFim=&idTipoAutor=&parteNomeAutor=&"
                "siglaPartidoAutor=&siglaUFAutor=&generoAutor=&"
                "codEstado=&codOrgaoEstado=&emTramitacao=&%s")
    props = []
    for nome, _ in apensadas:
        #recupera a sigla para a busca
        sigla = nome.split() #a sigla mesmo é o elemento 0
        numero = sigla[1][:sigla[1].find('/')] #tudo antes da /
        ano = sigla[1][-4:] #4 últimos dígitos

        #se a proposição já foi baixada, não baixar novamente
        if numero in numeros:
            continue
        params = urllib.parse.urlencode({'sigla': sigla[0],
                                         'numero': numero,
                                         'ano': ano})
        with urllib.request.urlopen(prop_url % params) as res:
            data = ET.fromstring(res.read())
            #se não retornou nada, continua
            if data.tag == 'erro':
                continue
            prop = monta_proposicao(data.find('proposicao'))
            props.append(prop)
            print('\tAPENSADA: {} - {} {} (id: {})'.format(len(props),
                                                           prop.nome,
                                                           prop.ano,
                                                           prop.id_))
    return props

def main():
    #tratando os argumentos da linha de comando
    parser = argparse.ArgumentParser(
        description="""Baixa proposições de lei do site da câmara dos
                    deputados e salva o resultado por ano.""",
        epilog="""Ex. de uso: para baixar todas as proposições de
               lei do tipo PL, entre 2011 e 2014:
               ./obter_proposicoes.py -anos 2011 2012 2013 2014 -t PL
               para baixar todas as PECs de 2016:
               ./obter_proposicoes.py -anos 2016 -t PEC
               para que as proposições apensadas sejam baixadas no mesmo arquivo
               do ano, basta adicionar -apensadas.""")
    parser.add_argument('-listar', type=str, nargs='*',
                        help="""lista informações complementares, como tipos de
                             proposição (tp), tipos de autores (ta), e situações
                             de proposições (sp). Se esse parâmetro for 
                             fornecido, nenhuma proposição será baixada.""")
    parser.add_argument('-anos', type=int, action='append', nargs='*',
                        help="""anos que deseja baixar as proposições.
                             Cada ano salva um arquivo.""")
    parser.add_argument('-tipos', type=str, nargs='*',
                        help="""indica os tipos de proposição a serem obtidos.
                             Os valores possíveis podem ser listados com o
                             argumento -l tp.""")
    parser.add_argument('-apensadas', action='store_true',
                        help="""indica se deve baixar as proposições apensadas
                             no mesmo arquivo do ano.""")
    args = vars(parser.parse_args())
    licensa = ("baixa_camara  Copyright (C) 2016  Saullo Oliveira\n"
               "This program comes with ABSOLUTELY NO WARRANTY;\n"
               "This is free software, and you are welcome to redistribute it\n"
               "under certain conditions; See COPYING file for more"
               "information.\n"
               "Type ENTER to continue...")
    print(licensa)
    input()
    #tratando a listagem de coisas
    if args['listar']:
        if 'tp' in args['listar'][0]:
            print('Listagem dos tipos de proposição e se estão ativos')
            for obj in obter_siglas_tipo():
                print('{} - {}'.format(obj.sigla, obj.ativa))
        elif 'ta'in args['listar'][0]:
            for obj in obter_tipos_autores():
                print('{} - {}'.format(obj.id_, obj.descricao))
        elif 'sp' in args['listar'][0]:
            for obj in obter_situacoes():
                print('{} - {}'.format(obj.id_, obj.descricao))
    #se não é pra listar, é pra baixar!
    else:
        for tp in args['tipos']:
            #verificando se a sigla é válida
            obter_proposicoes(sigla=tp, anos=args['anos'][0],
                              apensadas=args['apensadas'])
                              
if __name__ == '__main__':
    main()
