import yaml
import joblib

from sklearn.model_selection import (
    train_test_split,
    cross_val_score
)

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    classification_report
)

from xgboost import XGBClassifier

from src.data_ingestion import load_dataset
from src.feature_engineering import create_features
from src.data_preprocessing import preprocess_data

from app.utils.logger import setup_logger

logger = setup_logger(
    "training",
    "training.log"
)

def load_config():

    with open("config/config.yaml", "r") as file:
        return yaml.safe_load(file)

config = load_config()

logger.info("Loading dataset")

df = load_dataset()

logger.info("Creating features")

df = create_features(df)

X, y = preprocess_data(df)
print(X.corrwith(y).sort_values(ascending=False))

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=config["model"]["test_size"],
    random_state=config["model"]["random_state"],
    stratify=y
)

# BASELINE MODEL

logistic_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000))
])

logger.info("Training Logistic Regression")

logistic_pipeline.fit(X_train, y_train)

logistic_pred = logistic_pipeline.predict(X_test)

logistic_acc = accuracy_score(
    y_test,
    logistic_pred
)

print(f"Logistic Regression Accuracy: {logistic_acc}")

# ADVANCED MODEL

xgb_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    (
        "model",
        XGBClassifier(
            n_estimators=300,
            max_depth=7,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=42,
            eval_metric="logloss"
        )
    )
])

logger.info("Training XGBoost")

xgb_pipeline.fit(X_train, y_train)

xgb_pred = xgb_pipeline.predict(X_test)

xgb_acc = accuracy_score(
    y_test,
    xgb_pred
)

print(f"XGBoost Accuracy: {xgb_acc}")

print(classification_report(
    y_test,
    xgb_pred
))

cv_scores = cross_val_score(
    xgb_pipeline,
    X,
    y,
    cv=5,
    scoring="accuracy"
)

print(f"Cross Validation Accuracy: {cv_scores.mean()}")

joblib.dump(
    xgb_pipeline,
    config["paths"]["model_path"]
)

joblib.dump(
    xgb_pipeline.named_steps["scaler"],
    config["paths"]["scaler_path"]
)

logger.info("Model Saved Successfully")