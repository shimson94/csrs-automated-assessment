from flask import Flask
from flask_cors import CORS
from src.api.routes import api_blueprint

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for frontend-backend communication

# Register the API blueprint
app.register_blueprint(api_blueprint, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
