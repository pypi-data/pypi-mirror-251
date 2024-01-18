
# API Data fbref.com

A Python package to api data fbref.com

## Usage

```python

## Comprobar si fbref-package esta instalado y su version
# !pip list

## Instalar
# !pip install fbref_package

## Actualizar a la ultima version
# !pip install fbref-package --upgrade

## Pre install
# !pip install sqlalchemy
# !pip install pandas mysql-connector-python

## Import package
import fbref_package as fbref

## Ejemplo de uso 1
# Obtenemos todos los nombres de los dataframe posibles
table_names = getTables()
table_names

## Ejemplo de uso 2
# Obtenemos todas las competiciones posibles
df_competition = getCompetitions()
df_competition

## Ejemplo de uso 3
# Obtenemos los partidos de una competicion en una temporada
df_result = getData('12', '2023-2024', 'matches')
df_result

## Ejemplo de uso 4
# Obtenemos el resumen por competicion y temporada
df_result = getData('12', '2023-2024', 'competition_summary')
df_result

## Ejemplo de uso 5
# Obtenemos el resumen de la competicion por equipo y temporada
df_result = getData('12', '2023-2024', 'competition_team_summary')
df_result

## Ejemplo de uso 6
# Obtenemos el resumen de la competicion por jugador y temporada
df_result = getData('12', '2023-2024', 'competition_player_summary')
df_result

## Ejemplo de uso 7
# Obtenemos el resumen de los jugadores por partido en la competicion y temporada
df_result = getData('12', '2023-2024', 'match_player_summary')
df_result

## Ejemplo de uso 8
# Obtenemos el resumen de los equipos por partido en la competicion y temporada
df_result = getData('12', '2023-2024', 'match_team_summary')
df_result


```

