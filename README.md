# baixa_camara
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fshgo%2Fbaixa_camara.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fshgo%2Fbaixa_camara?ref=badge_shield)

Código python que baixa os dados dos Web Services da Câmara dos Deputados.

Descrição dos arquivos e pastas:
- documentacao/ - contém os diagramas de classe e qualquer outra documentação que ajude a entender a estrutura do código.
- inteiro_teor/ - só é criada quando os arquivos com inteiro teor das proposições estão corruptos e não aceitam pouco dinheiro.
- down_files/ - guarda todos os arquivos baixados por qualquer script.
- logs/ - auto-descritiva.
- classes_deputados.py - contém as definições de classes para baixar os dados nesses [Web Services](http://www2.camara.leg.br/transparencia/dados-abertos/dados-abertos-legislativo/webservices/deputados).
- classes_proposicoes.py - contém as definições de classes para baixar proposições de lei, sem as votações, nesses [Web Services](http://www2.camara.leg.br/transparencia/dados-abertos/dados-abertos-legislativo/webservices/proposicoes-1)
- COPYING - arquivo com a licença GPLv3.
- obter_deputados.py - script que baixa dados dos deputados.
- obter_inteiro_teor.py - script que baixa e processa o inteiro teor de proposições já baixadas.
- obter_proposicoes.py - script que baixa as porposições de lei.

# Como usar#
Se você deseja baixar informações sobre os deputados, basta executar o comando `./obter_deputados.py -h` para ver a ajuda desse script.

Se você deseja baixar informações sobre as proposições de lei, basta executar o comando `./obter_proposicoes.py -h` para ver a ajuda desse script.

Se você *já baixou* as proposições e deseja obter o inteiro teor de cada uma, basta executar o comando `./obter_inteiro_teor.py -h` para ver a ajuda desse script.


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fshgo%2Fbaixa_camara.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fshgo%2Fbaixa_camara?ref=badge_large)