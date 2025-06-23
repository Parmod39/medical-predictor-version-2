import numpy as np
from pandas import Series
from tree import TreeNode


def compute_entropy(labels: Series) -> float:
    counts = labels.value_counts()
    probs = counts / counts.sum()
    if len(probs) <= 1:
        return 0.0
    return -np.sum(probs * np.log2(probs))


def compute_information_gain(df, symptom_col: str, symptom: str) -> float:
    parent_entropy = compute_entropy(df['Disease'])
    mask = df[symptom_col] == symptom
    df_yes, df_no = df[mask], df[~mask]
    if df_yes.empty or df_no.empty:
        return 0.0
    weight_yes = len(df_yes) / len(df)
    ent_yes = compute_entropy(df_yes['Disease'])
    ent_no = compute_entropy(df_no['Disease'])
    return parent_entropy - (weight_yes * ent_yes + (1 - weight_yes) * ent_no)


def build_tree(df, symptoms, used, symptom_col: str = 'Symptom') -> TreeNode:
    # Leaf if single disease remains
    if df['Disease'].nunique() == 1:
        return TreeNode(label=df['Disease'].iloc[0])
    # Leaf by majority if no symptoms left
    if all(used.values()):
        majority = df['Disease'].mode()[0]
        return TreeNode(label=majority)

    best_symptom, best_gain = None, 0.0
    for s in symptoms:
        if not used[s]:
            gain = compute_information_gain(df, symptom_col, s)
            if gain > best_gain:
                best_gain, best_symptom = gain, s
    if best_gain <= 0.0 or best_symptom is None:
        majority = df['Disease'].mode()[0]
        return TreeNode(label=majority)

    used[best_symptom] = True
    node = TreeNode(attribute=best_symptom)
    mask = df[symptom_col] == best_symptom
    node.yes = build_tree(df[mask], symptoms, used.copy(), symptom_col)
    node.no = build_tree(df[~mask], symptoms, used.copy(), symptom_col)
    return node