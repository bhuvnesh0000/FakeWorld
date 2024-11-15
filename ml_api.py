import os
import io
from flask import Flask, request, jsonify, send_file
import pandas as pd
from tempfile import NamedTemporaryFile
from ml_service import generate_privacy_preserving_synthetic_data  # Importing from ml_service

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_synthetic_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty file"}), 400
    
    # Check if the file is a CSV
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Invalid file type. Please upload a CSV file."}), 400

    try:
        # Read CSV file
        df = pd.read_csv(file)

        # Generate synthetic data using ml_service function
        synthetic_data = generate_privacy_preserving_synthetic_data(df)

        # Convert the DataFrame to CSV and prepare the response
        output = io.BytesIO()
        synthetic_data.to_csv(output, index=False)
        output.seek(0)

        # Use a temporary file to store the generated synthetic data
        with NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
            temp_file.write(output.getvalue())
            output_path = temp_file.name

        # Return the generated file directly to the user as a download
        return send_file(output, mimetype='text/csv', as_attachment=True, download_name='synthetic_data.csv')

    except Exception as e:
        app.logger.error(f"Error processing the file: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5001, debug=True)
