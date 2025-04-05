from flask import Flask, render_template, request, redirect, url_for, session
import joblib
import numpy as np
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session (language toggle)

# Load model and scaler
model = joblib.load('model/tb_diabetes_model_1.pkl')
scaler = joblib.load('model/scaler_1.pkl')

# Initialize the prediction history database
def init_db():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        gender TEXT,
        bmi REAL,
        blood_pressure REAL,
        glucose REAL,
        hba1c REAL,
        smoking TEXT,
        alcohol TEXT,
        history_tb TEXT,
        diabetes TEXT,
        prediction TEXT,
        probability REAL,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    lang = session.get('lang', 'en')
    return render_template('index.html', lang=lang)

@app.route('/set_language/<lang>')
def set_language(lang):
    session['lang'] = lang
    return redirect(url_for('index'))

from flask import session

@app.route('/predict', methods=['POST'])
def predict():
    try:
        form = request.form
        lang = session.get('lang', 'en')

        input_data = [
            float(form['age']),
            1 if form['gender'] == 'Male' else 0,
            float(form['bmi']),
            float(form['blood_pressure']),
            float(form['glucose_level']),
            float(form['hba1c']),
            1 if form['smoking'] == 'Yes' else 0,
            1 if form['alcohol'] == 'Yes' else 0,
            1 if form['history_tb'] == 'Yes' else 0,
            1 if form['diabetes'] == 'Yes' else 0
        ]

        input_scaled = scaler.transform([input_data])
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0][1]
        risk = "High Risk" if prediction == 1 else "Low Risk"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Dynamic advice based on risk and language
        if prediction == 1:
            advice = (
                "🩺 You're at high risk. Please consult a doctor.\n"
                "🍎 Eat healthy, monitor sugar.\n"
                "🚶‍♂️ Exercise regularly.\n"
            ) if lang == 'en' else (
                "🩺 আপনি উচ্চ ঝুঁকিতে আছেন। দয়া করে ডাক্তারের পরামর্শ নিন।\n"
                "🍎 স্বাস্থ্যকর খাবার খান, শর্করা নিয়ন্ত্রণে রাখুন।\n"
                "🚶‍♂️ নিয়মিত ব্যায়াম করুন।"
            )
        else:
            advice = (
                "✅ You're safe! Keep up a healthy lifestyle."
            ) if lang == 'en' else (
                "✅ আপনি নিরাপদ! স্বাস্থ্যকর জীবনধারা বজায় রাখুন।"
            )

        # Store in DB
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute('''INSERT INTO predictions (
            age, gender, bmi, blood_pressure, glucose, hba1c,
            smoking, alcohol, history_tb, diabetes,
            prediction, probability, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (form['age'], form['gender'], form['bmi'], form['blood_pressure'],
         form['glucose_level'], form['hba1c'], form['smoking'], form['alcohol'],
         form['history_tb'], form['diabetes'], risk,
         round(probability * 100, 2), timestamp))
        conn.commit()
        conn.close()

        # Pass data to result page using session
        session['result_data'] = {
            'prediction': risk,
            'probability': round(probability * 100, 2),
            'advice': advice,
            'timestamp': timestamp,
            'lang': lang
        }

        return redirect(url_for('result'))

    except Exception as e:
        return render_template('index.html', error=str(e), lang=session.get('lang', 'en'))

@app.route('/history')
def history():
    conn = sqlite3.connect('db.sqlite3')
    df = conn.execute("SELECT * FROM predictions ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('history.html', history=df, lang=session.get('lang', 'en'))

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT age, prediction FROM predictions")
    data = c.fetchall()
    conn.close()

    ages = [row[0] for row in data]
    risks = [1 if row[1] == 'High Risk' else 0 for row in data]
    return render_template('dashboard.html', ages=ages, risks=risks, lang=session.get('lang', 'en'))

@app.route('/prevention')
def prevention():
    return render_template('prevention.html', lang=session.get('lang', 'en'))

@app.route('/result')
def result():
    data = session.get('result_data', {})
    return render_template('result.html', **data)

# Optional: custom 404 handler
@app.errorhandler(404)
def not_found(e):
    return f"404 Not Found: {request.path}", 404

if __name__ == '__main__':
    app.run(debug=True)