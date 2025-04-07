
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

model = joblib.load("model.pkl")
le_jour = joblib.load("le_jour.pkl")
le_meteo = joblib.load("le_meteo.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    jour = le_jour.transform([data["jour"]])[0]
    meteo = le_meteo.transform([data["meteo"]])[0]
    heure = int(data["heure"])
    evenement = int(data["evenement"])
    X = [[jour, heure, meteo, evenement]]
    prediction = model.predict(X)[0]
    return jsonify({"prediction": round(prediction)})



@app.route("/", methods=["GET"])
def home():
    return "🚀 API Resto IA opérationnelle ! Utilisez /predict ou /briefing."


if __name__ == "__main__":
    app.run(debug=True)
