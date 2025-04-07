
from flask import Flask, request, jsonify, send_file
import joblib
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import datetime
import os

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

@app.route("/briefing", methods=["POST"])
def generate_briefing():
    data = request.get_json()
    jour = data["jour"]
    heure = int(data["heure"])
    meteo = data["meteo"]
    evenement = "Oui" if data["evenement"] == 1 else "Non"
    affluence = int(data["prediction"])
    filename = "briefing_{}.pdf".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    filepath = os.path.join("briefings", filename)
    os.makedirs("briefings", exist_ok=True)
    c = canvas.Canvas(filepath, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "📋 Briefing Équipe - Resto IA")
    c.setFont("Helvetica", 12)
    c.drawString(50, 770, f"🗓️ Date : {jour} - {heure}h")
    c.drawString(50, 750, f"🌤️ Météo prévue : {meteo}")
    c.drawString(50, 730, f"🎉 Événement local : {evenement}")
    c.drawString(50, 710, f"👥 Affluence estimée : {affluence} clients")
    c.drawString(50, 690, f"📣 Consignes :")
    c.drawString(70, 670, "- Vérifier staffing sur les heures de rush.")
    c.drawString(70, 650, "- Proposer formule rapide si affluence élevée.")
    c.drawString(70, 630, "- Prévoir couverts supplémentaires.")
    c.save()
    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
