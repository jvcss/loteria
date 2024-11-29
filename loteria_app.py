# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import locale
# from babel.numbers import parse_decimal

# # Definir o local para formato brasileiro
# locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


# def show_checkout():
#     """
#     Exibe a interface do Checkout com as opções de compra.
#     """
#     st.title("Adquira a Lista Completa")
#     st.write("""
#     ### Pacotes Disponíveis:
#     - **Pacote Completo**: R$ 199,99 - Todas as combinações geradas.
#     - **Pacote Filtro**: R$ 99,99 - Top 100 combinações com maior precisão.
#     """)
    
#     # Botão de pagamento (redirecionamento simulado)
#     if st.button("Comprar Agora"):
#         stripe_checkout_url = "https://checkout.stripe.com/pay/cs_test_YOUR_CHECKOUT_SESSION_ID"
#         st.write("Redirecionando para o pagamento...")
#         st.markdown(f"[Clique aqui se não for redirecionado automaticamente.]({stripe_checkout_url})")


# def parse_brazilian_currency(value):
#     """
#     Converte um valor no formato brasileiro de moeda (e.g., "R$15.591.365,07") para float.
    
#     Args:
#         value (str): Valor monetário em formato brasileiro.

#     Returns:
#         float: Valor convertido em formato numérico.
#     """
#     try:
#         return float(parse_decimal(value.replace("R$", "").strip(), locale='pt_BR'))
#     except (ValueError, TypeError):
#         return 0.0

# def calculate_hits(official_df, generated_df):
#     """Calcula o número de acertos entre os números gerados pela IA e os resultados oficiais.

#     Args:
#         official_df (pd.DataFrame): DataFrame com os resultados oficiais da Mega-Sena.
#         generated_df (pd.DataFrame): DataFrame com os números gerados pela IA.

#     Returns:
#         pd.DataFrame: DataFrame com as combinações geradas, o número de acertos e outros dados relevantes.
#     """

#     # Assumindo que 'generated_df' contém apenas as colunas com os números gerados
#     generated_combinations = generated_df.values.tolist()

#     # Criar uma lista para armazenar os resultados
#     results = []

#     # Iterar sobre cada combinação gerada
#     for combo in generated_combinations:
#         # Converter a combinação gerada em um conjunto para facilitar a comparação
#         combo_set = set(combo)

#         # Criar uma nova coluna em 'official_df' para armazenar os acertos por sorteio
#         official_df['Acertos'] = official_df[[f'Bola{i}' for i in range(1, 7)]].apply(
#             lambda x: len(combo_set.intersection(set(x))), axis=1
#         )

#         # Calcular o número total de acertos para essa combinação
#         total_hits = official_df['Acertos'].sum()

#         # Armazenar os resultados
#         results.append([*combo, total_hits])

#     # Criar um DataFrame com os resultados
#     results_df = pd.DataFrame(results, columns=['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Acertos'])

#     return results_df

# # Função para simular prêmios com os números gerados pela IA
# def simulate_prizes_with_generated(official_df, generated_df):
#     """
#     Calcula prêmios potenciais ao jogar combinações geradas pela IA.

#     Args:
#         official_df (pd.DataFrame): DataFrame com os resultados oficiais.
#         generated_df (pd.DataFrame): DataFrame com as combinações geradas pela IA.

#     Returns:
#         pd.DataFrame: DataFrame com acertos, prêmios e outras estatísticas por combinação gerada.
#     """
#     results = []

#     for _, generated_row in generated_df.iterrows():
#         generated_set = set(generated_row.values)

#         # Calcular acertos para cada sorteio oficial
#         official_df['Acertos'] = official_df[[f'Bola{i}' for i in range(1, 7)]].apply(
#             lambda x: len(generated_set.intersection(set(x))), axis=1
#         )

#         # Calcular o prêmio com base nos acertos
#         official_df['Prêmio'] = official_df.apply(
#             lambda row: 
#             parse_brazilian_currency(row['Rateio 6 acertos']) if row['Acertos'] == 6 else
#             parse_brazilian_currency(row['Rateio 5 acertos']) if row['Acertos'] == 5 else
#             parse_brazilian_currency(row['Rateio 4 acertos']) if row['Acertos'] == 4 else 0.0,
#             axis=1
#         )

#         # Obter o total de prêmios ganhos para esta combinação gerada
#         total_prize = official_df['Prêmio'].sum()

#         # Armazenar a combinação gerada e o prêmio total
#         results.append([*generated_row.values, total_prize])

#     # Criar DataFrame com os resultados
#     results_df = pd.DataFrame(
#         results,
#         columns=['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Prêmio Total']
#     )

#     return results_df

# # Atualização do gráfico de prêmios
# def plot_prizes(prizes_df):
#     """Plota um gráfico com a distribuição de prêmios calculados."""
#     prizes_summary = prizes_df['Prêmio Total'].value_counts().reset_index()
#     prizes_summary.columns = ['Prêmio Total (R$)', 'Frequência']
    
#     fig = px.bar(
#         prizes_summary,
#         x='Prêmio Total (R$)',
#         y='Frequência',
#         title='Distribuição de Potenciais Prêmios com Combinações Geradas',
#         labels={'Prêmio Total (R$)': 'Prêmio (R$)', 'Frequência': 'Quantidade'}
#     )
#     return fig

# # Função principal
# def main():
#     st.title("Loteria Inteligente - Mega-Sena e Lotofácil")

#     st.sidebar.title("Configurações")
#     # Carregamento dos arquivos CSV
#     st.sidebar.subheader("Upload de Dados")
#     official_file = st.sidebar.file_uploader("Resultados Oficiais (CSV)", type="csv")
#     generated_file = st.sidebar.file_uploader("Resultados Gerados pela IA (CSV)", type="csv")
#     # Se arquivos forem carregados
#     if official_file and generated_file:
#         official_df = pd.read_csv(official_file)
#         generated_df = pd.read_csv(generated_file)

#         # Visão geral dos dados
#         st.header("Resultados Oficiais")
#         st.write(official_df.head())
#         st.header("Resultados Gerados pela IA")
#         st.write(generated_df.head())

#         # ! Adicionar na função main para exibir os resultados
#         st.subheader("Potencial de Prêmios com Combinações Geradas pela IA")
#         prizes_df = simulate_prizes_with_generated(official_df, generated_df)
#         st.write("Prêmios Potenciais para Combinações Geradas:")
#         st.write(prizes_df)


#         # Comparação de acertos
#         st.subheader("Desempenho das Combinações Geradas")
#         results_df = calculate_hits(official_df, generated_df)
#         st.write(results_df[['Acertos']])
#         # Gráfico de distribuição de acertos
#         accuracy_summary = results_df['Acertos'].value_counts().reset_index()
#         accuracy_summary.columns = ['Número de Acertos', 'Frequência']
#         st.plotly_chart(
#             px.bar(
#                 accuracy_summary,
#                 x='Número de Acertos',
#                 y='Frequência',
#                 title='Distribuição de Acertos das Combinações Geradas',
#                 labels={'Número de Acertos': 'Nº de Acertos', 'Frequência': 'Quantidade'}
#             )
#         )

#         # Simulação de prêmios
#         st.subheader("Simulador de Prêmios")
#         user_numbers_input = st.text_input("Insira sua combinação (separados por vírgula):")
        
#         if user_numbers_input:
#             user_numbers = list(map(int, user_numbers_input.split(',')))
#             simulation_df = simulate_prizes_with_generated(official_df, user_numbers)
#             st.write("Resultados da Simulação:")
#             st.write(simulation_df)

#     else:
#         st.warning("Por favor, carregue os arquivos CSV para continuar.")


# if __name__ == "__main__":
#     main()
import streamlit as st
import pandas as pd
import plotly.express as px
prize_data = {
    "premio_4": 961.50,  # Valor do prêmio para 4 acertos
    "premio_5": 41501.26,  # Valor do prêmio para 5 acertos
    "premio_6": 12561383.62  # Valor do prêmio para 6 acertos
}
# Configuração de cache para melhorar a performance
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

def validate_data(official_df, generated_df):
    """Valida o formato das tabelas carregadas."""
    required_columns_official = {f"Bola{i}" for i in range(1, 7)}
    if not required_columns_official.issubset(official_df.columns):
        raise ValueError("Arquivo oficial deve conter as colunas Bola1 a Bola6.")
    if generated_df.shape[1] != 6:
        raise ValueError("Arquivo gerado pela IA deve conter exatamente 6 colunas.")

def calculate_hits_with_prizes(official_df, generated_df, prize_data):
    """Calcula os acertos e os prêmios potenciais."""
    result_list = []
    for combo in generated_df.values:
        combo_set = set(combo)
        official_df["Acertos"] = official_df[[f"Bola{i}" for i in range(1, 7)]].apply(
            lambda x: len(combo_set.intersection(set(x))), axis=1
        )

        # Categorizar acertos
        official_df["Acertos4"] = (official_df["Acertos"] == 4).astype(int)
        official_df["Acertos5"] = (official_df["Acertos"] == 5).astype(int)
        official_df["Acertos6"] = (official_df["Acertos"] == 6).astype(int)

        # Calcular o prêmio total
        total_prize = sum(
            official_df[col].sum() * prize
            for col, prize in zip(
                ["Acertos4", "Acertos5", "Acertos6"],
                [prize_data["premio_4"], prize_data["premio_5"], prize_data["premio_6"]],
            )
        )

        # Adicionar resultados
        result_list.append(
            list(combo) + [
                official_df["Acertos4"].sum(),
                official_df["Acertos5"].sum(),
                official_df["Acertos6"].sum(),
                total_prize,
            ]
        )

    return pd.DataFrame(
        result_list,
        columns=["Bola1", "Bola2", "Bola3", "Bola4", "Bola5", "Bola6", "Acertos4", "Acertos5", "Acertos6", "Prêmio Total"]
    )

def plot_accuracy_distribution(results_df):
    """Plota a distribuição dos acertos das combinações geradas."""
    # Consolidar os acertos em uma única coluna
    results_df["Acertos"] = (
        results_df["Acertos4"] * 4 + 
        results_df["Acertos5"] * 5 + 
        results_df["Acertos6"] * 6
    )
    
    # Criar a contagem de frequência
    accuracy_summary = results_df["Acertos"].value_counts().reset_index()
    accuracy_summary.columns = ["Número de Acertos", "Frequência"]
    
    # Criar o gráfico
    return px.bar(
        accuracy_summary,
        x="Número de Acertos",
        y="Frequência",
        title="Distribuição de Acertos das Combinações Geradas",
        labels={"Número de Acertos": "Nº de Acertos", "Frequência": "Quantidade"},
    )

def display_summary(results_df):
    """Exibe um resumo dos prêmios e acertos."""
    total_prizes = results_df["Prêmio Total"].sum()
    total_hits = results_df[["Acertos4", "Acertos5", "Acertos6"]].sum()

    st.metric("Prêmio Total Acumulado", f"R${total_prizes:,.2f}")
    st.metric("Total de Quadras", total_hits["Acertos4"])
    st.metric("Total de Quinas", total_hits["Acertos5"])
    st.metric("Total de Senas", total_hits["Acertos6"])

def main():
    st.title("Análise de Performance de IA em Loterias")
    st.sidebar.title("Dados da Loteria")

    st.sidebar.subheader("Upload de Dados")
    # ! vamos preencher essa variavel com o MegaSena.csv que temos na raiz do servidor
    official_file = st.sidebar.file_uploader("Resultados Oficiais (CSV)", type="csv")

    # ! vamos preencher essa variavel com o resultado_mega.csv que temos na raiz do servidor
    generated_file = st.sidebar.file_uploader("Resultados Gerados pela IA (CSV)", type="csv")

    if official_file and generated_file:
        # Carregamento e validação dos dados
        official_df = load_data(official_file)
        generated_df = load_data(generated_file)
        try:
            validate_data(official_df, generated_df)
        except ValueError as e:
            st.error(f"Erro nos dados: {e}")
            return

        # Mostrar os dados carregados
        st.header("Dados Carregados")
        st.subheader("Resultados Oficiais")
        st.write(official_df.head())
        st.subheader("Resultados Gerados pela IA")
        st.write(generated_df.head())

        # Cálculo de acertos
        st.subheader("Análise de Performance")
        # Cálculo de acertos e prêmios
        results_df = calculate_hits_with_prizes(official_df, generated_df, prize_data)
        st.write("Resumo das combinações geradas e seus acertos:")
        st.write(results_df)

        # Plotar distribuição de acertos
        st.plotly_chart(plot_accuracy_distribution(results_df))

        # Informar insights adicionais
        st.info(
            "A análise acima demonstra como as combinações geradas pela IA se comparam com os resultados oficiais."
        )
    else:
        st.warning("Por favor, carregue ambos os arquivos CSV para continuar.")

if __name__ == "__main__":
    main()
