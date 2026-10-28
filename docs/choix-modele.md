# Choix du modèle

Date : 27/10/2026 · Groupe : [Salaheddine el assassi , Ahmed Ben abou , Ahmed Faris]

## Contexte
MaintAI : prédire, à partir de relevés de capteurs, si une machine va tomber en panne, pour que l'équipe de maintenance choisisse chaque matin les machines à inspecter. Métrique principale : le **rappel**, car une panne manquée arrête une ligne une journée alors qu'une fausse alerte ne coûte qu'une heure d'inspection (section 5).

## Données et découpage
`data/exemple_pannes.csv` : 5 000 relevés, 17,6 % de pannes. Variables : `temperature_c`, `vibration_mm_s`, `load_pct`, `runtime_hours` ; cible : `failure`. Découpage aléatoire stratifié, graine 42 : 4 000 lignes d'entraînement, **1 000 lignes de test** (≈ 176 pannes), identiques pour tous les modèles.

## Résultats sur le jeu de test

| Modèle | Rappel (principale) | Précision | F1 | Accuracy |
|---|---|---|---|---|
| Baseline (classe majoritaire) | 0,000 | 0,000 | 0,000 | 0,824 |
| Régression logistique `class_weight="balanced"` | **0,847** | 0,527 | 0,649 | 0,839 |
| Régression logistique | 0,574 | 0,737 | 0,645 | 0,889 |
| HistGradientBoosting | 0,574 | 0,697 | 0,629 | 0,881 |
| Random Forest | 0,557 | 0,705 | 0,622 | 0,881 |
| KNN (k = 15) | 0,517 | 0,784 | 0,623 | 0,890 |

## Décision
Modèle retenu : **régression logistique avec `class_weight="balanced"`**, qui obtient le meilleur rappel (0,847) : sur ~176 pannes du test, elle en détecte ~149 et en manque ~27, contre ~75 manquées pour le meilleur modèle non pondéré. Elle bat largement la baseline (+0,847 de rappel ; la baseline ne détecte aucune panne malgré 82,4 % d'accuracy).

Le prix est la précision : 0,527, soit environ une alerte sur deux justifiée (~134 fausses alertes sur 1 000 relevés). Vu le coût relatif (1 heure d'inspection contre 1 journée d'arrêt), ce compromis est acceptable.

Critère d'acceptation (section 5) : rappel ≥ 0,75 **et** précision ≥ 0,50 sur le jeu de test → **atteint** (0,847 et 0,527). La précision reste toutefois très proche du seuil.

C'est aussi un modèle simple, rapide et interprétable (coefficients par variable), ce qui facilite l'explication des alertes à l'équipe de maintenance.

## Limites
- **Taille du test** : ~176 pannes seulement ; une dizaine de pannes de plus ou de moins détectées fait varier le rappel de ±0,05. Une validation croisée donnerait une estimation plus fiable.
- **Choix fait sur le jeu de test** : le meilleur modèle a été sélectionné sur ce même test, donc son score est légèrement optimiste. Il faudrait un jeu de validation séparé.
- **Seuil de décision par défaut (0,5)** et hyperparamètres non réglés : ajuster le seuil permettrait de choisir explicitement le compromis rappel / précision.
- **Découpage aléatoire** : pas d'identifiant de machine ni de date, donc des relevés d'une même machine peuvent se trouver en entraînement et en test, et on ne teste pas la capacité à prédire le futur.
- **Précision juste au-dessus du seuil** : une petite dérive des données pourrait faire passer le modèle sous le critère.