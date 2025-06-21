from connections.db import db
from flask import jsonify, request
from datetime import datetime

abertura = db.abertura
usuarios = db.usuarios

def cadastrar_abertura():
    dados = request.get_json()   
    
    if "id_colaborador" not in dados:
        return jsonify({"erro": "Obrigatório id do colaborador."})
    hora_atual = datetime.now()

    usuario = usuarios.find_one({"id_colaborador": dados["id_colaborador"]})
    print(usuario)
    if not usuario:
        return jsonify({"mensagem": "Acesso negado."}), 403


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
    aberturas = abertura.find({})

    print(aberturas)

    aberturas_formatadas = []

    for ab in aberturas:
        usuario = usuarios.find_one({"id_colaborador": ab["id_colaborador"]}, {"_id": 0, "nome": 1})
        nome = usuario["nome"] if usuario else "Desconhecido"
        
        aberturas_formatadas.append({
            "id_colaborador": ab["id_colaborador"],
            "nome": nome,
            "hora_abertura": ab["hora_abertura"]
        })

    return jsonify(aberturas_formatadas)
    