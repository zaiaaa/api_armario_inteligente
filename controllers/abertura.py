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

    #trocar essa query para o cadastro na intenção de abertura.
    queryFinal = {
        "UID": dados["UID"],
        "status": False
    }

    try:
        status_abertura.insert_one(queryFinal)
        return jsonify({"mensagem": "Aguardando preenchimento do Formulário."}), 201
    except Exception as e:
        return jsonify({"mensagem": f"Erro -> {str(e)}"}), 400


def envia_formulario_retirada():
    dados = request.get_json()    

    try: 
        lock = db.lockout.find_one({"tag": dados["tag"]})
        if lock and lock.get("status") == "retirado":
            return jsonify({"erro": "Este lockout já foi retirado!"}), 400


        db.status_abertura.update_one(
        {"UID": dados["UID"]},
        {"$set": {"status": True}}
        )

        db.lockout.update_one(
        {"tag": dados["tag"]},
        {"$set":  {
            "status": "retirado",
            "local": dados["local"],
            "UID": dados["UID"],
            "hora_retirada": datetime.now()
        }}
        )

        #db.status_abertura.delete_one({"UID": dados["UID"]})


        return {"status": "Formulario de retirada preenchido e trava Aberta!"}
    except Exception as e:
        return jsonify({"mensagem": f"Erro -> {str(e)}"}), 400

def envia_formulario_devolucao():
    dados = request.get_json()    

    try: 
        lock = db.lockout.find_one({"tag": dados["tag"]})
        if lock and lock.get("status") == "devolvido":
            return jsonify({"erro": "Este lockout já foi devolvido!"}), 400
        
        db.status_abertura.update_one(
        {"UID": dados["UID"]},
        {"$set": {"status": True}}
        )

        db.lockout.update_one(
        {"tag": dados["tag"]},
        {"$set":  {
            "status": "devolvido",
            "local": "",
        }}
        )

        #db.status_abertura.delete_one({"UID": dados["UID"]})


        return {"status": "Formulario de devolução preenchido e trava Aberta!"}
    except Exception as e:
        return jsonify({"mensagem": f"Erro -> {str(e)}"}), 400

def listar_lockouts():
    lockouts = db.lockout.find({})

    lockouts_formatados = []

    for lock in lockouts:
        usuario = usuarios.find_one(
            {"UID": lock.get("UID")},
            {"_id": 0, "nome": 1, "id_colaborador": 1}
        )
        nome = usuario["nome"] if usuario else "Desconhecido"
        id_colaborador = usuario["id_colaborador"] if usuario else "sem ID"

        lockouts_formatados.append({
            "UID": lock.get("UID"),
            "nome": nome,
            "id_colaborador": id_colaborador,
            "tag": lock.get("tag"),
            "local": lock.get("local"),
            "status": lock.get("status"),
            "hora_retirada": lock.get("hora_retirada")
        })

    return jsonify(lockouts_formatados)

def lista_status():
    try:
        usuario_atual = status_abertura.find_one({"status": False})

        usuario_logado = usuarios.find_one({"UID": usuario_atual["UID"]}, {"_id": 0})
        return jsonify(usuario_logado), 200
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
    
