from connections.db import db
from flask import jsonify, request
from datetime import datetime
from zoneinfo import ZoneInfo

abertura = db.abertura
status_abertura = db.status_abertura
usuarios = db.usuarios
lockout = db.lockout

def validar_cracha():
    dados = request.get_json()   
    
    if "UID" not in dados:
        return jsonify({"erro": "Obrigatório UID do crachá do colaborador."})
    # hora_atual = datetime.now()

    usuario = usuarios.find_one({"UID": dados["UID"]})
    print(usuario)
    if not usuario:
        return jsonify({"mensagem": "Acesso negado."}), 403

    #trocar essa query para o cadastro na intenção de abertura.
    queryFinal = {
        "UID": dados["UID"],
        "acao": dados["acao"],
        "status": False
    }
    #acao deve ser retirada ou devolucao

    try:
        status_abertura.insert_one(queryFinal)
        return jsonify({"mensagem": "Aguardando preenchimento do Formulário."}), 201
    except Exception as e:
        return jsonify({"mensagem": f"Erro -> {str(e)}"}), 400

def excluir_status_abertura():
    try:
        resultado = status_abertura.delete_many({})  # Apaga todos os documentos
        return jsonify({"mensagem": f"{resultado.deleted_count} status apagados com sucesso."}), 200
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao apagar status -> {str(e)}"}), 400


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

        if not dados.get("chave") :
            db.lockout.update_one(
            {"tag": dados["tag"]},
            {"$set":  {
                "status": "devolvido",
                "local": "",
                "UID": "",
                "hora_retirada": None
            }})
            return {"status": "Formulario de devolução preenchido e trava Aberta!"}
        else:
            return {"status": "Formulario de devolução preenchido e trava Aberta!"}
            #db.status_abertura.delete_one({"UID": dados["UID"]})
            #A ação da auto-exclusão foi para a parte de firmware.
        

    except Exception as e:
        return jsonify({"mensagem": f"Erro -> {str(e)}"}), 400

def listar_lockouts():
    lockouts = list(db.lockout.find({}))
    usuarios_cursor = usuarios.find({}, {"_id": 0, "UID": 1, "nome": 1, "id_colaborador": 1})
    
    # cria um dicionário para lookup rápido por UID
    usuarios_dict = {u["UID"]: u for u in usuarios_cursor}

    lockouts_formatados = []

    for lock in lockouts:
        user = usuarios_dict.get(lock.get("UID"))
        nome = user.get("nome", "Desconhecido") if user else "Desconhecido"
        id_colaborador = user["id_colaborador"] if user else "sem ID"

        hora_utc = lock.get("hora_retirada")
        if hora_utc:
            if isinstance(hora_utc, str):
                hora_utc = datetime.fromisoformat(hora_utc.replace("Z", "+00:00"))
            hora_brasil = hora_utc.astimezone(ZoneInfo("America/Sao_Paulo"))
            hora_retirada = hora_brasil.strftime("%Y-%m-%d %H:%M:%S")
        else:
            hora_retirada = None

        lockouts_formatados.append({
            "UID": lock.get("UID"),
            "nome": nome,
            "id_colaborador": id_colaborador,
            "tag": lock.get("tag"),
            "local": lock.get("local"),
            "status": lock.get("status"),
            "hora_retirada": hora_retirada
        })

    return jsonify(lockouts_formatados)


def listar_lockout(tag):
    if not tag:
        return jsonify({"erro": "Parâmetro 'tag' é obrigatório"}), 400

    lock = db.lockout.find_one({"tag": tag})

    if not lock:
        return jsonify({"erro": "Lockout não encontrado"}), 404

    usuario = usuarios.find_one(
        {"UID": lock.get("UID")},
        {"_id": 0, "nome": 1, "id_colaborador": 1}
    )

    nome = usuario["nome"] if usuario else "Desconhecido"
    id_colaborador = usuario["id_colaborador"] if usuario else "sem ID"

    lock_formatado = {
        "UID": lock.get("UID"),
        "nome": nome,
        "id_colaborador": id_colaborador,
        "tag": lock.get("tag"),
        "local": lock.get("local"),
        "status": lock.get("status"),
        "hora_retirada": lock.get("hora_retirada")
    }

    return jsonify(lock_formatado)



def cadastrar_lockout():
    data = request.get_json()
    tag = data.get("tag")
    if not tag :
        return jsonify({"erro": "tag é obrigatória"}), 400
    # Monta o documento
    novo_lockout = {
        "tag": tag,
        "local": "",
        "status": "devolvido",  # ou qualquer valor padrão
    }
    db.lockout.insert_one(novo_lockout)
    return jsonify({"mensagem": "Lockout cadastrado com sucesso"}), 201





def lista_status():
    try:
        usuario_atual = status_abertura.find_one()

        if not usuario_atual:
            return jsonify({"mensagem": "Nenhum status encontrado."}), 404

        usuario_logado = usuarios.find_one({"UID": usuario_atual["UID"]}, {"_id": 0})

        usuario_logado["status"] = usuario_atual["status"]
        usuario_logado["acao"] = usuario_atual["acao"]

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
    
