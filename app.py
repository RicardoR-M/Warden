import pandas as pd
from sqlalchemy import Integer, Text, DateTime

from dbconfig import conn_postpago, select_evas_postpago, engine_errores, conn_hfc, select_evas_adm, select_evas_tec
from validaciones import verifica_eva

if __name__ == '__main__':
    errores = []

    res_postpago = conn_postpago.execute(select_evas_postpago)
    for _r in res_postpago:
        errores.extend(verifica_eva(_r, 'POST'))

    res_adm = conn_hfc.execute(select_evas_adm)
    for _r in res_adm:
        errores.extend(verifica_eva(_r, 'ADM'))

    res_tec = conn_hfc.execute(select_evas_tec)
    for _r in res_tec:
        errores.extend(verifica_eva(_r, 'TEC'))

    # if errores:
    #     # print('Se encontraron los siguientes errores:')
    #     for _i, _e in enumerate(errores):
    #         # if _e.msg == 'Tipo de monitoreo no coincide con evaluador':
    #         print(f'{_i}) ID:{_e["id_eva"]} - E:{_e["evaluador"]} - SN:{_e["sn"]} - MSG:{_e["msg"]} - O:{_e["original"]}')

    df_local = pd.DataFrame(data=errores)
    df_server = pd.read_sql_table(table_name='APP_ERRORES', con=engine_errores)
    # df_total = pd.concat([df_server, df_local])
    df_total = df_local  # Temporal por desarrolo, crea la tabla nuevamente en cada corrida.

    df_total.drop_duplicates(subset=['id_eva', 'sn', 'evaluador', 'original', 'msg'], keep='first', inplace=True)

    print(df_local)
    print(df_server)

    df_total.to_sql(name='APP_ERRORES',
                    con=engine_errores,
                    if_exists='replace',
                    index=False,
                    dtype={'id_eva': Integer,
                           'evaluador': Text,
                           'sn': Text,
                           'original': Text,
                           'msg': Text,
                           'skill': Text,
                           'timestamp': DateTime})
