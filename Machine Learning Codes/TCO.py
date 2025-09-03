import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import joblib
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import LabelBinarizer, LabelEncoder, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.multiclass import OneVsRestClassifier
from imblearn.over_sampling import SMOTE

# Load dataset
df = pd.read_csv("TCO.csv")

# === Keep only 4 raw features ===
X = df[[
    "Wavelength",
    "AbsorptionRate",
    "Transmission",
    "OpticalDensity"
]]
y = df["Material"]

# Encode class labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)
class_names = le.classes_

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Apply SMOTE on training data only
sm = SMOTE(random_state=42)
X_train, y_train = sm.fit_resample(X_train, y_train)

# Binarize for ROC (optional)
lb = LabelBinarizer()
y_test_bin = lb.fit_transform(y_test)

# Define models
models = {
    "SVC": make_pipeline(StandardScaler(), OneVsRestClassifier(SVC(probability=True, C=10, kernel='rbf'))),
    "KNN": make_pipeline(StandardScaler(), OneVsRestClassifier(KNeighborsClassifier(n_neighbors=3))),
    "Decision Tree": OneVsRestClassifier(DecisionTreeClassifier()),
    "Random Forest": OneVsRestClassifier(RandomForestClassifier(n_estimators=200)),
    "XGBoost": make_pipeline(StandardScaler(), OneVsRestClassifier(XGBClassifier(
        eval_metric='mlogloss', learning_rate=0.1, n_estimators=200, max_depth=10))),
    "MLP": make_pipeline(StandardScaler(), OneVsRestClassifier(MLPClassifier(max_iter=500)))
}

# Evaluation and storage
accuracy_results = []
conf_matrices = {}

print("=== Model Evaluation ===")
for name, model in models.items():
    try:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"\n{name} Accuracy: {acc:.4f}")
        print(classification_report(y_test, y_pred, target_names=class_names))
        accuracy_results.append((name, acc))
        conf_matrices[name] = confusion_matrix(y_test, y_pred)
    except Exception as e:
        print(f"{name} failed: {e}")
        accuracy_results.append((name, 0.0))

# Accuracy Bar Chart
accuracy_results.sort(key=lambda x: x[1], reverse=True)
model_names, model_accuracies = zip(*accuracy_results)

plt.figure(figsize=(10, 6))
sns.barplot(x=list(model_accuracies), y=list(model_names), palette="viridis")
plt.xlabel("Accuracy")
plt.title("Model Accuracy Comparison")
plt.xlim(0, 1)
plt.grid(True, axis='x')
plt.tight_layout()
plt.show()

# Confusion Matrix Grid
num_models = len(conf_matrices)
cols = 3
rows = int(np.ceil(num_models / cols))

fig, axes = plt.subplots(rows, cols, figsize=(18, 5 * rows))
for idx, (name, cm) in enumerate(conf_matrices.items()):
    ax = axes.flat[idx]
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
    disp.plot(ax=ax, xticks_rotation=45, colorbar=False)
    ax.set_title(f"Confusion Matrix: {name}")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    ax.grid(False)

# Hide any unused subplot axes
for i in range(len(conf_matrices), len(axes.flat)):
    fig.delaxes(axes.flat[i])

plt.tight_layout()
plt.show()

# === ROC Curves ===
plt.figure(figsize=(14, 10))

for name, model in models.items():
    try:
        model.fit(X_train, y_train)
        if hasattr(model, "predict_proba"):
            y_score = model.predict_proba(X_test)
        else:
            y_score = model.decision_function(X_test)
        
        if np.isnan(y_score).any():
            print(f"Skipping {name}: y_score contains NaNs.")
            continue

        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        for i in range(len(class_names)):
            fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_score[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])
        mean_auc = np.mean(list(roc_auc.values()))
        plt.plot(fpr[0], tpr[0], label=f"{name} (avg AUC = {mean_auc:.2f})")

    except Exception as e:
        print(f"Skipping {name} due to {e}")

plt.plot([0, 1], [0, 1], 'k--')
plt.title("ROC Curve (One-vs-Rest Multi-class)")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# === Learning Curves ===
plt.figure(figsize=(20, 16))
for idx, (name, model) in enumerate(models.items()):
    plt.subplot(3, 2, idx + 1)
    try:
        train_sizes, train_scores, test_scores = learning_curve(
            model, X, y_encoded, cv=5, scoring='accuracy',
            n_jobs=-1, train_sizes=np.linspace(0.1, 1.0, 5)
        )
        train_mean = np.mean(train_scores, axis=1)
        test_mean = np.mean(test_scores, axis=1)
        plt.plot(train_sizes, train_mean, 'o-', label='Train Accuracy')
        plt.plot(train_sizes, test_mean, 's-', label='Validation Accuracy')
        plt.title(f"Learning Curve: {name}")
        plt.xlabel("Training Size")
        plt.ylabel("Accuracy")
        plt.legend()
        plt.grid(True)
    except Exception as e:
        plt.title(f"{name} - Failed: {str(e)}")

plt.tight_layout()
plt.show()

# === Save Trained XGBoost Pipeline ===
xgb_pipeline = models["XGBoost"]
xgb_pipeline.fit(X_train, y_train)

joblib.dump(xgb_pipeline, "xgb_pipeline_model.pkl")
joblib.dump(le, "label_encoder.pkl")
print("✅ XGBoost model pipeline saved as 'xgb_pipeline_model.pkl'")
print("✅ Label encoder saved as 'label_encoder.pkl'")

# --- Test one prediction before finishing ---
sample = X_test.iloc[[0]]
pred_index = xgb_pipeline.predict(sample)[0]
pred_label = le.inverse_transform([pred_index])[0]

print("Raw prediction index:", pred_index)
print("Predicted material:", pred_label)
print("All encoder classes:", le.classes_)

# === 🔹 Manual User Input Prediction ===
print("\n=== Manual Prediction Test ===")
try:
    wavelength = float(input("Enter Wavelength (nm): "))
    absorbance = float(input("Enter Absorption Rate: "))
    transmission = float(input("Enter Transmission (%): "))
    optical_density = float(input("Enter Optical Density: "))

    input_df = pd.DataFrame([[
        wavelength,
        absorbance,
        transmission,
        optical_density
    ]], columns=[
        "Wavelength",
        "AbsorptionRate",
        "Transmission",
        "OpticalDensity"
    ])

    pred_index = xgb_pipeline.predict(input_df)[0]
    pred_label = le.inverse_transform([pred_index])[0]
    print(f"✅ Predicted Material: {pred_label}")

except Exception as e:
    print(f"❌ Error in manual prediction: {e}")
