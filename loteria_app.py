import streamlit as st
import pandas as pd
import plotly.express as px

def calculate_hits(official_df, generated_df):
    """Calcula o número de acertos entre os números gerados pela IA e os resultados oficiais.

    Args:
        official_df (pd.DataFrame): DataFrame com os resultados oficiais da Mega-Sena.
        generated_df (pd.DataFrame): DataFrame com os números gerados pela IA.

    Returns:
        pd.DataFrame: DataFrame com as combinações geradas, o número de acertos e outros dados relevantes.
    """

    # Assumindo que 'generated_df' contém apenas as colunas com os números gerados
    generated_combinations = generated_df.values.tolist()

    # Criar uma lista para armazenar os resultados
    results = []

    # Iterar sobre cada combinação gerada
    for combo in generated_combinations:
        # Converter a combinação gerada em um conjunto para facilitar a comparação
        combo_set = set(combo)

        # Criar uma nova coluna em 'official_df' para armazenar os acertos por sorteio
        official_df['Acertos'] = official_df[[f'Bola{i}' for i in range(1, 7)]].apply(
            lambda x: len(combo_set.intersection(set(x))), axis=1
        )

        # Calcular o número total de acertos para essa combinação
        total_hits = official_df['Acertos'].sum()

        # Armazenar os resultados
        results.append([*combo, total_hits])

    # Criar um DataFrame com os resultados
    results_df = pd.DataFrame(results, columns=['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Acertos'])

    return results_df


# Função para calcular evolução da arrecadação
def plot_evolution(official_df):
    fig = px.line(
        official_df,
        x='Data do Sorteio',
        y='Arrecadação Total',
        title='Evolução da Arrecadação Total',
        labels={'Data do Sorteio': 'Data', 'Arrecadação Total': 'Arrecadação (R$)'}
    )
    return fig

# Função para simular prêmios
def simulate_prizes(official_df, user_numbers):
    user_set = set(user_numbers)
    official_df['Números Sorteados'] = official_df[[f'Bola{i}' for i in range(1, 7)]].apply(lambda x: list(x), axis=1)

    official_df['Acertos'] = official_df['Números Sorteados'].apply(lambda x: len(user_set.intersection(set(x))))

    official_df['Prêmio'] = official_df['Acertos'].apply(lambda x: 
        official_df['Rateio 6 acertos'] if x == 6 else
        official_df['Rateio 5 acertos'] if x == 5 else
        official_df['Rateio 4 acertos'] if x == 4 else 0
    )
    return official_df[['Data do Sorteio', 'Números Sorteados', 'Acertos', 'Prêmio']]

# Função principal
def main():
    st.title("Loteria Inteligente - Mega-Sena e Lotofácil")
    st.sidebar.title("Configurações")
    
    # Carregamento dos arquivos CSV
    st.sidebar.subheader("Upload de Dados")
    official_file = st.sidebar.file_uploader("Resultados Oficiais (CSV)", type="csv")
    generated_file = st.sidebar.file_uploader("Resultados Gerados pela IA (CSV)", type="csv")
    
    # Se arquivos forem carregados
    if official_file and generated_file:
        official_df = pd.read_csv(official_file)
        generated_df = pd.read_csv(generated_file)

        # Visão geral dos dados
        st.header("Resultados Oficiais")
        st.write(official_df.head())
        st.header("Resultados Gerados pela IA")
        st.write(generated_df.head())

        # Comparação de acertos
        st.subheader("Desempenho das Combinações Geradas")
        results_df = calculate_hits(official_df, generated_df)
        #st.write(results_df[['Números Gerados', 'Acertos']])

        # Gráfico de distribuição de acertos
        accuracy_summary = results_df['Acertos'].value_counts().reset_index()
        accuracy_summary.columns = ['Número de Acertos', 'Frequência']
        st.plotly_chart(
            px.bar(
                accuracy_summary,
                x='Número de Acertos',
                y='Frequência',
                title='Distribuição de Acertos das Combinações Geradas',
                labels={'Número de Acertos': 'Nº de Acertos', 'Frequência': 'Quantidade'}
            )
        )

        # Gráfico de evolução de arrecadação
        st.subheader("Evolução da Arrecadação")
        st.plotly_chart(plot_evolution(official_df))

        # Simulação de prêmios
        st.subheader("Simulador de Prêmios")
        user_numbers_input = st.text_input("Insira sua combinação (separados por vírgula):")
        
        if user_numbers_input:
            user_numbers = list(map(int, user_numbers_input.split(',')))
            simulation_df = simulate_prizes(official_df, user_numbers)
            st.write("Resultados da Simulação:")
            st.write(simulation_df)

    else:
        st.warning("Por favor, carregue os arquivos CSV para continuar.")

    # Checkout Simples
    st.sidebar.title("Adquira a Lista Completa")
    st.sidebar.subheader("Pacotes Disponíveis")
    st.sidebar.write("""
    - **Pacote Completo**: R$ 199,99 - Todas as combinações geradas.
    - **Pacote Filtro**: R$ 99,99 - Top 100 combinações com maior precisão.
    """)
    st.sidebar.button("Comprar Agora")

if __name__ == "__main__":
    main()
