from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import the CORS module
import joblib
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model and vectorizer
model_filename = 'svm_model.joblib'
vectorizer_filename = 'count_vectorizer.joblib'  # Assuming you saved the CountVectorizer
loaded_model = joblib.load(model_filename)
vectorizer = joblib.load(vectorizer_filename)

@app.route('/')
def index():
    return render_template('prediction.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        user_input = request.form['user_input']

        # Preprocess the user input using the same CountVectorizer
        user_input_vectorized = vectorizer.transform([user_input])

        # Make a prediction
        prediction = loaded_model.predict(user_input_vectorized)

        # Return the prediction as JSON
        return jsonify({'result': 'SQL Injection Attack Detected!' if prediction[0] == 1 else 'No SQL Injection Attack Detected.'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
