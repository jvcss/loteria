import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score
import graphviz

def load_data(training_path, evaluation_path):
    training_data = np.loadtxt(training_path, dtype=np.int32, delimiter=",")
    evaluation_data = np.loadtxt(evaluation_path, dtype=np.int32, delimiter=",")
    return training_data, evaluation_data

def split_training_data(training_data):
    return np.array_split(training_data, 2)

def train_decision_tree(X, y):
    model = DecisionTreeClassifier()
    model.fit(X, y)
    return model

def evaluate_model(model, X_eval, y_eval=None):
    predictions = model.predict(X_eval)
    acc = accuracy_score(y_eval, predictions) if y_eval is not None else None
    return predictions, acc

def export_tree(model, feature_names):
    dot_data = export_graphviz(
        model, filled=True, feature_names=feature_names
    )
    return graphviz.Source(dot_data)

def save_filtered_predictions(predictions, training_X, out_path):
    filtered = [pred for pred in predictions if pred not in training_X]
    with open(out_path, "w") as f:
        for pred in filtered:
            f.write(f"{pred}\n")
    return filtered
