from sqlalchemy import create_engine, MetaData, select, and_
from sqlalchemy.engine.url import URL

from config import mes_auditoria, year_auditoria

evas_db = {'drivername': 'mssql+pyodbc',
           'username': 'readonly',
           'password': 'readonly',
           'host': '10.197.91.1',
           'database': 'CLARO_IN_CALIDAD',
           'query': {'driver': 'ODBC Driver 13 for SQL Server'}}

errores_db = {'drivername': 'mssql+pyodbc',
              'username': 'sa',
              'password': '***REMOVED***',
              'host': '10.197.91.1',
              'database': 'CLARO_IN_CALIDAD',
              'query': {'driver': 'ODBC Driver 13 for SQL Server'}}

db_postpago = URL(**evas_db)
db_errores = URL(**errores_db)

engine_postpago = create_engine(db_postpago, echo=False)
engine_errores = create_engine(db_errores)

metadata = MetaData()
metadata.reflect(bind=engine_postpago)
# metadata_interno.create_all()

conn = engine_postpago.connect()
# result = engine_postpago.execute('SELECT * FROM Evas_postpago2')

postpago_table = metadata.tables['Evas_postpago2']
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
