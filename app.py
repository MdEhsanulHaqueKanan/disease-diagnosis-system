# --- Imports ---
import os
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# --- Initialize the Flask App ---
app = Flask(__name__)
# Enable CORS for smooth cross-origin requests from the frontend
CORS(app)

# --- Load Model Artifacts (Done ONCE at startup) ---
# This is a key best practice: load models and data only once when the app starts.
# This makes every subsequent prediction much faster.
MODEL_DIR = './model_artifacts'

try:
    # Load the processed DataFrame
    symptoms_df = pd.read_parquet(os.path.join(MODEL_DIR, 'processed_diseases.parquet'))
    
    # Load the embeddings
    symptom_embeddings = np.load(os.path.join(MODEL_DIR, 'symptom_embeddings.npy'))
    
    # Load the Sentence Transformer model
    # model = SentenceTransformer('all-MiniLM-L6-v2')

    # New Line Added
    # We are using a smaller model to fit within Render's free tier memory limits.
    model = SentenceTransformer('all-MiniLM-L12-v1') # A slightly different, but still good model
    
    print("✅ Model artifacts loaded successfully!")

except FileNotFoundError:
    print("❌ Error: Model artifacts not found. Make sure the 'model_artifacts' directory and its contents are in the correct location.")
    # In a real scenario, you might want to exit or handle this more gracefully.
    model = None
    symptoms_df = None
    symptom_embeddings = None

# --- Helper Functions ---
def preprocess_text(text):
    """A simple function to preprocess text for the model."""
    return text.lower().strip()

def find_top_diseases(query, top_k=5):
    """
    Core diagnosis function. Encapsulates the logic from the notebook.
    """
    if model is None or symptoms_df is None:
        return []

    # Preprocess and encode the user's query
    query_processed = preprocess_text(query)
    query_embedding = model.encode(query_processed)
    
    # Calculate similarities and find top matches
    similarities = cosine_similarity([query_embedding], symptom_embeddings).flatten()
    top_k_indices = np.argsort(similarities)[::-1][:top_k]
    
    results = []
    for idx in top_k_indices:
        row = symptoms_df.iloc[idx]
        results.append({
            'Name': row['Name'],
            'Symptoms': row['Symptoms'],
            'Treatments': row['Treatments'],
            'Contagious': bool(row['Contagious']), # Ensure JSON-compatible types
            'Chronic': bool(row['Chronic']),     # Ensure JSON-compatible types
            'Similarity': round(float(similarities[idx]), 4)
        })
    return results

# --- Define API Routes ---
@app.route('/')
def home():
    """
    Serves the main HTML page of the application.
    """
    return render_template('index.html')

@app.route('/healthz')
def health_check():
    """A simple health check endpoint for Render."""
    return "OK", 200
@app.route('/predict', methods=['POST'])
def predict():
    """
    The main prediction endpoint. It receives a user query, finds matching
    diseases, and returns them as JSON.
    """
    # Get the JSON data from the request
    data = request.get_json()
    
    if not data or 'symptoms' not in data:
        return jsonify({'error': 'Invalid input. "symptoms" key is required.'}), 400
        
    query = data['symptoms']
    top_k = data.get('top_k', 5) # Allow frontend to specify top_k, default to 5
    
    # Get the predictions
    predictions = find_top_diseases(query, top_k)
    
    # Return the results as a JSON response
    return jsonify(predictions)

# --- Run the App ---
if __name__ == '__main__':
    # Use host='0.0.0.0' to make the app accessible on your local network
    app.run(debug=True, host='0.0.0.0')