from __future__ import annotations
from flask import Blueprint, request, jsonify, current_app, url_for
from pathlib import Path
import traceback

from ..services.utils import save_uploaded_file, load_csv, basic_insights
from ..services.data_cleaning import clean_dataframe
from ..services.data_visualization import generate_histograms, generate_correlation_heatmap

insights_bp = Blueprint('insights', __name__)

@insights_bp.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    try:
        saved_path = save_uploaded_file(file)
        df = load_csv(saved_path)
        cleaned = clean_dataframe(df)
        insight = basic_insights(cleaned)
        plots_dir = Path(current_app.config['PLOTS_DIR'])
        hist_files = generate_histograms(cleaned, plots_dir)
        heatmap = generate_correlation_heatmap(cleaned, plots_dir)
        plot_urls = []
        for fname in hist_files:
            plot_urls.append(url_for('static', filename=f'plots/{fname}', _external=True))
        if heatmap:
            plot_urls.append(url_for('static', filename=f'plots/{heatmap}', _external=True))
        return jsonify({
            'filename': saved_path.name,
            'insights': insight,
            'plots': plot_urls
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
