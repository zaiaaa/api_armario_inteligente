from connections.db import db
from flask import jsonify, request

usuarios = db.usuarios

def busca_master_uid():
    dados = request.get_json()
    if "UID" not in dados:
        return jsonify({"erro": "UID é obrigatório"}), 400

    if usuarios.find_one({"UID": dados["UID"]}):
        return jsonify({"mensagem": "Master OK"}), 201
    else:
        return jsonify({"erro": "Master Não encontrada"}), 403

