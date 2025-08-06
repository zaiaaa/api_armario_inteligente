from connections.db import db
from flask import jsonify, request
from datetime import datetime

usuarios = db.usuarios

def listar_usuarios():
    lista = list(usuarios.find({}, {"_id": 0}))
    return jsonify(lista), 200

def cadastrar_usuario():
    dados = request.get_json()
    if "UID" not in dados:
        return jsonify({"erro": "UID é obrigatório"}), 400

    if usuarios.find_one({"UID": dados["UID"]}):
        return jsonify({"erro": "UID já cadastrado"}), 409
    dados["hora_cadastro"] = datetime.now()

    usuarios.insert_one(dados)
    return jsonify({"mensagem": "Usuário cadastrado"}), 201

def listar_usuario_uid(uid):
    usuario = usuarios.find_one({"UID": uid}, {"_id": 0})
    print("entrou usuario unico")
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    return jsonify(usuario), 200


def editar_usuario(uid):
    dados = request.get_json()
    res = usuarios.update_one({"UID": uid}, {"$set": dados})
    if res.matched_count == 0:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    return jsonify({"mensagem": "Atualizado com sucesso"}), 200

def deletar_usuario(uid):
    res = usuarios.delete_one({"UID": uid})
    if res.deleted_count == 0:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    return jsonify({"mensagem": "Deletado com sucesso"}), 200