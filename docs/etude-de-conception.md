# Étude de conception — [nom du projet]

Groupe : [noms] · Version : [brouillon / finale] · Date : [jj/mm/aaaa]

## 1. Contexte et utilisateurs
- Utilisateur principal (un rôle précis) :

## 2. Problème et décision
- Décision que l'utilisateur prend avec le système :
- Fréquence :
- Coût d'une erreur, et pour qui :

## 3. Approche par sous-problème
| Sous-problème | Approche (règles / ML / DL / LLM / RAG) | Pourquoi pas une approche plus simple |
|---|---|---|

## 4. Données

| Jeu de données | Source et licence | Volume | Données personnelles ? |
|---|---|---|---|
| Hotel Booking Demand (`data/hotel_bookings.csv`) | Antonio, Almeida & Nunes, « Hotel booking demand datasets », *Data in Brief*, 2019 — article en accès libre, licence CC BY 4.0 (à confirmer sur la page de l'article) ; copie téléchargée depuis Kaggle (fichier original `hotel_bookings.csv`) | ≈ 119 000 réservations, 32 colonnes, 2 hôtels portugais (un hôtel de ville, un hôtel balnéaire), arrivées de juillet 2015 à août 2017 | Pas d'identifiant direct (ni nom, ni email, ni téléphone). Données pseudonymisées : pays d'origine, identifiants numériques d'agence et d'entreprise. Ces deux identifiants ne sont pas utilisés comme variables. |

**Cible.** `is_canceled` : 1 = réservation annulée, 0 = séjour effectué. Environ 37 % d'annulations : classes déséquilibrées, mais moins que MaintAI.

**Variables retenues (listées dans `config.FEATURES`).**
- Réservation : `hotel`, `lead_time` (jours entre réservation et arrivée), `arrival_date_month`, `stays_in_weekend_nights`, `stays_in_week_nights`, `reserved_room_type`, `meal`, `adr` (prix moyen par nuit), `booking_changes`, `deposit_type`.
- Client : `adults`, `children`, `customer_type`, `is_repeated_guest`, `previous_cancellations`, `previous_bookings_not_canceled`, `total_of_special_requests`, `required_car_parking_spaces`.
- Canal : `market_segment`, `distribution_channel`.

**Variables exclues, et pourquoi.**
- `reservation_status`, `reservation_status_date` : **fuite de données**. Elles indiquent directement si la réservation a été annulée, information inconnue au moment de la prédiction.
- `assigned_room_type` : connue seulement à l'arrivée du client, donc indisponible au moment de la décision.
- `agent`, `company` : identifiants à forte cardinalité, majoritairement vides pour `company`, et proches de données d'identification.
- `country` : écartée dans un premier temps (risque de biais selon la nationalité, voir section 8) ; son apport sera mesuré à part.

**Qualité des données à traiter.** Quelques valeurs manquantes (`children`, `country`), quelques réservations à 0 client et quelques `adr` aberrants (négatifs ou extrêmes). Les valeurs manquantes sont imputées par `build_preprocessing()` ; les lignes aberrantes seront retirées dans `load_data()` et leur nombre documenté.

**Découpage.** Version 1 : aléatoire stratifié, 20 % en test, graine 42 (≈ 23 900 réservations de test). Version 2 : chronologique, en construisant une colonne `arrival_date` à partir de l'année, du mois et du jour d'arrivée, puis en gardant les arrivées les plus récentes pour le test. Ce découpage correspond à l'usage réel : prédire de futures réservations à partir du passé.

**Risque principal.** Données de 2015-2017, de deux hôtels portugais : les comportements d'annulation (après le COVID, ailleurs qu'au Portugal) peuvent avoir changé. Le modèle est un démonstrateur, pas un outil prêt pour un hôtel marocain sans données locales.

## 5. Métriques, baseline et critères d'acceptation

**Décision servie.** Chaque matin, le responsable des réservations reçoit la liste des réservations des 30 prochains jours jugées à risque d'annulation, et décide lesquelles relancer (demande de confirmation ou d'acompte).

**Coût des erreurs.**
- Annulation manquée (faux négatif) : chambre vide ou revendue à la dernière minute à prix réduit, soit la perte d'une ou plusieurs nuits (plusieurs centaines de dirhams).
- Fausse alerte (faux positif) : un email ou un appel de relance inutile, quelques minutes de travail et une légère gêne pour le client.
→ Une annulation manquée coûte beaucoup plus cher qu'une fausse alerte.

**Baseline et son score.** Toujours prédire « pas d'annulation » (`DummyClassifier(strategy="most_frequent")`) : accuracy ≈ 0,63, rappel 0 (valeurs exactes à reporter après `python -m monprojet.train`). Elle ne détecte aucune annulation : c'est le niveau à battre.

**Métrique principale, et pourquoi.** Le **rappel** sur la classe « annulée » : la part des annulations réelles que le système signale. C'est l'erreur la plus coûteuse qu'il faut limiter. La **précision** est suivie comme contrainte : si elle est trop basse, l'équipe relance presque tout le monde et le système perd son intérêt. L'accuracy n'est pas utilisée pour décider, car la baseline atteint déjà ≈ 0,63 sans rien détecter.

**Critères d'acceptation.**
1. Rappel ≥ 0,75 sur le jeu de test (20 %, tenu à l'écart, découpage aléatoire stratifié, graine 42).
2. Précision ≥ 0,65 sur le même jeu de test, soit au moins deux relances sur trois justifiées.
3. Rappel supérieur d'au moins 0,50 à celui de la baseline.
4. Contrôle de robustesse : avec le découpage chronologique (arrivées les plus récentes en test), le rappel ne baisse pas de plus de 0,10 par rapport au découpage aléatoire.

## 6. Architecture prévue
## 7. Choix technologiques
## 8. Risques, éthique, confidentialité
## 9. Limites et hors périmètre
