from flask import Blueprint,current_app,flash,redirect,render_template,request,url_for
from app.models import *
main=Blueprint("main",__name__)
PRIORIDADES=["Baixa","Média","Alta"]; STATUS=["Pendente","Concluída"]

@main.route("/")
def inicio():
    s=request.args.get("status",""); p=request.args.get("prioridade","")
    path=current_app.config["DATABASE_PATH"]
    return render_template("index.html",atividades=listar_atividades(path,s or None,p or None),contadores=contar_atividades(path),filtro_status=s,filtro_prioridade=p,prioridades=PRIORIDADES,status_opcoes=STATUS)

@main.route("/atividade/nova",methods=["GET","POST"])
def nova_atividade():
    if request.method=="POST":
        t=request.form.get("titulo","").strip()
        if not t: flash("Informe um título.","erro")
        else:
            criar_atividade(current_app.config["DATABASE_PATH"],t,request.form.get("descricao","").strip(),request.form.get("data_entrega",""),request.form.get("prioridade","Média"))
            flash("Atividade cadastrada!","sucesso"); return redirect(url_for("main.inicio"))
    return render_template("formulario.html",atividade=None,prioridades=PRIORIDADES,status_opcoes=STATUS)

@main.route("/atividade/<int:i>/editar",methods=["GET","POST"])
def editar_atividade(i):
    path=current_app.config["DATABASE_PATH"]; a=buscar_atividade(path,i)
    if not a: flash("Atividade não encontrada.","erro"); return redirect(url_for("main.inicio"))
    if request.method=="POST":
        atualizar_atividade(path,i,request.form.get("titulo","").strip(),request.form.get("descricao","").strip(),request.form.get("data_entrega",""),request.form.get("prioridade","Média"),request.form.get("status","Pendente"))
        flash("Atividade atualizada!","sucesso"); return redirect(url_for("main.inicio"))
    return render_template("formulario.html",atividade=a,prioridades=PRIORIDADES,status_opcoes=STATUS)

@main.post("/atividade/<int:i>/concluir")
def marcar_concluida(i):
    concluir_atividade(current_app.config["DATABASE_PATH"],i); flash("Atividade concluída!","sucesso"); return redirect(url_for("main.inicio"))

@main.post("/atividade/<int:i>/excluir")
def remover_atividade(i):
    excluir_atividade(current_app.config["DATABASE_PATH"],i); flash("Atividade excluída.","sucesso"); return redirect(url_for("main.inicio"))
