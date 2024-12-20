import io
import streamlit as st
import pandas as pd
import plotly.express as px
import time  # Para simular o delay de upload
from values import mega_sena, resultados_gerados_ia

prize_data = {
    "premio_4": 961.50,  # Valor do prêmio para 4 acertos
    "premio_5": 41501.26,  # Valor do prêmio para 5 acertos
    "premio_6": 12561383.62  # Valor do prêmio para 6 acertos
}

def load_data(file):
    return pd.read_csv(file)

# Função para simular o upload de arquivos
def simulate_file_upload(file_path):
    """Simula o upload de um arquivo local para o file_uploader."""
    with open(file_path, "rb") as f:
        return io.BytesIO(f.read())

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

    col1, col2, col3, col4 = st.columns(4)
    st.metric("Prêmio Total Acumulado", f"R${total_prizes:,.2f}")
    col1.metric("Prêmio Total Acumulado", f"R${total_prizes:,.2f}")
    col2.metric("Total de Quadras", total_hits["Acertos4"])
    col3.metric("Total de Quinas", total_hits["Acertos5"])
    col4.metric("Total de Senas", total_hits["Acertos6"])

def main():
    st.title("Análise de Performance de IA em Loterias")
    st.sidebar.title("Dados da Loteria")

    st.sidebar.subheader("Upload de Dados")
     # vamos preencher essa variavel com o MegaSena.csv que temos na raiz do servidor
    official_file = st.sidebar.file_uploader("Resultados Oficiais (CSV)", type="csv")

    # vamos preencher essa variavel com o resultado_mega.csv que temos na raiz do servidor
    generated_file = st.sidebar.file_uploader("Resultados Gerados pela IA (CSV)", type="csv")

    # Inicialização das variáveis para quando os arquivos não forem carregados
    if official_file is None:
        official_df = pd.DataFrame(mega_sena, columns=[f"Bola{i}" for i in range(1, 7)])
    else:
        # Caso o usuário tenha carregado um arquivo, lê-lo
        official_df = pd.read_csv(official_file)

    if generated_file is None:
        generated_df = pd.DataFrame(resultados_gerados_ia, columns=[f"Bola{i}" for i in range(1, 7)])
    else:
        # Caso o usuário tenha carregado um arquivo, lê-lo
        generated_df = pd.read_csv(generated_file)

    # Exibindo a animação enquanto o processamento acontece
    with st.spinner("Processando arquivos, aguarde..."):
        try:
            validate_data(official_df, generated_df)
        except ValueError as e:
            st.error(f"Erro nos dados: {e}")

        # Cálculo de acertos
        st.subheader("Análise de Performance")
        # Cálculo de acertos e prêmios
        results_df = calculate_hits_with_prizes(official_df, generated_df, prize_data)
        st.write("Resumo das combinações geradas e seus acertos:")
        display_summary(results_df)

        # Plotar distribuição de acertos
        st.plotly_chart(plot_accuracy_distribution(results_df))

        st.write(results_df)
        # Informar insights adicionais
        st.info(
            "A análise acima demonstra como as combinações geradas pela IA se comparam com os resultados oficiais."
        )

        # Exibe os dados carregados
        st.header("Dados Carregados")
        st.subheader("Resultados Oficiais")
        st.write(official_df.head())  # Exibe as primeiras linhas do arquivo oficial
        st.subheader("Resultados Gerados pela IA")
        st.write(generated_df.head())  # Exibe as primeiras linhas do arquivo gerado pela IA

if __name__ == "__main__":
    # Configure the page
    st.set_page_config(
        page_title="I.A da Loteria",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed"  # Options: 'expanded', 'collapsed', 'auto'
    )
    main()
