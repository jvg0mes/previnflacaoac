# Métodos de Aprendizagem de Máquina aplicados a previsão da inflação

Projeto desenvolvido visando obter o titulo de especialista em Aprendizado de Máquina e Inteligência Artificial.
---------------------------------

O nível de preços afeta diretamente a vida de todos os agentes econômicos da sociedade, influenciando as decisões imediatas e também o planejamento futuro tanto nas relações de consumo quanto nas de investimento. De junho de 2018 a junho de 2022 o real perdeu cerca de 21% do seu poder de compra de acordo com o principal índice de preços do Brasil o Índice de Preços ao Consumidor Amplo (IPCA), de modo que para a população apresentar um padrão de consumo maior os reajustes salariais deveriam ter sido acima desse percentual, fato este que não ocorreu segundo o acompanhamento dos estudos do Departamento Intersindical de Estatística e Estudos Socioeconômicos (Dieese). Neste contexto, este trabalho tem como objetivo fazer um modelo que permita prever a variação do nível de preços acumulada para os próximos 3 meses, possibilitando a tomada de decisões de curto e médio prazo com maior segurança e contribuir na pesquisa de métodos de previsão dos níveis de inflação e os benefícios que suas soluções podem trazer ao governo, empresas e sociedade.

A coleta de dados foi feita principalmente em dois repositórios de fontes: o Sistema Gerenciador de Séries Temporais do Banco Central que será importado utilizando o pacote python-bcb e o IPEADATA que utilizará o ipeadatapy. Esses são alguns dos principais repositórios de dados referentes a economia brasileira. As cotações históricas dos preços dos mercados futuros de commodities e índices acionários serão importados do Yahoo Finance utilizando o pacote yfinance do Python 3.6. Para possibilitar a aplicação de métodos tradicionais de aprendizado de máquina a variável alvo será a variação da inflação acumulada nos próximos 3 meses, a variação mensal já é estacionaria levando em consideração os dados a partir de 2014, porém, considerando o objetivo do modelo e a compreensão do fenômeno, além da variação acumulada ser mais perceptível ela permite um planejamento mais próximo da realidade sendo mais resistente a choques temporários e também é estacionaria.

Devido a ideia inicial de utilizar uma base grande para mineração de dados a fim de possibilitar também a obtenção de relações não óbvias, após aplicar rotinas de geração de features nas variáveis como médias móveis e transformações quadráticas mesmo aplicando alguns filtros que garantem a integridade dos dados a base de dados resultante ainda é grande. Se a base fosse utilizada no estado atual as relações não óbvias ainda seriam captadas com algum nível de eficácia, entretanto, apenas captar essas relações não é o suficiente, é necessário também que elas sejam significativas. Por isso, adiantando uma etapa da preparação de dados para o modelo, foi calculada a matriz de correlação das variáveis dependentes com a variável independente e foram filtradas as variáveis que possuem correlação igual ou superior a 0.4, valor que sugere uma correlação ao menos moderada. A base final obtida para ser utilizada como insumo para os modelos de aprendizado de máquina ao final dessa etapa possui 89 linhas, 113 colunas e 10622 registros.

Observando o gráfico da variável alvo visualizamos os resquícios de estacionariedade que foram confirmados por meio dos testes de Dickey Fuller Aumentado utilizados durante o processamento dos dados. Também é notável a presença de picos, tornando necessária a checagem de existência de fator sazonal na série, como pode ser visto na Figura Inflação Acumulada em 3 Meses.

![image](https://user-images.githubusercontent.com/60692882/207216040-375448d0-c634-4b49-9d80-379146d32943.png)

Um fator importante do padrão de comportamento da variável é a sua variabilidade, na série obtida da inflação acumulada em três meses praticamente todos os registros se encontram em até dois desvios padrões da média, enquanto a maioria dos registros se encontram em até um desvio padrão de distância da média. Isso oferece indícios que a maior parte das previsões tendem a estar próximas a essa faixa de modo que em um cenário em que possuímos dois modelos, um de variabilidade maior e outro menor, o modelo com a variabilidade menor, se a médias das previsões for próxima a média da série, tende a apresentar melhores resultados.

![image](https://user-images.githubusercontent.com/60692882/207216090-566727cb-ba29-417a-b16f-c177ce456cd4.png)

Essa observação pode ser complementada com a análise dos quartis, onde nota-se que 50% dos dados estão em um intervalo dentro da faixa do primeiro desvio padrão. Ainda no gráfico de box-plot existe um indicativo de uma possível não existência de outliers na série, fato este que seria esperado, visto que por se tratar de uma variável de variação acumulada os outros tempos envolvidos durante o cálculo tendem a suavizar os outliers que ocorreram em um determinado período.

![image](https://user-images.githubusercontent.com/60692882/207216123-e5b60267-9fa2-494c-b649-6b35c72c859e.png)

Categorizando a variável alvo por níveis de acordo com os seus quartis a presença dos períodos de deflação e o efeito da eliminação dessess outliers torna-se mais perceptível. Somente com a visualização de um gráfico de histogramas já é notável um melhor balanceamento entre os níveis.
 
![image](https://user-images.githubusercontent.com/60692882/207216230-9016cfba-14eb-4f19-b2ca-6d86ff385441.png)

Plontando os dados ordenados em um scatter e observando a distância entre os pontos torna-se possível notar e eliminar outros outliers.

![image](https://user-images.githubusercontent.com/60692882/207216436-292b69e1-476b-4828-b4b0-cf5fc7754eec.png)

Para comparação de resultados três algoritmos distintos foram usados para criar os modelos. O algoritmo ElasticNet foi o ponto de partida e o modelo principal visto que permite maior interpretabilidade dos seus resultados é em tese mais simples que os demais modelos empregados, ele utiliza uma combinação de regularização L1 (Lasso) com regularização L2 (Ridge) sendo capaz de selecionar um grupo ótimo de variáveis quando as variáveis são altamente correlacionadas, fato este muito recorrente entre variáveis de natureza econômica. Os outros dois modelos que serviram de comparação aos resultados obtidos com o modelo ElasticNet foi um Modelo de Rede Neural Multilayer Perceptron (MLP) e o modelo de Gradient Boosting  CatBoost.

Os resultados obtidos com os modelos foram de uma capacidade de previsão da inflação com um erro médio de até 0.31. Dos modelos treinados o que apresentou melhor performance foi o Catboost que conseguiu não só se ajustar melhor aos dados como também captar as variáveis importantes com uma grande convergência aos modelos lineares estimados que possuem por natureza esta capacidade.
 
![image](https://user-images.githubusercontent.com/60692882/207216627-92e9347c-9e72-481b-8c4f-d09b1b1c184c.png)

Apesar do desempenho melhor, quando comparado o comportamento da série original com as séries previstas, o modelo de Rede Neural apesar de captar em magnitude incorreta o valor da série consegue exibir um comportamento mais semelhante, fato este que pode ser visto na figura Comparação valores observados com previstos pelo modelo. Entretanto, devido a não repetição deste feito no conjunto de treinamento leva-se a acreditar no fator sorte ter ocorrido durante a amostragem, não incorrendo na repetição em amostras maiores e previsões futuras.

![image](https://user-images.githubusercontent.com/60692882/207216657-0e7cf6a4-3226-4db6-a540-c8fbf8d0ebfd.png)

As variáveis mais importantes dos modelos interpretáveis (ElasticNet e CatBoost) em grande parte coincidiram com a teoria econômica e o efeito esperado, como pode ser observado na Tabela 5 - Divergência da Influência das Variáveis do Modelo ElasticNet e CatBoost.

![image](https://user-images.githubusercontent.com/60692882/207216867-e03b9304-ec13-4096-8c73-92bd9296a3fb.png)

O diferencial entre o resultado obtido com o ElasticNet foi a saída da variável Produção da lista e a inserção da Taxa de Juros, além de uma importância maior ao Consumo e uma redução da importância dos Gastos do Governo e da Renda. A série da taxa de juros neste caso foi suavizado poro médias móveis 3 vezes indicando um efeito acumulado de longo prazo, devido a relação existente entre taxa de juros e produção derivada do trade-off entre produzir e poupar levanta-se a hipótese da taxa de juros neste caso está representando o aumento da oferta ao longo do tempo quando ocorre uma redução na mesma e vice-versa no modelo CatBoost. Já no modelo ElasticNet estaria ocorrendo o contrário, a variável Produção estaria captando também o efeito da Taxa de Juros.

Algumas possíveis explicações podem ser cogitadas no caso de o Consumo possuir relação inversa com a inflação contrariando o pressuposto assumido. Devido as transformações que inferem um efeito de longo prazo, esta variável pode estar captando o efeito de outras variáveis omitidas no modelo que indicam um ciclo econômico favorável onde o consumo tende a se elevar e a inflação reduzir, mas, não existindo relação direta neste caso.
