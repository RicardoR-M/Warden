from datetime import datetime
from re import search

from config import evaluador_cruzado


# class ErrorValidacion:
#     def __init__(self, id_eva, sn, evaluador, original, msg):
#         self.id_eva = id_eva
#         self.sn = sn
#         self.evaluador = evaluador
#         self.msg = msg
#         self.original = original


def verifica_eva(eva, skill):
    errores = []
    if sn_eva(eva.txt_sn):
        errores.append({'id_eva': eva.idform_cross, 'sn': eva.txt_sn, 'evaluador': eva.evaluador, 'original': eva.txt_sn, 'msg': sn_eva(eva.txt_sn), 'skill': skill, 'timestamp': datetime.today()})
    if tipo_llamada(eva.tipo_llamada):
        errores.append({'id_eva': eva.idform_cross, 'sn': eva.txt_sn, 'evaluador': eva.evaluador, 'original': eva.tipo_llamada, 'msg': tipo_llamada(eva.tipo_llamada), 'skill': skill, 'timestamp': datetime.today()})
    if motivo_llamada(eva.motivo_llamada):
        errores.append({'id_eva': eva.idform_cross, 'sn': eva.txt_sn, 'evaluador': eva.evaluador, 'original': eva.motivo_llamada, 'msg': motivo_llamada(eva.motivo_llamada), 'skill': skill, 'timestamp': datetime.today()})
    if mala_praxis(eva.CALIFICACION_FINAL, eva.detecta_mala_practica, skill):
        errores.append({'id_eva': eva.idform_cross, 'sn': eva.txt_sn, 'evaluador': eva.evaluador, 'original': 'Mala praxis', 'msg': mala_praxis(eva.CALIFICACION_FINAL, eva.detecta_mala_practica, skill), 'skill': skill, 'timestamp': datetime.today()})
    if eva_dentroplazo(eva.Fecha_monitoreo, eva.txt_sn, eva.evaluador):
        errores.append({'id_eva': eva.idform_cross, 'sn': eva.txt_sn, 'evaluador': eva.evaluador, 'original': 'Eva fuera de fecha', 'msg': eva_dentroplazo(eva.Fecha_monitoreo, eva.txt_sn, eva.evaluador), 'skill': skill, 'timestamp': datetime.today()})
    if tipo_monitoreo(eva.TIPO_EVALUACION, eva.evaluador):
        errores.append({'id_eva': eva.idform_cross, 'sn': eva.txt_sn, 'evaluador': eva.evaluador, 'original': eva.TIPO_EVALUACION, 'msg': tipo_monitoreo(eva.TIPO_EVALUACION, eva.evaluador), 'skill': skill, 'timestamp': datetime.today()})

    return errores


def sn_eva(sn):
    msg_error = 'SN Incorrecta'
    if sn is None:
        return msg_error
    if bool(search(r'[^0-9]+', sn)):
        return msg_error
    return None


def tipo_llamada(tipo):
    msg_error = 'Tipo de llamada incorrecto'
    if tipo is None:
        return msg_error
    elif tipo != 'INFORMATIVO' and tipo != 'RECLAMO' and tipo != 'VARIACION':
        return msg_error
    return None


def motivo_llamada(motivo):
    msg_error = 'Motivo de llamada incorrecto'
    if motivo is None:
        return msg_error
    elif motivo == 'SELECCIONAR':
        return msg_error
    return None


def mala_praxis(calificacion, mpraxis, skill):
    msg_error = 'No se selecciono motivo de mala praxis'
    if skill == 'POST':
        if calificacion == 0 and (mpraxis == 'NO' or mpraxis == 'SELECCIONAR'):
            return msg_error
    else:
        if calificacion == 0 and mpraxis == 0:
            return msg_error
    return None


def eva_dentroplazo(fmon, sn, evaluador):
    msg_error = 'Evaluación mayor a '
    feva = datetime.strptime(sn.strip()[0:6], '%y%m%d')
    if (fmon.date() - feva.date()).days > 2 and evaluador not in evaluador_cruzado():
        return msg_error + f'{(fmon.date() - feva.date()).days * 24}H'
    return None


def tipo_monitoreo(tipo, evaluador):
    msg_error = 'Tipo de monitoreo no coincide con evaluador'
    if ('CALIDAD' in tipo.upper() and evaluador in evaluador_cruzado()) or ('CRUZADO' in tipo.upper() and evaluador not in evaluador_cruzado()):
        return msg_error
    return None
