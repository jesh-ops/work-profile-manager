import os

from app import create_app

config_name = os.environ.get("FLASK_CONFIG")
if not config_name:
    config_name = "production" if os.environ.get("FLASK_ENV") == "production" else "development"

app = create_app(config_name)

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)
