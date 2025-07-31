
from flask import Flask
from flask_cors import CORS
from routes.usuarios import usuarios_bp
from routes.abertura import abertura_bp
from routes.master import master_bp
from routes.valida_abertura import valida_abertura_bp
import os
#*Isso aqui é toda a parte de conexão no bd.

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


app.register_blueprint(usuarios_bp)
app.register_blueprint(abertura_bp)
app.register_blueprint(master_bp)
app.register_blueprint(valida_abertura_bp)

@app.route("/", methods=["GET"])
def index():
    return "API ONLINE"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000));
    app.run(host='0.0.0.0', port=port)