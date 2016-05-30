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
Percorre as proposições já armazenadas, obter o inteiro teor de cada uma e
processa o texto.
"""
__author__ = "Saullo Oliveira"
__copyright__ = "Copyright 2016"
__credits__ = ["Saullo Oliveira"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Saullo Oliveira"
__email__ = "shgo@dca.fee.unincamp.br"
__status__ = "Development"

from io import StringIO
import os.path
import argparse
import pickle as pkl
import urllib.request
import urllib.parse
import logging
import re
import magic
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from docx import Document


def get_inteiro_teor(prop):
    """
    Obtém o conteúdo do inteiro teor de prop, e já tokeniza.
    Args:
        prop (Proposicao)
    """
    print('{}\tObtendo inteiro teor da proposição {}'.format(
        prop.ano, prop.id_))
    print(prop.link_inteiro_teor)
    #se o inteiro teor já foi coletado, não faz nada
    if hasattr(prop, 'inteiro_teor'):
        return prop

    #caso não tenha link do inteiro teor
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not regex.match(prop.link_inteiro_teor):
        logging.warning('MISSING - %s não tem link para inteiro teor.\n',
                        prop.id_)
        return prop

    arquivo = urllib.request.urlretrieve(prop.link_inteiro_teor)
    with open(arquivo[0], 'rb') as arq:
        cabecalho = magic.from_file(arquivo[0])
        texto = ''
        try:
            if cabecalho.startswith(b'PDF'):
                parser = PDFParser(arq)
                doc = PDFDocument()
                parser.set_document(doc)
                doc.set_parser(parser)
                doc.initialize()
                rsrcmgr = PDFResourceManager()
                output = StringIO()
                converter = TextConverter(rsrcmgr, output, laparams=LAParams())
                interpreter = PDFPageInterpreter(rsrcmgr, converter)
                print('\t\tprocessando páginas')
                for page in doc.get_pages():
                    interpreter.process_page(page)
                texto = output.getvalue()
            elif cabecalho.startswith(b'Com'):
                document = Document(arq)
                print('\t\tprocessando paragrafos')
                for paragraph in document:
                    texto += paragraph.text
            else:
                raise Exception('Formato desconhecido')
            print('\t\ttokenizando')
            prop.inteiro_teor = re.split(r'\W+', texto)
        except:
            logging.warning('CORRUPT: %s arquivo corrupto! Oferecer dinheiro!',
                            prop.id_)
            logging.warning(prop.link_inteiro_teor)
            nome = 'inteiro_teor/inteiro_teor_{}.doc'.format(prop.id_)
            with open(nome, 'wb') as salvar:
                salvar.write(arq.read())
            logging.warning('arquivo salvo em %s\n', nome)
    return prop

def main():
    #tratando os argumentos da linha de comando
    parser = argparse.ArgumentParser(
            description="""Baixa e processa os arquivos com inteiro teor para
                        cada proposição de lei no arquivo correspondente aos
                        parâmtros. As proposições que não forem processadas por
                        qualquer motivo (arquivo corrupto (hahaha), ou sem link)
                        estarão listadas no log, e os arquivos se corruptos,
                        serão baixados para a pasta inteiro_teor.""",
            epilog="""Ex. de uso: para baixar o inteiro teor do arquivo
                   down_files/prop_props_PL_2016_apens_True.pkl:
                   ./obter_inteiro_teor.py -anos 2016 -tipos PL -apensadas""")
    parser.add_argument('-anos', type=int, action='append', nargs='*',
                        help="""anos das proposições já baixadas sem inteiro
                             teor.""")
    parser.add_argument('-tipos', type=str, nargs='*',
            help="""tipos de proposição já baixadas sem inteiro teor.""")
    parser.add_argument('-apensadas', action='store_true',
                        help="""indica se o arquivo das proposições já baixadas
                             contém apensadas ou não. Útil para encontrar o
                             arquivo correto.""")
    args = vars(parser.parse_args())
    licensa = ("baixa_camara  Copyright (C) 2016  Saullo Oliveira\n"
               "This program comes with ABSOLUTELY NO WARRANTY;\n"
               "This is free software, and you are welcome to redistribute it\n"
               "under certain conditions; See COPYING file for more"
               "information.\n"
               "Type ENTER to continue...")
    print(licensa)
    input()
    apens = args['apensadas']
    for tp in args['tipos']:
        for ano in args['anos'][0]:
            print('Tipo {} ano {}.'.format(tp, ano))
            logging.basicConfig(filename="logs/warnings_{}_{}.log".format(tp,
                                                                          ano),
                                level=logging.WARNING)
            if os.path.isfile('down_files/prop_props_{}_{}_apens{}.pkl'\
                    .format(tp, ano, apens)):
                with open('down_files/prop_props_{}_{}_apens_{}.pkl'\
                         .format(tp, ano, apens), 'rb')\
                        as arq_prop:
                    print('Processando {}-{}'.format(tp, ano))
                    props = pkl.load(arq_prop)
                    props = [get_inteiro_teor(prop) for prop in props]
                with open('down_files/prop_props_{}_{}_apens_{}.pkl'\
                        .format(tp, ano, apens), 'wb')\
                        as arq_prop:
                    print('Salvando {}-{}'.format(tp, ano))
                    pkl.dump(props, arq_prop)
            else:
                print(("\tarquivo não encontrado. Você já rodou o script "
                       "obter_proposicoes.py?"))

if __name__ == '__main__':
    main()
