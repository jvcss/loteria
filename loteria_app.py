import io
import streamlit as st
import pandas as pd
import plotly.express as px
import time  # Para simular o delay de upload

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

    st.metric("Prêmio Total Acumulado", f"R${total_prizes:,.2f}")
    st.metric("Total de Quadras", total_hits["Acertos4"])
    st.metric("Total de Quinas", total_hits["Acertos5"])
    st.metric("Total de Senas", total_hits["Acertos6"])

def main():
    st.title("Análise de Performance de IA em Loterias")
    st.sidebar.title("Dados da Loteria")

    st.sidebar.subheader("Upload de Dados")
    
    # Caminho dos arquivos locais
    official_file_path = "Mega-Sena.csv"
    generated_file_path = "resultado_modificado.csv"

    # Simulando o upload dos arquivos locais
    official_file = simulate_file_upload(official_file_path)
    generated_file = simulate_file_upload(generated_file_path)

    # Exibindo a animação enquanto o processamento acontece
    with st.spinner("Processando arquivos, aguarde..."):
        time.sleep(2)  # Simula o tempo de upload

        # Carregar os dados dos arquivos
        official_df = load_data(official_file)
        generated_df = load_data(generated_file)
        try:
            validate_data(official_df, generated_df)
        except ValueError as e:
            st.error(f"Erro nos dados: {e}")
            return

        # Exibe os dados carregados
        st.header("Dados Carregados")
        st.subheader("Resultados Oficiais")
        st.write(official_df.head())  # Exibe as primeiras linhas do arquivo oficial
        st.subheader("Resultados Gerados pela IA")
        st.write(generated_df.head())  # Exibe as primeiras linhas do arquivo gerado pela IA

if __name__ == "__main__":
    main()
