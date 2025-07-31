from flask import Blueprint, request, jsonify
from connections.db import db
from controllers.abertura import envia_formulario
status_abertura = db.status_abertura

valida_abertura_bp = Blueprint("status_abertura", __name__, url_prefix="/status_abertura")


@valida_abertura_bp.route("/", methods=["POST"])
def abertura_handler():
        return envia_formulario()