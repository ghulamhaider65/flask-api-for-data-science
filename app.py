import os
from flask_data_insight_api.app import create_app

app = create_app()

if __name__ == '__main__':
    # Allow GitHub Codespaces / cloud platforms to override port
    port = int(os.environ.get('PORT', '8000'))
    print(f"Starting AI-Powered Data Insight API on 0.0.0.0:{port} (set PORT env var to change)")
    app.run(host='0.0.0.0', port=port, debug=False)
