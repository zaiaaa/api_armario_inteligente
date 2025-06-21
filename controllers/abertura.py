from connections.db import db
from flask import jsonify, request
from datetime import datetime

abertura = db.abertura

def cadastrar_abertura():
    dados = request.get_json()
    if "id_colaborador" not in dados:
        return jsonify({"erro": "Obrigatório id do colaborador."})
    hora_atual = datetime.now()

    queryFinal = {
        "id_colaborador": dados["id_colaborador"],
        "hora_abertura": hora_atual
    }

    try:
        abertura.insert_one(queryFinal)
        return jsonify({"mensagem": "Abertura registrada com sucesso."}), 201
    except Exception as e:
        return jsonify({"mensagem": f"Erro -> {str(e)}"}), 400

def listar_aberturas():
    aberturas = list(abertura.find({}, {"_id": 0}))
    return jsonify(aberturas)
    