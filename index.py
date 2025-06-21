
from flask import Flask
from flask_cors import CORS
from routes.usuarios import usuarios_bp
from routes.abertura import abertura_bp

#*Isso aqui é toda a parte de conexão no bd.

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


app.register_blueprint(usuarios_bp)
app.register_blueprint(abertura_bp)


if __name__ == "__main__":
    app.run()