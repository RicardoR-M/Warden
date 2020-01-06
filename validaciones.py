from re import search


class ErrorValidacion:
    def __init__(self, id_eva, sn, evaluador, original, msg):
        self.id_eva = id_eva
        self.sn = sn
        self.evaluador = evaluador
        self.msg = msg
        self.original = original


def verifica_eva(eva):
    errores = []
    if sn_eva(eva.txt_sn) is not None:
        errores.append(sn_eva(eva.txt_sn))
    if tipo_llamada(eva.tipo_llamada) is not None:
        errores.append(tipo_llamada(eva.tipo_llamada))
    if motivo_llamada(eva.motivo_llamada) is not None:
        errores.append(motivo_llamada(eva.motivo_llamada))

    if len(errores) == 0:
        print('No se encontraron errores')
    else:
        print('Se encontraron los siguientes errores:')
        for i, _e in enumerate(errores):
            print(f'{i}: ID:{_e.id_eva} - E:{_e.evaluador} - SN:{_e.sn} - MSG:{_e.msg} - O:{_e.original}')


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
