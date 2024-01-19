
<img src="https://github.com/lucbra21/images/blob/main/sdc_logo.jpeg" alt="Sports Data Campus" />

# API Data understat.com by Sports Data Campus

A Python package to api data understat.com

https://pypi.org/project/understat-package/

# Aviso Importante sobre el Uso de Datos de understat.com

Esta librería está diseñada para facilitar el acceso a los datos disponibles en [understat.com](https://understat.com/) con propósitos educativos y de investigación. Al utilizar esta librería, los usuarios deben adherirse a los siguientes términos y condiciones:

## Atribución de Datos
Todos los datos obtenidos a través de esta librería provienen de understat.com. Los usuarios deben asegurarse de atribuir claramente a understat.com como la fuente de los datos en cualquier publicación, análisis o proyecto donde se utilicen estos datos.

## Uso No Comercial
Esta librería se proporciona exclusivamente para uso no comercial. Cualquier uso de los datos obtenidos para propósitos comerciales está estrictamente prohibido.

## Adherencia a los Términos de Uso de understat.com
Se insta a los usuarios a revisar y seguir los términos de uso establecidos. El uso indebido de los datos puede resultar en la violación de estos términos.

## Limitación de Responsabilidad
El creador de esta librería no se hace responsable del mal uso de la misma ni de cualquier violación de los términos de uso de understat.com por parte de los usuarios. Los usuarios son responsables de asegurar que su uso de los datos cumple con todas las leyes y regulaciones aplicables.

Al utilizar esta librería, usted reconoce y acepta estos términos.


## Usage

```python

## Comprobar si understat-package esta instalado y su version
# !pip list

## Instalar
# !pip install understat_package

## Actualizar a la ultima version
# !pip install understat-package --upgrade

## Pre install
# !pip install sqlalchemy
# !pip install pandas mysql-connector-python

## Import package
import understat_package as understat

## Ejemplo de uso 1
# Obtenemos todos las competiciones
table_names = understat.getCompetitions()
table_names

## Ejemplo de uso 2
# Obtenemos la lista de equipos y tabla de posicion de cada liga
# df_result = understat.getLigas(season, copetition_id)
df_competition = understat.getLigas('2024', 'Serie A')
df_competition

## Ejemplo de uso 3
# Obtenemos los jugadores por temporada y competicion 
# df_result = understat.getJugadores_temporadas(season, copetition_id)
df_result = getJugadores_temporadas('2024','Serie A')
df_result

## Ejemplo de uso 4
# Obtenemos los disparos por temporada y competicion
# df_result = understat.getDisparos(season, copetition_id)
df_result = understat.getDisparos('2024','Serie A')
df_result

## Ejemplo de uso 5
# Obtenemos la lista de partidos de cada competicion y temporada
# df_result = understat.getPartidos(season, copetition_id)
df_result = understat.getPartidos('2024','Serie A')
df_result


```

by Sports Data Campus