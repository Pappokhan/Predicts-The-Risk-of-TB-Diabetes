# 🧠 TB-Diabetes Risk Prediction Web App

An AI-powered web application that predicts the **risk of TB-Diabetes co-morbidity** using basic health and lifestyle inputs. Built with 🐍 Python, Flask, and a Random Forest Classifier trained on a **synthetic dataset** of 2,000 records.

> 🇧🇩 Designed with a bilingual interface (English & বাংলা) to support users in Bangladesh and similar contexts.

---

## 🌟 Features

- ✅ Predict TB-Diabetes co-morbidity risk (High or Low)
- 📊 Show model probability score
- 🗂 Track prediction history with timestamp
- 📈 Dashboard with visual analytics
- 🌐 Language toggle: English ↔ বাংলা
- 🧠 Personalized prevention tips based on prediction
- 💻 Clean, mobile-friendly web UI using Bootstrap

---

## 🧪 How It Works

1. **User inputs** health data:
   - Age, Gender, BMI, Blood Pressure, Glucose, HbA1c
   - Lifestyle: Smoking, Alcohol
   - History: Diabetes, TB

2. **Model prediction** using trained `RandomForestClassifier`

3. **Result display** with:
   - Risk level (High / Low)
   - Confidence score (%)
   - Personalized prevention tips
   - Option to view past predictions

---

## 🛠️ Tech Stack

| Tech | Description |
|------|-------------|
| Python | Core programming language |
| Flask | Web framework |
| Scikit-learn | ML model (Random Forest) |
| SQLite | Lightweight database for history |
| Bootstrap | Frontend styling |
| Chart.js | Visualizations |
| Joblib | Save/load model & scaler |

---

## 📁 Project Structure

<pre>
TB_D_APP/
├── 🧠 <b>app.py</b>                  # Main Flask app (routes, prediction logic)
├── 📁 <b>model/</b>                 
│   ├── tb_diabetes_model_1.pkl   # Trained Random Forest model
│   └── scaler_1.pkl              # StandardScaler for input normalization
├── 📁 <b>templates/</b>             
│   ├── base.html                # Shared layout with navbar
│   ├── index.html               # Input form (bilingual)
│   ├── result.html              # Prediction result page
│   ├── history.html             # Past predictions view
│   └── dashboard.html           # Visual analytics using Chart.js
├── 📁 <b>static/</b>                
│   └── charts.js                # (Optional) JS for charts
├── 🗃️ <b>db.sqlite3</b>              # SQLite database for storing prediction history
├── 📄 <b>requirements.txt</b>         # Required Python packages
└── 📘 <b>README.md</b>                # Project description and instructions
</pre>

