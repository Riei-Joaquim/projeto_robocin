# Projeto Robocin
Projeto do processo seletivo para o robocin 2018, voltado para a área de visão computacional, projetado no ambiente virtual de desenvolvemento Ipython

## Proposta desenvolvida no projeto:
(Desafio de video): foi usado a biblioteca open source Opencv para o tracker de robôs, em um trecho de uma competição na categoria very small size, a partir desse tracker se obteve uma aproximação da distancia de cada robô até a bola, e as velocidades dos objetos na cena. Esses dados são retornados para a main do código principal como uma lista que representa uma arvore enraizada na bola.


(Desafio de imagem): foi utilizado as bibliotecas open source scikit-learn e tensorflow para fazer o treinamento da rede neural pre treinada Inception, open source da google. Tendo como base um código que reconhece e diferencia flores, essa rede neural foi treinada para reconhecer o mascote do robocin impresso em 3d e a logo do robocin, além de diferenciar um do outro, treinamento baseado em fotos publicas do facebook. Uma vez treinada, essa rede foi usada como uma caixa preta por um código externo que usar opencv para mostrar ao usuário que fotos foram analisadas e qual a pontuação, emque o estimulo daquela foto produz na rede neural, para as duas saídas analisadas.
