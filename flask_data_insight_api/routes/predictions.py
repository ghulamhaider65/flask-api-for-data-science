from __future__ import annotations
from flask import Blueprint, request, jsonify
from ..services.utils import save_uploaded_file, load_csv
from ..services.data_cleaning import clean_dataframe
from ..services.model_training import train_simple_model
import traceback

predictions_bp = Blueprint('predictions', __name__)

@predictions_bp.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    try:
        path = save_uploaded_file(file)
        df = load_csv(path)
        df = clean_dataframe(df)
        result = train_simple_model(df)
        if not result.get('trained'):
            return jsonify({'model': result}), 200
        # Remove non-serializable objects
        result.pop('model', None)
        return jsonify({'model': result})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
