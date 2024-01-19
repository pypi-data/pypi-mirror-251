import pandas as pd
# import mysql.connector
from sqlalchemy import create_engine
import sqlalchemy


var_host='dbmbds.cfngygfor8bi.us-east-1.rds.amazonaws.com' 
var_port='3306'
var_database='db_understat'
var_user='admin'
var_password='mbdsf*2022'
# var_host='localhost' 
# var_port='8889'
# var_database='db_understat'
# var_user='root'
# var_password='root'

# Parámetros de conexión a tu base de datos
connection_params = {
    'user': var_user,
    'password': var_password,
    'host': var_host,
    'port': var_port,
    'database': var_database
}

# def query_to_dataframe(competition_id, season, query, connection_params):
def query_to_dataframe(query, connection_params):
    """
    Ejecuta una consulta SQL y devuelve los resultados en un DataFrame de pandas.
    Si hay un error, devuelve un mensaje indicando que los parámetros son incorrectos.

    :param competition_id: ID de la competición
    :param season: Temporada
    :param query: Consulta SQL con placeholders para competition_id y season
    :param connection_params: Parámetros de conexión a la base de datos
    :return: DataFrame de pandas con el resultado de la consulta o un mensaje de error
    """
    # Crear conexión a la base de datos
    # conn = mysql.connector.connect(**connection_params)

    connection_string = f"mysql+mysqlconnector://{connection_params['user']}:{connection_params['password']}@{connection_params['host']}:{connection_params['port']}/{connection_params['database']}"
    # Crear un motor de conexión con SQLAlchemy
    engine = create_engine(connection_string)

    try:
        # Formatear la consulta con los parámetros
        # formatted_query = query.format(competition_id=competition_id, season=season, table=table)

        # Ejecutar la consulta y cargar en DataFrame
        # df = pd.read_sql_query(formatted_query, conn)
        df = pd.read_sql_query(query, engine)
        return df

    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío

    finally:
        # Cerrar la conexión, independientemente de si hubo un error o no
        engine.dispose()


def getLigas(temporada, Competicion):

    consulta_sql = "SELECT * FROM ligas WHERE Competicion = '"+Competicion+"' AND temporada = '"+temporada+"'"
    result = query_to_dataframe(consulta_sql, connection_params)

    return result

def getJugadores_temporadas(temporada, Competicion):

    consulta_sql = "SELECT * FROM jugadores_temporadas WHERE competicion = '"+Competicion+"' AND temporada = '"+temporada+"'"
    result = query_to_dataframe(consulta_sql, connection_params)

    return result

def getCompetitions():
    
    consulta_sql = "SELECT * FROM competiciones "
    result = query_to_dataframe(consulta_sql, connection_params)

    return result

def getDisparos(temporada, Competicion):

    consulta_sql = "SELECT * FROM disparos WHERE Competicion = '"+Competicion+"' AND season = '"+temporada+"'"
    result = query_to_dataframe(consulta_sql, connection_params)

    return result

def getPartidos(temporada, Competicion):

    consulta_sql = "SELECT * FROM partidos WHERE Competicion = '"+Competicion+"' AND season = '"+temporada+"'"
    result = query_to_dataframe(consulta_sql, connection_params)

    return result

def getTables():
    """
    Devuelve una lista de todas las tablas en la base de datos.

    :param connection_params: Parámetros de conexión a la base de datos
    :return: Lista de nombres de tablas
    """
    connection_string = f"mysql+mysqlconnector://{connection_params['user']}:{connection_params['password']}@{connection_params['host']}:{connection_params['port']}/{connection_params['database']}"

    engine = create_engine(connection_string)

    try:
        # Utilizar sqlalchemy.inspect() para obtener un inspector
        inspector = sqlalchemy.inspect(engine)
        table_names = inspector.get_table_names()
        return table_names

    except Exception as e:
        print(f"Error al recuperar las tablas: {e}")
        return []

