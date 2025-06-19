from flask import Blueprint, request, jsonify
from connections.db import db
from controllers.usuarios import listar_usuarios, cadastrar_usuario, editar_usuario, deletar_usuario

usuarios = db.usuarios

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@usuarios_bp.route("/", methods=["GET", "POST"])
def usuarios_handler():
    if request.method == "GET":
        return listar_usuarios()

    elif request.method == "POST":
        return cadastrar_usuario()

@usuarios_bp.route("/<uid>", methods=["PUT", "DELETE"])
def usuario_unico(uid):
    if request.method == "PUT":
        return editar_usuario(uid)

    elif request.method == "DELETE":
        return deletar_usuario(uid)