from flask import Blueprint, request, jsonify
from connections.db import db
from controllers.abertura import validar_cracha, listar_aberturas
abertura = db.abertura

abertura_bp = Blueprint("abertura", __name__, url_prefix="/abertura")


@abertura_bp.route("/", methods=["GET", "POST"])
def abertura_handler():
    if request.method == "GET":
        return listar_aberturas()

    elif request.method == "POST":
        return validar_cracha()