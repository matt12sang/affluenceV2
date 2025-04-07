# Resto IA – API de prédiction d'affluence + briefing

Ce projet est une API Flask déployable sur Railway 🚄  
Elle prédit l'affluence dans un restaurant selon :
- le jour
- l’heure
- la météo
- la présence d’un événement

## Routes disponibles

### `POST /predict`
Prévoit l’affluence estimée à partir d’un JSON comme :
```json
{
  "jour": "Samedi",
  "heure": 20,
  "meteo": "Soleil",
  "evenement": 1
}
```

### `POST /briefing`
Génère un PDF briefing de l’équipe, avec météo + estimation + consignes.

## Déploiement Railway

1. Uploade ce dossier sur GitHub
2. Va sur https://railway.app → New Project → Deploy from GitHub
3. Railway détectera le `.railway` + `affluence_api`
4. Done 🚀

