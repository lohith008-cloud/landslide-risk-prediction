import joblib

from sklearn.metrics import (
    classification_report,
    confusion_matrix
)

from sklearn.model_selection import (
    train_test_split
)

from src.data_ingestion import (
    load_dataset
)

from src.feature_engineering import (
    create_features
)

from src.data_preprocessing import (
    preprocess_data
)

df = load_dataset()

df = create_features(df)

X, y = preprocess_data(df)

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42
)

model = joblib.load(
    "models/landslide_model.pkl"
)

predictions = model.predict(
    X_test
)

print(classification_report(
    y_test,
    predictions
))

print(confusion_matrix(
    y_test,
    predictions
))