import pandas as pd
from sqlalchemy import Integer, Text, DateTime

from dbconfig import conn, select_evas_postpago, engine_errores
from validaciones import verifica_eva

if __name__ == '__main__':
    res = conn.execute(select_evas_postpago)
    errores = []

    for _r in res:
        errores.extend(verifica_eva(_r))

    # if errores:
    #     # print('Se encontraron los siguientes errores:')
    #     for _i, _e in enumerate(errores):
    #         # if _e.msg == 'Tipo de monitoreo no coincide con evaluador':
    #         print(f'{_i}) ID:{_e["id_eva"]} - E:{_e["evaluador"]} - SN:{_e["sn"]} - MSG:{_e["msg"]} - O:{_e["original"]}')

    df_local = pd.DataFrame(data=errores)
    df_server = pd.read_sql_table(table_name='APP_ERRORES', con=engine_errores)
    df_total = pd.concat([df_server, df_local])

    df_total.drop_duplicates(subset=['id_eva', 'sn', 'evaluador', 'original', 'msg'], keep='first', inplace=True)

    df_total.to_sql(name='APP_ERRORES',
                    con=engine_errores,
                    if_exists='replace',
                    index=False,
                    dtype={'id_eva': Integer,
                           'evaluador': Text,
                           'sn': Text,
                           'original': Text,
                           'msg': Text,
                           'timestamp': DateTime})
