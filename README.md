# Aplicação de Análise de Loteria
## Descrição
### Esta aplicação Python, desenvolvida com Streamlit, Pandas e Plotly, tem como objetivo analisar o desempenho de combinações numéricas geradas por um algoritmo de inteligência artificial (IA) em relação aos resultados oficiais da Mega-Sena.

# Funcionalidades Principais:

- ###  `Carregamento de dados`: Permite o upload de arquivos CSV contendo os resultados oficiais da Mega-Sena e as combinações geradas pela IA.
- ###  Cálculo de acertos: Compara cada combinação gerada com todos os sorteios oficiais e calcula o número total de acertos.
- ###  Visualização de resultados:
- ###  Gráfico de distribuição de acertos: Apresenta a frequência de cada quantidade de acertos.
- ###  Gráfico de evolução da arrecadação: Mostra a variação da arrecadação total ao longo do tempo.
- ###  Simulador de prêmios: Permite ao usuário inserir uma combinação e simular os possíveis prêmios caso tivesse jogado.



# Tecnologias Utilizadas

- ###  Streamlit: Framework Python para criar aplicações web interativas.
- ###  Pandas: Biblioteca para manipulação e análise de dados.
- ###  Plotly: Biblioteca para criar visualizações interativas.


# Estrutura do Código

- ###  calculate_hits: Calcula o número de acertos entre as combinações geradas e os resultados oficiais.
- ###  plot_evolution: Cria um gráfico de linha mostrando a evolução da arrecadação total ao longo do tempo.
- ###  simulate_prizes: Simula os prêmios para uma combinação específica do usuário.
- ###  main: Função principal que controla a execução da aplicação, incluindo o carregamento de dados, a realização dos cálculos e a exibição dos resultados.


# Instruções de Uso
- ###  Clone o repositório:
```bash
git clone https://github.com/jvcss/loteria.git
```
Instale as dependências:
```bash
pip install -r requirements.txt
```
Execute a aplicação:
```bash
streamlit run loteria_app.py
```
- ### Carregue os arquivos CSV:
- ### Resultados Oficiais: Um arquivo CSV contendo os resultados oficiais da Mega-Sena, incluindo data do sorteio, números sorteados e valores dos prêmios.
- ### Resultados Gerados: Um arquivo CSV contendo as combinações numéricas geradas pela IA.

# Contribuições
- ### Contribuições são bem-vindas! Para contribuir, por favor, siga estas etapas:

Fork este repositório.
Crie um novo branch para sua feature.
Faça suas alterações e commit.
Envie um pull request.
Licença MIT
