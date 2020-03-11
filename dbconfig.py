from sqlalchemy import create_engine, MetaData, select, and_
from sqlalchemy.engine.url import URL

from config import mes_auditoria, year_auditoria

evas_postpago_db = {'drivername': 'mssql+pyodbc',
                    'username': 'readonly',
                    'password': 'readonly',
                    'host': '10.197.91.1',
                    'database': 'CLARO_IN_CALIDAD',
                    'query': {'driver': 'ODBC Driver 11 for SQL Server'}}

evas_hfc_db = {'drivername': 'mssql+pyodbc',
               'username': 'readonly',
               'password': 'readonly',
               'host': '10.197.91.1',
               'database': 'CLARO_IN_HFC',
               'query': {'driver': 'ODBC Driver 11 for SQL Server'}}

errores_db = {'drivername': 'mssql+pyodbc',
              'username': 'evizcarra',
              'password': '123',
              'host': '10.197.91.1',
              'database': 'DEV_Ricardo',
              'query': {'driver': 'ODBC Driver 11 for SQL Server'}}

db_postpago = URL(**evas_postpago_db)
db_hfc = URL(**evas_hfc_db)
db_errores = URL(**errores_db)

engine_postpago = create_engine(db_postpago, echo=False)
engine_hfc = create_engine(db_hfc, echo=False)
engine_errores = create_engine(db_errores)

metadata_postpago = MetaData()
metadata_postpago.reflect(bind=engine_postpago)
# metadata_interno.create_all()
metadata_hfc = MetaData()
metadata_hfc.reflect(bind=engine_hfc)

conn_postpago = engine_postpago.connect()
# result = engine_postpago.execute('SELECT * FROM Evas_postpago2')
conn_hfc = engine_hfc.connect()

postpago_table = metadata_postpago.tables['Evas_postpago2']
select_evas_postpago = select([postpago_table.c.txt_sn,
                               postpago_table.c.tipo_llamada,
                               postpago_table.c.motivo_llamada,
                               postpago_table.c.idform_cross,
                               postpago_table.c.evaluador,
                               postpago_table.c.CALIFICACION_FINAL,
                               postpago_table.c.detecta_mala_practica,
                               postpago_table.c.fecha_llamada,
                               postpago_table.c.Fecha_monitoreo,
                               postpago_table.c.TIPO_EVALUACION]).where(and_(postpago_table.c.idform_cross is not None,
                                                                             postpago_table.c.MES_FLL == mes_auditoria(),
                                                                             postpago_table.c.AÑO_FLL == year_auditoria(),
                                                                             postpago_table.c.TIPO_EVALUACION.in_(('CALIDAD_DYNAMICALL', 'MONITOREO_CRUZADO_MDY'))))  # , postpago_table.c.idform_cross.notin_(result)))

adm_table = metadata_hfc.tables['Evas_hfc_admin2']
select_evas_adm = select([adm_table.c.txt_sn,
                          adm_table.c.TipoLlamada,
                          adm_table.c.motivo_llamada,
                          adm_table.c.idform_cross,
                          adm_table.c.USUARIO,
                          adm_table.c.CALIFICACION_FINAL,
                          adm_table.c.MALA_PRACTICA,
                          adm_table.c.fecha_llamada,
                          adm_table.c.Fecha_monitoreo,
                          adm_table.c.TIPO_EVALUACION]).where(and_(adm_table.c.idform_cross is not None,
                                                                   adm_table.c.MES_FLL == mes_auditoria(),
                                                                   adm_table.c.AÑO_FLL == year_auditoria(),
                                                                   adm_table.c.TIPO_EVALUACION.in_(('MONITOREO_CALIDAD_DYNAMICALL', 'MONITOREO_CRUZADO'))))  # , postpago_table.c.idform_cross.notin_(result)))

tec_table = metadata_hfc.tables['Evas_hfc_tecnico2']
select_evas_tec = select([adm_table.c.txt_sn,
                          adm_table.c.TipoLlamada,
                          adm_table.c.motivo_llamada,
                          adm_table.c.idform_cross,
                          adm_table.c.USUARIO,
                          adm_table.c.CALIFICACION_FINAL,
                          adm_table.c.MALA_PRACTICA,
                          adm_table.c.fecha_llamada,
                          adm_table.c.Fecha_monitoreo,
                          adm_table.c.TIPO_EVALUACION]).where(and_(adm_table.c.idform_cross is not None,
                                                                   adm_table.c.MES_FLL == mes_auditoria(),
                                                                   adm_table.c.AÑO_FLL == year_auditoria(),
                                                                   adm_table.c.TIPO_EVALUACION.in_(('MONITOREO_CALIDAD_DYNAMICALL', 'MONITOREO_CRUZADO'))))  # , postpago_table.c.idform_cross.notin_(result)))
