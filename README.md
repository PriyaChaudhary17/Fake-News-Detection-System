# 📰 Nepali Fake News Detection System

## BEIT – Minor Project

**Bachelor of Engineering in Information Technology (BEIT)**
**Minor Project**

### 👥 Project Members

1. Aditi Karn
2. Neha Kumari
3. Manav Piya
4. Udesh Maharjan
5. Priya Chaudhary Kurmi

   
**Project Supervisor:** Basantraj Phulara
**Institution:** Cosmos College Of Management And Technology
**Academic Year:** 2026

---

## 📌 Project Overview

The **Nepali Fake News Detection System** is a web-based application developed as a **BEIT Minor Project** to identify whether a given Nepali news article or news text is **Real or Fake** using Machine Learning and Natural Language Processing (NLP).

The system supports both **text-based and URL-based news analysis** and provides prediction confidence, analysis reasons, and a history of previously analyzed news.

The primary objective of this project is to develop an accessible system that can assist users in identifying potentially misleading or fabricated Nepali news content.

---

## 🎯 Project Objectives

* To develop an automated Nepali fake news detection system.
* To apply NLP techniques for processing Nepali news text.
* To train and evaluate Machine Learning classification models.
* To classify news as **REAL** or **FAKE**.
* To provide confidence scores for predictions.
* To support both text and URL-based analysis.
* To maintain analysis history using MongoDB.
* To develop a simple and user-friendly web interface.
* To demonstrate the practical application of Machine Learning in misinformation detection.

---

## ✨ Key Features

* 📰 Nepali fake news classification
* 📝 Text-based news analysis
* 🔗 URL-based news analysis
* 🤖 Machine Learning prediction
* 📊 Confidence score
* 🔍 Prediction reasons/indicators
* 📚 Analysis history
* 🗄️ MongoDB database
* 🌐 Flask REST API
* ⚛️ React frontend
* ⚠️ Input validation and error handling
* 📱 Responsive user interface

---

## 🛠️ Technologies Used

### Frontend

* React.js
* JavaScript
* HTML5
* CSS3
* React Router
* Axios

### Backend

* Python
* Flask
* Flask-CORS
* REST API

### Machine Learning & NLP

* Scikit-learn
* Pandas
* NumPy
* NLTK
* TF-IDF Vectorization
* Logistic Regression
* Random Forest
* XGBoost
* Multinomial Naive Bayes

### BEIT Project Components

The project integrates concepts from:

* Artificial Intelligence
* Machine Learning
* Natural Language Processing
* Web Technology
* Database Management
* Software Engineering

### Database

* MongoDB
* MongoDB Compass

### Development Tools

* Visual Studio Code
* Git
* GitHub
* Postman

---

## 🤖 Machine Learning Approach

The system follows a complete NLP and Machine Learning pipeline:

```text
News Dataset
     ↓
Data Cleaning
     ↓
Text Preprocessing
     ↓
Feature Extraction
     ↓
TF-IDF Vectorization
     ↓
Model Training
     ↓
Model Evaluation
     ↓
Best Model Selection
     ↓
Prediction
     ↓
REAL / FAKE
```

### Models Evaluated

Several Machine Learning algorithms were evaluated:

1. Logistic Regression
2. Random Forest
3. XGBoost
4. Multinomial Naive Bayes

Based on the evaluation results, **Logistic Regression** was selected as the primary text classification model.

---

## 📊 Model Evaluation

The models were evaluated using:

* Accuracy
* Precision
* Recall
* F1 Score
* Confusion Matrix

The final Logistic Regression model achieved approximately:

| Metric   |      Score |
| -------- | ---------: |
| Accuracy | **96.33%** |
| F1 Score | **96.20%** |

---

## 📂 Project Structure

```text
FakeNewsDetection/
│
├── backend/
│   ├── __init__.py
│   ├── app.py
│   │
│   ├── database/
│   │   └── db.py
│   │
│   ├── ml/
│   │   ├── text_utils.py
│   │   ├── predict_text.py
│   │   └── ...
│   │
│   ├── models/
│   │   └── ...
│   │
│   ├── search/
│   │   └── ...
│   │
│   └── verification/
│       └── ...
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── ...
│   └── package.json
│
├── dataset/
│   └── ...
│
├── models/
│   ├── text_model.pkl
│   ├── tfidf_vectorizer.pkl
│   └── label_encoder.pkl
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation and Setup

### Prerequisites

Make sure the following are installed:

* Python 3.x
* Node.js
* npm
* MongoDB
* Git

### Backend

```bash
cd FakeNewsDetection
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
python -m backend.app
```

Backend:

```text
http://127.0.0.1:5000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## 🗄️ Database

The system uses MongoDB for storing prediction history.

**Database:**

```text
fake_news_db
```

**Collection:**

```text
predictions
```

Each prediction may contain:

```json
{
  "text": "News article text",
  "prediction": "REAL",
  "confidence": 95.42,
  "timestamp": "2026-08-09T..."
}
```

---

## 🔌 API Endpoints

### API Status

```http
GET /
```

### News Prediction

```http
POST /predict
```

Example:

```json
{
  "text": "नेपाल सरकारले नयाँ नीति सार्वजनिक गरेको छ।"
}
```

### Analysis History

```http
GET /history
```

---

## 🔗 URL Analysis

The system can also analyze news through a URL.

```text
News URL
   ↓
URL Validation
   ↓
News Content Extraction
   ↓
Text Preprocessing
   ↓
TF-IDF Vectorization
   ↓
Machine Learning Model
   ↓
Prediction
   ↓
REAL / FAKE
```

---

## 📈 System Workflow

```text
                 USER
                   │
          ┌────────┴────────┐
          │                 │
      NEWS TEXT         NEWS URL
          │                 │
          │          Extract Content
          │                 │
          └────────┬────────┘
                   ↓
          Text Preprocessing
                   ↓
            TF-IDF Features
                   ↓
          Logistic Regression
                   ↓
            ┌──────┴──────┐
            ↓             ↓
          REAL           FAKE
            │             │
            └──────┬──────┘
                   ↓
           Confidence Score
                   ↓
             MongoDB
                   ↓
             History Page
```

---

## ⚠️ Limitations

The system is an automated prediction tool and does not guarantee that every prediction is factually correct.

Performance can be affected by:

* Dataset quality
* Dataset diversity
* News writing style
* New or unseen topics
* Changes in misinformation patterns
* Availability of content from URLs

Therefore, the system should be used as an **assistive tool for news verification**, rather than as a replacement for professional fact-checking.

---

## 🚀 Future Enhancements

Future improvements may include:

* Nepali BERT / transformer-based models
* **BEIT-compatible deep learning experimentation**
* Real-time news monitoring
* Browser extension
* Multilingual fake news detection
* Improved source credibility analysis
* Explainable AI
* User authentication
* Cloud deployment
* Mobile application
* Improved URL verification
* Real-time database analytics

---

## 👥 Project Team

### BEIT – Minor Project

**Project Title:** Nepali Fake News Detection System

**Members:**

1. Aditi Karn
2. Neha Kumari
3. Manav Piya
4. Udesh Maharjan
5. Priya Chaudhary Kurmi

   
**Project Supervisor:** Basantraj Phulara
**Institution:** Cosmos College Of Management And Technology

**Program:** Bachelor of Engineering in Information Technology (BEIT)

**Project Type:** Minor Project(6th Semester)

**Academic Year:** 2026

---

## 📜 License

This project is developed for **academic and educational purposes** as part of the BEIT Minor Project.

---

## ⭐ Acknowledgement

This project was developed as part of the **Bachelor of Engineering in Information Technology (BEIT) Minor Project** to explore the practical application of **Machine Learning, Natural Language Processing, Web Development, and Database Technologies** in detecting potentially misleading Nepali news.

---

**© 2026 BEIT Minor Project – Nepali Fake News Detection System**
