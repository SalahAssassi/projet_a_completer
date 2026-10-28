"""Les modèles à comparer."""
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import (HistGradientBoostingClassifier, HistGradientBoostingRegressor,
                              RandomForestClassifier, RandomForestRegressor)
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

from monprojet import config


def candidates() -> dict:
    """Renvoie un dictionnaire {nom: modèle scikit-learn non entraîné}, la baseline en premier."""
    if config.TASK == "classification":
        return {
            "baseline": DummyClassifier(strategy="most_frequent"),
            "regression_logistique": LogisticRegression(max_iter=1000, random_state=config.SEED),
            "regression_logistique_balanced": LogisticRegression(
                max_iter=1000, class_weight="balanced", random_state=config.SEED),
            "knn": KNeighborsClassifier(n_neighbors=15),
            "random_forest": RandomForestClassifier(n_estimators=200, random_state=config.SEED),
            "gradient_boosting": HistGradientBoostingClassifier(random_state=config.SEED),
        }

    if config.TASK == "regression":
        return {
            "baseline": DummyRegressor(strategy="mean"),
            "regression_lineaire": LinearRegression(),
            "knn": KNeighborsRegressor(n_neighbors=15),
            "random_forest": RandomForestRegressor(n_estimators=200, random_state=config.SEED),
            "gradient_boosting": HistGradientBoostingRegressor(random_state=config.SEED),
        }

    raise ValueError(f"TASK inconnue : {config.TASK!r} (attendu 'classification' ou 'regression')")