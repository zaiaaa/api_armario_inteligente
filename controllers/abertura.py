from connections.db import db
from flask import jsonify, request
from datetime import datetime

abertura = db.abertura
usuarios = db.usuarios

# isso aqui vai virar um "VALIDAR TEAM MEMBER". vai verificar se o paizao ta pesente na lista de cadastro. Se estiver, retorna 200 e é cadastrada a INTENÇÃO de abertura do armário.
def cadastrar_abertura():
    dados = request.get_json()   
    
    if "UID" not in dados:
        return jsonify({"erro": "Obrigatório UID do crachá do colaborador."})
    hora_atual = datetime.now()

    usuario = usuarios.find_one({"UID": dados["UID"]})
    print(usuario)
    if not usuario:
        return jsonify({"mensagem": "Acesso negado."}), 403


    queryFinal = {
        "UID": dados["UID"],
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
        usuario = usuarios.find_one({"UID": ab["UID"]}, {"_id": 0, "nome": 1, "id_colaborador": 1})
        nome = usuario["nome"] if usuario else "Desconhecido"
        id_colaborador = usuario["id_colaborador"] if usuario else "sem ID"
        
        print(ab)
        print(usuario)

        aberturas_formatadas.append({
            "UID": ab["UID"],
            "nome": nome,
            "id_colaborador": id_colaborador,
            "hora_abertura": ab["hora_abertura"]
        })

    return jsonify(aberturas_formatadas)
    
