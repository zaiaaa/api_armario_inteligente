from flask import Blueprint, request, jsonify
from connections.db import db
from controllers.abertura import excluir_status_abertura, lista_status, envia_formulario_retirada, listar_lockouts, envia_formulario_devolucao
status_abertura = db.status_abertura

valida_abertura_bp = Blueprint("status_abertura", __name__, url_prefix="/status_abertura")


@valida_abertura_bp.route("/", methods=["GET"])
def visualizar():
        return listar_lockouts()

@valida_abertura_bp.route("/status", methods=["GET"])
def status():
        return lista_status()

@valida_abertura_bp.route("/retirada", methods=["POST"])
def retirada():
                return envia_formulario_retirada()
        
@valida_abertura_bp.route("/devolucao", methods=["POST"])
def devolucao():
        return envia_formulario_devolucao()

@valida_abertura_bp.route("/status/reset", methods=["DELETE"])
def status_reset():
        return excluir_status_abertura()
