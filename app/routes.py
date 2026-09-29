from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from app.models import (
    atualizar_atividade,
    buscar_atividade,
    concluir_atividade,
    contar_atividades,
    criar_atividade,
    excluir_atividade,
    listar_atividades,
)

main = Blueprint("main", __name__)

PRIORIDADES = ["Baixa", "Média", "Alta"]
STATUS = ["Pendente", "Concluída"]

@main.route("/")
def inicio():
    status = request.args.get("status", "")
    prioridade = request.args.get("prioridade", "")

    atividades = listar_atividades(
        current_app.config["DATABASE_PATH"],
        status=status or None,
        prioridade=prioridade or None,
    )
    contadores = contar_atividades(current_app.config["DATABASE_PATH"])

    return render_template(
        "index.html",
        atividades=atividades,
        contadores=contadores,
        filtro_status=status,
        filtro_prioridade=prioridade,
        prioridades=PRIORIDADES,
        status_opcoes=STATUS,
    )

@main.route("/atividade/nova", methods=["GET", "POST"])
def nova_atividade():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        data_entrega = request.form.get("data_entrega", "").strip()
        prioridade = request.form.get("prioridade", "Média")

        if not titulo:
            flash("Informe um título para a atividade.", "erro")
            return render_template(
                "formulario.html",
                atividade=None,
                prioridades=PRIORIDADES,
                status_opcoes=STATUS,
            )

        if prioridade not in PRIORIDADES:
            prioridade = "Média"

        criar_atividade(
            current_app.config["DATABASE_PATH"],
            titulo,
            descricao,
            data_entrega,
            prioridade,
        )
        flash("Atividade cadastrada com sucesso!", "sucesso")
        return redirect(url_for("main.inicio"))

    return render_template(
        "formulario.html",
        atividade=None,
        prioridades=PRIORIDADES,
        status_opcoes=STATUS,
    )

@main.route("/atividade/<int:atividade_id>/editar", methods=["GET", "POST"])
def editar_atividade(atividade_id):
    atividade = buscar_atividade(current_app.config["DATABASE_PATH"], atividade_id)

    if atividade is None:
        flash("Atividade não encontrada.", "erro")
        return redirect(url_for("main.inicio"))

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        data_entrega = request.form.get("data_entrega", "").strip()
        prioridade = request.form.get("prioridade", "Média")
        status = request.form.get("status", "Pendente")

        if not titulo:
            flash("Informe um título para a atividade.", "erro")
            return render_template(
                "formulario.html",
                atividade=atividade,
                prioridades=PRIORIDADES,
                status_opcoes=STATUS,
            )

        atualizar_atividade(
            current_app.config["DATABASE_PATH"],
            atividade_id,
            titulo,
            descricao,
            data_entrega,
            prioridade if prioridade in PRIORIDADES else "Média",
            status if status in STATUS else "Pendente",
        )
        flash("Atividade atualizada com sucesso!", "sucesso")
        return redirect(url_for("main.inicio"))

    return render_template(
        "formulario.html",
        atividade=atividade,
        prioridades=PRIORIDADES,
        status_opcoes=STATUS,
    )

@main.post("/atividade/<int:atividade_id>/concluir")
def marcar_concluida(atividade_id):
    if buscar_atividade(current_app.config["DATABASE_PATH"], atividade_id):
        concluir_atividade(current_app.config["DATABASE_PATH"], atividade_id)
        flash("Atividade marcada como concluída.", "sucesso")
    else:
        flash("Atividade não encontrada.", "erro")
    return redirect(url_for("main.inicio"))

@main.post("/atividade/<int:atividade_id>/excluir")
def remover_atividade(atividade_id):
    if buscar_atividade(current_app.config["DATABASE_PATH"], atividade_id):
        excluir_atividade(current_app.config["DATABASE_PATH"], atividade_id)
        flash("Atividade excluída.", "sucesso")
    else:
        flash("Atividade não encontrada.", "erro")
    return redirect(url_for("main.inicio"))
