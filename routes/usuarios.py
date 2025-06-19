from flask import Blueprint, request, jsonify
from connections.db import db

usuarios = db.usuarios

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@usuarios_bp.route("/", methods=["GET", "POST"])
def usuarios_handler():
    if request.method == "GET":
        lista = list(usuarios.find({}, {"_id": 0}))
        return jsonify(lista), 200

    elif request.method == "POST":
        dados = request.get_json()
        if "UID" not in dados:
            return jsonify({"erro": "UID é obrigatório"}), 400

        if usuarios.find_one({"UID": dados["UID"]}):
            return jsonify({"erro": "UID já cadastrado"}), 409

        usuarios.insert_one(dados)
        return jsonify({"mensagem": "Usuário cadastrado"}), 201

@usuarios_bp.route("/<uid>", methods=["PUT", "DELETE"])
def usuario_unico(uid):
    if request.method == "PUT":
        dados = request.get_json()
        res = usuarios.update_one({"UID": uid}, {"$set": dados})
        if res.matched_count == 0:
            return jsonify({"erro": "Usuário não encontrado"}), 404
        return jsonify({"mensagem": "Atualizado com sucesso"}), 200

    elif request.method == "DELETE":
        res = usuarios.delete_one({"UID": uid})
        if res.deleted_count == 0:
            return jsonify({"erro": "Usuário não encontrado"}), 404
        return jsonify({"mensagem": "Deletado com sucesso"}), 200