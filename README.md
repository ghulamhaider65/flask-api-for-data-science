
# AI-Powered Data Insight API (Portfolio Project)

>A modern Flask web app for data science portfolios: upload CSVs, get instant insights, visualizations, and (optionally) train a machine learning model—all in a beautiful UI.

---

## 🚀 Features
- **Upload CSV** via web UI or `/upload` API
- **Automatic data cleaning** (numeric NaNs → median, categorical NaNs → mode)
- **Data insights**: row/column counts, null counts, dtypes
- **Visualizations**: histograms (all numeric columns), correlation heatmap
- **Model training**: trains a RandomForestClassifier **only if your CSV has a column named `target`**
- **Model performance**: shows accuracy, features, and row count
- **/ui**: Modern, responsive web interface (portfolio-ready)
- **/predict**: API endpoint for model training (if `target` column exists)
- **/health**: Liveness check

---

## 🧠 How Model Training Works
- If your uploaded CSV has a column named **`target`** (case-sensitive):
  - The system uses it as the label for training a RandomForestClassifier.
  - All other numeric columns are used as features.
  - Model accuracy is shown in the UI and API response.
- If there is **no `target` column**:
  - No model is trained.
  - You still get insights and plots.
  - The UI will show a friendly message explaining why.

**Tip:** To enable model training, make sure your CSV has a column named `target` (e.g. `feature1,feature2,target`).

---

## 🖥️ Using the Web UI
1. Start the server:
   ```bash
   python app.py
   # or: /workspaces/codespaces-blank/.venv/bin/python app.py
   ```
2. In GitHub Codespaces, open the Ports panel. Click the forwarded URL for the running port and add `/ui` at the end. Example:
  `https://<forwarded-id>.githubpreview.dev/ui`
3. Upload your CSV file.
4. (Optional) Check "Train model" if your CSV has a `target` column.
5. Click Process. View insights, plots, and (if trained) model accuracy.

---

## 🛠️ API Endpoints

**/upload** (POST):
```bash
curl -X POST -F "file=@yourdata.csv" http://localhost:8000/upload
```
Returns: filename, insights, plots (URLs)

**/predict** (POST, needs `target` column):
```bash
curl -X POST -F "file=@yourdata_with_target.csv" http://localhost:8000/predict
```
Returns: model accuracy and metadata if trained, or a message if not.

**/health** (GET):
```bash
curl http://localhost:8000/health
```

---

## 📁 Project Structure
```
flask_data_insight_api/
  app.py
  config.py
  requirements.txt
  services/
    data_cleaning.py
    data_visualization.py
    model_training.py
    utils.py
  routes/
    insights.py
    predictions.py
    health.py
    ui.py
  static/plots/
  static/style.css
  data/
  templates/
    base.html
    index.html
```

---

## ⚡ Example Response (`/upload`)
```json
{
  "filename": "example.csv",
  "insights": {
    "rows": 150,
    "columns": 5,
    "null_counts": {"col1": 0},
    "dtypes": {"col1": "float64"}
  },
  "plots": [
    "http://localhost:8000/static/plots/hist_col1.png",
    "http://localhost:8000/static/plots/correlation_heatmap.png"
  ]
}
```

---

## 📝 Notes
- Only `.csv` uploads allowed (10 MB limit).
- Correlation heatmap generated only if >=2 numeric columns.
- Model training returns accuracy and metadata if successful.
- If no `target` column, model training is skipped and UI explains why.

---

## 🌐 Deployment
- Free deploy: [Render.com](https://render.com/docs/deploy-flask), Railway, Fly.io, etc.
- See code comments for production tips (gunicorn, Procfile, etc.)

---


## 👤 Author
Portfolio project by ghulamhaider65

---
Enjoy building with the AI-Powered Data Insight API! 🎉
