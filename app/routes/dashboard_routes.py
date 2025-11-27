from flask import Blueprint, render_template
from app.models.dashboard_model import (
    total_insumos, insumos_stock_bajo, insumos_activos_descontinuados,
    alertas_pendientes, recepciones_mes, stock_por_categoria,
    entradas_salidas_ultimos_dias, peso_neto_por_variedad,
    top_agricultores_por_peso, jabas_entregadas_devueltas,
    agricultores_jabas_pendientes, ultimas_actividades,
    actividad_por_dia, insumos_proximo_vencer, ultimos_movimientos
)
from app.utils.auth import permiso_de_admin

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard_bp.route('/dashboard')
@permiso_de_admin("ver_dashboard")
def dashboard_home():
    # Métricas simples
    total = total_insumos()
    bajo = insumos_stock_bajo()
    ratios = insumos_activos_descontinuados()
    alertas = alertas_pendientes()
    recepciones = recepciones_mes()

    # Gráficos y series
    cat_labels, cat_data = stock_por_categoria()
    es_labels, es_entradas, es_salidas = entradas_salidas_ultimos_dias(30)
    var_labels, var_data = peso_neto_por_variedad(30, limit=10)
    top_agri = top_agricultores_por_peso(30, limit=5)
    jabas_labels, jabas_ent, jabas_dev = jabas_entregadas_devueltas(30)
    agri_pendientes = agricultores_jabas_pendientes()
    ult_act = ultimas_actividades(limit=10)
    act_labels, act_data = actividad_por_dia(30)
    proximos_vencer = insumos_proximo_vencer(30)
    ult_movs = ultimos_movimientos(limit=10)

    return render_template(
        "dashboard/dashboard.html",
        total_insumos=total,
        insumos_bajo=bajo,
        insumos_ratios=ratios,
        alertas_pendientes=alertas,
        recepciones_mes=recepciones,
        categorias_labels=cat_labels,
        categorias_data=cat_data,
        es_labels=es_labels,
        es_entradas=es_entradas,
        es_salidas=es_salidas,
        variedad_labels=var_labels,
        variedad_data=var_data,
        top_agricultores=top_agri,
        jabas_labels=jabas_labels,
        jabas_ent=jabas_ent,
        jabas_dev=jabas_dev,
        agri_pendientes=agri_pendientes,
        ultimas_actividades=ult_act,
        actividad_labels=act_labels,
        actividad_data=act_data,
        proximos_vencer=proximos_vencer,
        ultimos_movimientos=ult_movs
    )

