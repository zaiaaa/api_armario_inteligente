from flask import Blueprint, request, jsonify
from connections.db import db
from controllers.master import busca_master_uid

usuarios = db.usuarios

master_bp = Blueprint("master", __name__, url_prefix="/master")

@master_bp.route("/", methods=["POST"])
def master_handler():
    if request.method == "POST":
        return busca_master_uid()