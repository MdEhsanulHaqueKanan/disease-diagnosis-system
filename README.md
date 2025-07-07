# NLP-Powered Disease Diagnosis System

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-black?style=for-the-badge&logo=flask)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

This project is an end-to-end web application that leverages Natural Language Processing to assist users in identifying potential diseases based on their described symptoms. It uses a state-of-the-art Sentence-Transformer model to understand the semantic meaning of symptoms, providing more accurate and context-aware results than simple keyword matching.

The entire application is built with a production-ready mindset, separating the data science development (in a Jupyter Notebook) from the deployed Flask application, ensuring efficiency and maintainability.

---

## ► Live Demo

**[► View Live Demo](https://your-render-app-url.onrender.com)**  
*(Note: The first load might be slow if the service is on a free tier and needs to spin up.)*

---

## 📸 Application Preview

![App Demo Screenshot](./app_ss_1.png)

---

## ✨ Key Features

*   **Semantic Symptom Search:** Utilizes a Sentence-Transformer model (`all-MiniLM-L6-v2`) to understand the *meaning* of user input, not just keywords. It can associate "head pain" with "headache," for example.
*   **Ranked Results with Confidence Score:** Returns the top 5 most likely diseases, ranked by their cosine similarity score, giving users a sense of the model's confidence.
*   **Clean, Responsive UI:** A modern and intuitive user interface built with vanilla HTML, CSS, and JavaScript that provides a seamless user experience.
*   **Production-Ready Backend:** A robust Flask API that loads the ML model artifacts once at startup for maximum performance and handles requests efficiently.

---

## 🛠️ Tech Stack

### **Data Science & Machine Learning**
*   **Python:** Core programming language.
*   **Pandas:** For data manipulation and analysis.
*   **Sentence-Transformers:** For generating high-quality semantic embeddings.
*   **Scikit-learn:** For calculating cosine similarity.
*   **Jupyter Notebook:** For an interactive development environment for EDA and model processing.

### **Backend**
*   **Flask:** A lightweight web framework for building the API.
*   **Gunicorn:** A production-grade WSGI server.
*   **Flask-Cors:** To handle Cross-Origin Resource Sharing.

### **Frontend**
*   **HTML5, CSS3, JavaScript:** Standard web technologies for the user interface.

---

## 🏛️ Project Architecture

This project follows a professional, industry-standard architecture that separates concerns for maintainability and scalability.

```
disease_diagnosis_app/
│
├── notebook/
│   └── data_exploration_and_modeling.ipynb  # The notebook for all data science work
│
├── model_artifacts/
│   ├── processed_diseases.parquet   # Pre-processed data for fast loading
│   └── symptom_embeddings.npy       # Pre-computed model embeddings
│
├── static/
│   └── styles.css                   # All application styles
│
├── templates/
│   └── index.html                   # The main HTML page
│
├── .gitignore                       # Specifies intentionally untracked files
├── app.py                           # The Flask application backend
└── requirements.txt                 # Project dependencies
```

### **The "Two-Phase" Philosophy**
1.  **Phase 1 (Development - The Notebook):** The `data_exploration_and_modeling.ipynb` notebook is used for all heavy-lifting. It handles data loading, cleaning, EDA, and the computationally expensive process of generating embeddings. Its final output is the lightweight, ready-to-use **model artifacts**.
2.  **Phase 2 (Production - The Flask App):** The `app.py` is a lightweight server. It does **not** re-run any data science processes. It simply loads the pre-computed artifacts from `model_artifacts/` once at startup and uses them to serve predictions quickly. This separation is a core MLOps principle.

---

## 🚀 Running the Project Locally

To run this application on your local machine, follow these steps:

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/MdEhsanulHaqueKanan/disease-diagnosis-system.git
    cd your-repo-name
    ```

2.  **Create and Activate a Virtual Environment**
    ```bash
    # Create the virtual environment
    python -m venv venv

    # Activate it (on Windows)
    venv\Scripts\activate

    # Activate it (on macOS/Linux)
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    (venv) pip install -r requirements.txt
    ```

4.  **Run the Flask Application**
    ```bash
    (venv) python app.py
    ```

5.  **Access the Application**
    Open your web browser and navigate to `http://127.0.0.1:5000`.

