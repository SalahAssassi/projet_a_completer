"""Chargement et découpage des données."""
import pandas as pd
from sklearn.model_selection import train_test_split

from monprojet import config


def load_data(path=None) -> pd.DataFrame:
    """Lit le fichier CSV et renvoie un DataFrame."""
    path = path or config.DATA_PATH
    df = pd.read_csv(path)
    if config.TARGET not in df.columns:
        raise ValueError(
            f"La colonne cible « {config.TARGET} » est absente de {path}. "
            f"Colonnes trouvées : {list(df.columns)}"
        )
    return df.dropna(subset=[config.TARGET])


def feature_columns(df: pd.DataFrame) -> list:
    """Les colonnes d'entrée : celles de config.FEATURES, ou toutes sauf la cible et la date. (Fournie.)"""
    if config.FEATURES is not None:
        return list(config.FEATURES)
    excluded = {config.TARGET, config.TIME_COLUMN}
    return [c for c in df.columns if c not in excluded]


def split(df: pd.DataFrame):
    """Renvoie X_train, X_test, y_train, y_test."""
    X = df[feature_columns(df)]
    y = df[config.TARGET]

    if config.SPLIT == "random":
        stratify = y if config.TASK == "classification" else None
        return train_test_split(X, y, test_size=config.TEST_SIZE,
                                random_state=config.SEED, stratify=stratify)

    if config.SPLIT == "chronologique":
        if config.TIME_COLUMN is None:
            raise ValueError("SPLIT = 'chronologique' exige TIME_COLUMN dans config.py")
        order = pd.to_datetime(df[config.TIME_COLUMN]).argsort().to_numpy()
        n_test = max(1, round(len(df) * config.TEST_SIZE))
        train_idx, test_idx = order[:-n_test], order[-n_test:]
        return X.iloc[train_idx], X.iloc[test_idx], y.iloc[train_idx], y.iloc[test_idx]

    raise ValueError(f"SPLIT inconnu : {config.SPLIT!r} (attendu 'random' ou 'chronologique')")