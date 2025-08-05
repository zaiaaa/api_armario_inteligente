from flask import Blueprint, request, jsonify
from connections.db import db
from controllers.abertura import envia_formulario_retirada, listar_lockouts, envia_formulario_devolucao
status_abertura = db.status_abertura

valida_abertura_bp = Blueprint("status_abertura", __name__, url_prefix="/status_abertura")


@valida_abertura_bp.route("/", methods=["GET"])
def visualizar():
        return listar_lockouts()

@valida_abertura_bp.route("/retirada", methods=["POST"])
def retirada():
                return envia_formulario_retirada()
        
@valida_abertura_bp.route("/devolucao", methods=["POST"])
def devolucao():
        return envia_formulario_devolucao()
