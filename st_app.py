import streamlit as st
import pandas as pd
import plotly.express as px

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

def calculate_hits(official_df, generated_df):
    """Calcula o desempenho das combinações geradas pela IA."""
    results = []
    for combo in generated_df.values:
        combo_set = set(combo)
        official_df["Acertos"] = official_df[[f"Bola{i}" for i in range(1, 7)]].apply(
            lambda x: len(combo_set.intersection(set(x))), axis=1
        )
        total_hits = official_df["Acertos"].sum()
        results.append([*combo, total_hits])
    return pd.DataFrame(results, columns=["Bola1", "Bola2", "Bola3", "Bola4", "Bola5", "Bola6", "Acertos"])

def plot_accuracy_distribution(results_df):
    """Plota a distribuição dos acertos das combinações geradas."""
    accuracy_summary = results_df["Acertos"].value_counts().reset_index()
    accuracy_summary.columns = ["Número de Acertos", "Frequência"]
    return px.bar(
        accuracy_summary,
        x="Número de Acertos",
        y="Frequência",
        title="Distribuição de Acertos das Combinações Geradas",
        labels={"Número de Acertos": "Nº de Acertos", "Frequência": "Quantidade"},
    )

def main():
    st.title("Análise de Performance de IA em Loterias")
    st.sidebar.title("Configurações")

    st.sidebar.subheader("Upload de Dados")
    official_file = st.sidebar.file_uploader("Resultados Oficiais (CSV)", type="csv")
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
        results_df = calculate_hits(official_df, generated_df)
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
