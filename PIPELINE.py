import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer


def extract_data(file_path):
    print("Extracting data...")
    return pd.read_csv(file_path)


def transform_data(df):
    print("Transforming data...")

    numeric_features = df.select_dtypes(include=["int64", "float64"]).columns
    categorical_features = df.select_dtypes(include=["object", "string"]).columns

    numeric_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="mean")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features)
        ]
    )

    transformed_data = preprocessor.fit_transform(df)

    return transformed_data


def load_data(transformed_data, output_path):
    print("Loading data...")

    if hasattr(transformed_data, "toarray"):
        transformed_data = transformed_data.toarray()

    processed_df = pd.DataFrame(transformed_data)
    processed_df.to_csv(output_path, index=False)

    print("ETL Pipeline Completed Successfully ✅")


if __name__ == "__main__":
    input_file = "raw_data.csv"
    output_file = "processed_data.csv"

    df = extract_data(input_file)
    transformed_data = transform_data(df)
    load_data(transformed_data, output_file)