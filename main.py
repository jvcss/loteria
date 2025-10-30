import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from model_utils import (
    load_data, split_training_data, train_decision_tree,
    evaluate_model, export_tree, save_filtered_predictions
)

st.set_page_config(layout="wide")
st.title("Decision Tree - Treinamento, Avaliação e Visualização")

with st.sidebar:
    st.header("Configuração")
    training_path = st.text_input("Training Data CSV", "training_data.csv")
    evaluation_path = st.text_input("Evaluation Data CSV", "evaluation_data.csv")
    output_path = st.text_input("Resultados Filtrados CSV", "resultado.csv")
    show_graphviz = st.checkbox("Mostrar Árvore no Graphviz", value=False)
    sum_filter = st.number_input("Valor mínimo de soma na predição", value=174)

# Isolar o pipeline completo
@st.cache_data(show_spinner=False)
def executar_pipeline(training_path, evaluation_path, output_path, sum_filter):
    # Carregar e dividir dados
    training_data, evaluation_data = load_data(training_path, evaluation_path)
    X_train, y_train = split_training_data(training_data)

    # Treinar modelo
    model = train_decision_tree(X_train, y_train)

    # Avaliar modelo (ajustar para seu problema real)
    # Aqui, por padrão, evaluation_data não possui y_eval
    predictions, acc = evaluate_model(model, evaluation_data, y_eval=None)

    # Salvar previsões filtradas
    filtered = save_filtered_predictions(predictions, X_train, output_path)

    # Para exibição: pegue uma amostra aleatória e as predições filtradas por soma
    random_pred = predictions[np.random.choice(len(predictions))]
    preds_sum_filter = [pred for pred in predictions if np.sum(pred) >= sum_filter]

    # Exportação da árvore
    feature_names = [f"Num{i+1}" for i in range(training_data.shape[1])]
    graphviz_tree = export_tree(model, feature_names)

    # Para o matplotlib, retorne dados necessários para plot
    return {
        "model": model,
        "training_data": training_data,
        "acc": acc,
        "random_pred": random_pred,
        "preds_sum_filter": preds_sum_filter,
        "graphviz_tree": graphviz_tree,
        "feature_names": feature_names
    }

if st.button("Executar Treinamento e Avaliação"):
    with st.spinner("Processando..."):
        results = executar_pipeline(
            training_path, evaluation_path, output_path, sum_filter
        )

    if results["acc"] is not None:
        st.subheader("Acurácia na validação:")
        st.metric("Porcentagem de acerto", f"{results['acc']*100:.2f}%")
    else:
        st.info("Sem dados de target em evaluation_data para calcular acurácia.")

    st.write("Amostra de predição aleatória:", results["random_pred"])
    st.write("Previsões com soma >= valor mínimo:")
    for pred in results["preds_sum_filter"]:
        st.write(pred)

    st.subheader("Árvore de Decisão (matplotlib)")
    fig, ax = plt.subplots(figsize=(20, 10))
    plot_tree(
        results["model"],
        filled=True,
        feature_names=results["feature_names"]
    )
    st.pyplot(fig)

    if show_graphviz:
        st.subheader("Árvore de Decisão (Graphviz)")
        st.graphviz_chart(results["graphviz_tree"].source)

    st.success("Processo finalizado.")
