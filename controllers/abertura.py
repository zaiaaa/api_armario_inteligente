from connections.db import db
from flask import jsonify, request
from datetime import datetime

abertura = db.abertura
status_abertura = db.status_abertura
usuarios = db.usuarios
lockout = db.lockout

def validar_cracha():
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
        "status": False
    }

    try:
        status_abertura.insert_one(queryFinal)
        return jsonify({"mensagem": "Aguardando preenchimento do Formulário."}), 201
    except Exception as e:
        return jsonify({"mensagem": f"Erro -> {str(e)}"}), 400


def envia_formulario():
    dados = request.get_json()    

    try: 
        db.status_abertura.update_one(
        {"UID": dados["UID"]},
        {"$set": {"status": True}}
        )

        db.lockout.update_one(
        {"tag": dados["tag"]},
        {"$set":  {
            "status": dados["status"],
            "local": dados["local"],
            "UID": dados["UID"],
            "hora_retirada": datetime.now()
        }}
        )

        db.status_abertura.delete_one({"UID": dados["UID"]})


        return {"status": "Formulario preenchido e trava Aberta!"}
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
    