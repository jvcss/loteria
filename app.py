import numpy as np
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_graphviz
import matplotlib.pyplot as plt
import graphviz

# Carrega a lista para treino
training_data = np.loadtxt("training_data.csv", dtype=np.int32, delimiter=",")

# Número par de dados para treino
training_data_a, training_data_b = np.array_split(training_data, 2)

# Cria o modelo
model = DecisionTreeClassifier()

# Treina o modelo
model.fit(training_data_a, y=training_data_b)

# Carrega a lista para validação
evaluation_data = np.loadtxt("evaluation_data.csv", dtype=np.int32, delimiter=",")

# Descobre os próximos valores
predictions = model.predict(evaluation_data)

# Filtra e salva os resultados em um arquivo
with open("resultado.csv", "w") as file:
    for prediction in predictions:
        if prediction not in training_data_a:
            file.write(f"{prediction}\n")

# Exibe um valor aleatório das predições
print(predictions[np.random.choice(len(predictions))])

print("__________________")

# Verifica e exibe valores que atendem à condição
for prediction in predictions:
    if np.sum(prediction) >= 174:  # Corrigido para usar np.sum
        print(prediction)

# # Visualiza a árvore de decisão
# plt.figure(figsize=(20, 10))
# plot_tree(
#     model,
#     filled=True,
#     feature_names=[f"Num{i+1}" for i in range(training_data.shape[1])],
# )
# plt.show()

# # Exporta a árvore para um arquivo .dot
# dot_data = export_graphviz(
#     model,
#     filled=True,
#     feature_names=[f"Num{i+1}" for i in range(training_data.shape[1])],
# )
# graph = graphviz.Source(dot_data)
# graph.render("decision_tree")
