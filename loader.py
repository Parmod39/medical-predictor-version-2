import os
import pandas as pd


def load_and_prepare(dataset_file: str):
    if not os.path.exists(dataset_file):
        raise FileNotFoundError(f"Dataset '{dataset_file}' not found.")
    df = pd.read_csv(dataset_file)
    df.columns = df.columns.str.strip()
    df.rename(columns={df.columns[0]: 'Disease'}, inplace=True)
    symptom_cols = df.columns[1:]
    long = df.melt(
        id_vars=['Disease'], value_vars=symptom_cols,
        var_name='Col', value_name='Symptom'
    ).dropna()
    long['Symptom'] = (
        long['Symptom']
        .str.replace('_', ' ')
        .str.strip()
        .str.lower()
    )
    symptoms = sorted(long['Symptom'].unique())
    return long, symptoms