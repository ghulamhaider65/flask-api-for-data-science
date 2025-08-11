from __future__ import annotations
from flask import Blueprint, render_template, request, current_app
from pathlib import Path
import traceback

from ..services.utils import save_uploaded_file, load_csv, basic_insights
from ..services.data_cleaning import clean_dataframe
from ..services.data_visualization import generate_histograms, generate_correlation_heatmap
from ..services.model_training import train_simple_model, TARGET_COLUMN

ui_bp = Blueprint('ui', __name__)

@ui_bp.route('/ui', methods=['GET', 'POST'])
def ui_index():
    context = {}
    if request.method == 'POST':
        file = request.files.get('file')
        run_model = request.form.get('run_model') == 'on'
        try:
            if not file or file.filename == '':
                context['error'] = 'Please choose a CSV file.'
            else:
                saved_path = save_uploaded_file(file)
                df = load_csv(saved_path)
                cleaned = clean_dataframe(df)
                insight = basic_insights(cleaned)
                plots_dir = Path(current_app.config['PLOTS_DIR'])
                hist_files = generate_histograms(cleaned, plots_dir)
                heatmap = generate_correlation_heatmap(cleaned, plots_dir)
                plot_urls = [f"/static/plots/{f}" for f in hist_files]
                if heatmap:
                    plot_urls.append(f"/static/plots/{heatmap}")
                context.update({
                    'filename': saved_path.name,
                    'insights': insight,
                    'plot_urls': plot_urls,
                })
                if run_model:
                    if TARGET_COLUMN in cleaned.columns:
                        model_res = train_simple_model(cleaned)
                        model_res.pop('model', None)
                        context['model_result'] = model_res
                    else:
                        context['model_result'] = {'trained': False, 'reason': f"No column named '{TARGET_COLUMN}' found. Model training skipped."}
        except Exception as e:
            import traceback
            traceback.print_exc()
            context['error'] = str(e)
    return render_template('index.html', **context)
