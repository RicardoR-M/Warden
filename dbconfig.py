from datetime import date
from pprint import pprint

from sqlalchemy import create_engine, MetaData, select, and_, Table, Column, Integer
from sqlalchemy.engine.url import URL

from validaciones import verifica_eva

evas_db = {'drivername': 'mssql+pyodbc',
           'username': 'readonly',
           'password': 'readonly',
           'host': '10.197.91.1',
           'database': 'CLARO_IN_CALIDAD',
           'query': {'driver': 'ODBC Driver 11 for SQL Server'}}
internal_db = {'drivername': 'sqlite',
               'database': 'interno.db'}

db_uri = URL(**evas_db)
interno_uri = URL(**internal_db)

engine = create_engine(db_uri)
engine_interno = create_engine(interno_uri)

metadata = MetaData()
metadata.reflect(bind=engine)
metadata_interno = MetaData(engine_interno)
tabla_interno = Table('Procesado', metadata_interno, Column('id', Integer))
metadata_interno.create_all()

conn = engine.connect()
conn_interno = engine_interno.connect()
conn_interno.execute('DELETE FROM Procesado')
# result = engine.execute('SELECT * FROM Evas_postpago2')

result = [r for r, in conn_interno.execute(select([tabla_interno.c.id]))]

evas_table = metadata.tables['Evas_postpago2']
select_evas = select([evas_table]).where(and_(evas_table.c.idform_cross != None,
                                              evas_table.c.DIA_FLL == 26,
                                              evas_table.c.TIPO_EVALUACION == 'CALIDAD_DYNAMICALL'))  # , evas_table.c.idform_cross.notin_(result)))

res = conn.execute(select_evas)
for _r in res:
    verifica_eva(_r)

# for _r in res:
#
#     conn_interno.execute(tabla_interno.insert().values(id=_r.idform_cross))

for _r in res:
    print(_r)
