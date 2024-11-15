import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

def is_categorical(series):
    if series.dtype == 'object' or series.nunique() <= 10:
        return True
    return False

def generate_synthetic_column(series):
    if is_categorical(series):
        unique_values = series.dropna().unique()
        return [random.choice(unique_values) for _ in range(len(series))]
    elif series.dtype == 'int64':
        return np.random.randint(series.min(), series.max() + 1, len(series))
    elif series.dtype == 'float64':
        return np.random.normal(series.mean(), series.std(), len(series)).round(2)
    else:
        return [fake.word() for _ in range(len(series))]

def generate_privacy_preserving_synthetic_data(df):
    synthetic_data = pd.DataFrame()
    for column in df.columns:
        synthetic_data[column] = generate_synthetic_column(df[column])
    return synthetic_data
