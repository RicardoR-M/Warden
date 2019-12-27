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
    if sn_eva(eva.txt_sn):
        errores.append(ErrorValidacion(eva.idform_cross, eva.txt_sn, eva.evaluador, eva.txt_sn, 'SN Incorrecta'))
    if tipo_llamada(eva.tipo_llamada):
        errores.append(ErrorValidacion(eva.idform_cross, eva.txt_sn, eva.evaluador, eva.tipo_llamada, 'Tipo de llamada incorrecto'))
    if motivo_llamada(eva.motivo_llamada):
        errores.append(ErrorValidacion(eva.idform_cross, eva.txt_sn, eva.evaluador, eva.motivo_llamada, 'Motivo de llamada incorrecto'))

    if len(errores) == 0:
        print('No se encontraron errores')
    else:
        print('Se encontraron los siguientes errores:')
        for i, _e in enumerate(errores):
            print(f'{i}: ID:{_e.id_eva} - E:{_e.evaluador} - SN:{_e.sn} - MSG:{_e.msg} - O:{_e.original}')


def sn_eva(sn):
    if sn is None:
        return True
    return bool(search(r'[^0-9]+', sn))


def tipo_llamada(tipo):
    if tipo is None:
        return True
    elif tipo != 'INFORMATIVO' and tipo != 'RECLAMO' and tipo != 'VARIACION':
        return True
    return False


def motivo_llamada(motivo):
    if motivo is None:
        return True
    elif motivo == 'SELECCIONAR':
        return True
    return False
