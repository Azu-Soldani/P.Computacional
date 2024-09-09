# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 18:40:06 2024

@author: Magaa
"""

import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st

"""
Leo un archivo
"""

def cargar_datos(archivo, separador):
    datos = pd.read_csv(archivo, sep = separador)
    return datos
"""
Saco la pelicula con menor y mayor rating
"""
def menor_rating(datos):
    menor = datos[datos["IMDB Rating"] == datos["IMDB Rating"].min()].Title
    return menor

def mayor_rating(datos):
    mayor = datos[datos["IMDB Rating"] == datos["IMDB Rating"].max()].Title
    return mayor
"""
la película con mayor rating (‘IMDB Rating’) de 2023
"""
def mayor_rating_2023(datos):
    filtro_por_año = datos[datos["IMDB Rating"] == 2023.0]
    # Le aplico la funcion mayor_rating a flitro_por_año para que me devuelva la pelicula con 
    #mayor rating que salio en el 2023
    m_rating = mayor_rating(filtro_por_año)
    #filtrar la columns "Release Year" por año 2023
    #devuelve las peliculas con mayor rating en el 2023
    return m_rating
"""
la película del género (Genre) Acción (‘Action’) más corta (Length in Min) y cuanto es su duración
"""
def pelicula_mas_corta(datos):
    #Filtro de todas las peliculas de accion
    genero_accion = datos[datos["Genre"] == "Action"]
    #mas corta en min
    mas_corta = genero_accion[genero_accion["Length in Min"] == genero_accion["Length in Min"].min()].loc[:,["Title","Length in Min"]]
    #modificar formato tiempo
    return mas_corta
"""    
Las películas que duran 3 o más horas)
"""
def peliculas_duran_3_o_mas_horas(datos):
    #60min x 3 = 180min es ig a 3 horas
    filtro_por_duracion = datos[datos["Length in Min"] >= 180.0].Title
    return filtro_por_duracion
"""
El año donde el género Drama (‘Drama’) obtuvo el mejor rating
"""
def año_mayor_rating_drama(datos):
    genero_drama = datos[datos["Genre"] == "Drama"]
    año = genero_drama[genero_drama["IMDB Rating"] == genero_drama["IMDB Rating"].max()]["Release Year"]
    return año
"""
¿Cuál género tuvo más películas en el año 2012?
"""
def genero_con_mayor_peliculas_2012 (datos):
    filtro_por_año = datos[datos["Release Year"] == 2012.0]
    genero = filtro_por_año.Genre.value_counts().idxmax()
    return genero
"""
Obtener un dataframe donde, por cada año, se tenga tanto el promedio como el desvío estándar de la duración de las películas de ese año.
"""

def promedio_y_desvío_por_año(datos):
#devuelve un dataframe donde por cada año se obtiene el promedio y el desvío estándar de la duración de las pelis de ese año
    promedio = datos.groupby(["Release Year"])["Length in Min"].mean()
    #agrupamos los datos por año y los minutos y le sacamos el promedio
    desvío = datos.groupby(["Release Year"])["Length in Min"].std()
    #sacamos el desvío estándar
    nuevo_dataframe = pd.DataFrame({
        "Promedio": promedio, 
        "Desvío": desvío})
    #creamos un nuevo dataframe con estas columnas
    return nuevo_dataframe

"""
Agregarle al dataframe anterior una columna con el nombre de la película más larga del año, y otras dos columnas para su duración, director y puntaje.
"""

def agregar_a_dataframe(datos):
#agregamos columnas al dataframe
    df = promedio_y_desvío_por_año(datos)
    #traigo el dataframe
    
    idx_mas_larga = datos.groupby(["Release Year"])["Length in Min"].idxmax()
    peli_mas_larga= datos.loc[idx_mas_larga, ["Title", "Release Year", "Length in Min", "Director"]]
    #saco los datos de la peli mas larga
   
    df["Película más larga"] = peli_mas_larga["Title"].values
    df["Duración película más larga"] = peli_mas_larga["Length in Min"].values
    df["Director película más larga"] = peli_mas_larga["Director"].values
    #agrego columnas llamando al título, duración y director
    
    return df

"""
¿Cuántas películas dirigió “Jesús Franco”? ¿En qué año dirigió más películas? 
"""

def año_con_mas_pelis_dirigidas(datos,director):
    filtro = datos[datos["Director"] == director]
    filtro_x_año = filtro["Release Year"].value_counts()
    filtro_año_max = filtro_x_año.max()
    rest = filtro_x_año[filtro_x_año == filtro_año_max].index.to_list()
    return rest

"""
Y “Lesley Selander” ¿cuántas películas dirigió?
"""
def cuantas_pelis_dirigio(datos,director):
    rest = datos[datos["Director"] == director].Title.count()
    return rest

"""
Generar un DataFrame que incluya las películas dirigidas por Jesús Franco y 
por Lesley Selander junto con sus ratings.
"""
def dataframe(datos,directores):
    filtro = datos[datos["Director"].isin(directores)]
    return filtro.loc[:,["Title","Director","IMDB Rating"]].copy(deep=True)

"""
Averiguar si existe una correlación entre el año de estreno y 
rating de las películas mediante un gráfico y obtener el coeficiente de Pearson.
"""

def correlacion(datos):
    datos.plot.scatter(x="Release Year", y="IMDB Rating", logy=True)
    pend, orig, r, p, err = st.linregress(datos["Release Year"], datos["IMDB Rating"])
    datos_regr = f'Reg. Lineal: y={orig:.2f}+{pend:.2f}x, r={r:.2f}'
    plt.plot(datos["Release Year"], orig + pend * datos["Release Year"], color="orange")
    #Calculo el coeficiente de Pearson.
    corrs = datos.corr(numeric_only = True)
    pearson = corrs.loc["Release Year","IMDB Rating"]
    
    #guardo el grafico como una imagen
    plt.savefig("correlacion.histograma.png")
    plt.close()
    
    print(pearson)
    

"""
Comparar las medias de la duración de películas entre el año 2003 y 2004
"""
#Como 2003.0 es mayor, entonces la media es mayor que la del 2004
def comparacion_duracion_2003_2004(datos):
    media_por_año=datos[["Release Year","Length in Min"]].groupby("Release Year").mean()
    #tomamos los datos de las columnas de año de estreno y duración, agrupamos por año y le sacamos la media a la duración
    datos[datos["Release Year"].isin([2003.0,2004.0])].boxplot("Length in Min",by="Release Year")
    plt.plot([1,2],media_por_año.loc[[2003.0,2004.0]],"o")
    #creamos el gráfico boxplot
    #Achico el rango del grafio
    plt.ylim(50,150)
    plt.title("Comparación de duracion por año")
    plt.xlabel("Año lanzamiento")
    plt.ylabel("Duración en Min")
    promedios = datos.groupby('Release Year')['Length in Min'].mean()
    promedios_filtrados = promedios.loc[[2003.0, 2004.0]]
    
    #guardo el grafico como una imagen
    plt.savefig("comparacion.por.año.histograma.png")
    plt.close()
    
    print(promedios_filtrados)

#Como 2004.0 esta mas cerca del 0, entonces el la es mayor  
def comparacion_duracion_2003_2004_normalizacion(datos):
    #filtramos los datos para quedarnos solo con los de 2003 y 2004
    df_duracion = datos[(datos["Release Year"] == 2003.0)|(datos["Release Year"] ==2004.0)]
    # Calcula la media y la desviación estándar de la columna IMDB Rating
    mean_rating = df_duracion["Length in Min"].mean()
    std_rating = df_duracion["Length in Min"].std()
    # Aplicar la normalización (z-score)
    df_duracion = df_duracion.copy()
    df_duracion["Length in Min Normalizado"] = (df_duracion["Length in Min"] - mean_rating) / std_rating
    # Calcular el promedio de IMDB Rating Normalizado para cada director
    promedios_normalizados = df_duracion.groupby("Release Year")["Length in Min Normalizado"].mean()
    # Mostrar los promedios normalizados
    print(promedios_normalizados)
  
    
"""
Comparar las medias de los ratings de las películas de Jesús Franco y Lesley Selander. 
Si las medias son distintas entre sí ¿cuál director dirigió mejores películas?   
"""
def comparacion_entre_directores(datos):
    media_por_ratings=datos[["Director","IMDB Rating"]].groupby("Director").mean()
    datos[datos["Director"].isin(["Jesús Franco","Lesley Selander"])].boxplot("IMDB Rating",by="Director")
    plt.plot([1,2],media_por_ratings.loc[["Jesús Franco","Lesley Selander"]],"o")
    #Achico el rango del grafio
    plt.ylim(0,3000)
    plt.title("Comparación entre Ratings de directores")
    plt.suptitle(" ")
    plt.xlabel("Director")
    plt.ylabel("Ratings")
    #Calculo los promedios
    promedios = datos.groupby('Director')['IMDB Rating'].mean()
    promedios_filtrados = promedios.loc[["Jesús Franco","Lesley Selander"]]
   
    #guardo el grafico como una imagen
    plt.savefig("comparacion.por.directores.histograma.png")
    plt.close()
    
    print(promedios_filtrados)


#Sin normalizar me da que Jesus es mejor pero tiene mayor cantidad de peliculas 
#hechas para ello hay que normalizar 
def comparacion_entre_directores_normalizado(datos):
    df_directores = datos[(datos["Director"] =="Jesús Franco")|(datos["Director"] =="Lesley Selander")]
    # Calcular la media y la desviación estándar de la columna IMDB Rating
    mean_rating = df_directores['IMDB Rating'].mean()
    std_rating = df_directores['IMDB Rating].std()
    # Aplicar la normalización (z-score)
    df_directores = df_directores.copy()
    df_directores['IMDB Rating Normalizado'] = (df_directores['IMDB Rating'] - mean_rating) / std_rating
    # Calcular el promedio de IMDB Rating Normalizado para cada director
    promedios_normalizados = df_directores.groupby('Director')['IMDB Rating Normalizado'].mean()
    # Mostrar los promedios normalizados
    print(promedios_normalizados)
    
    media_por_ratings= df_directores[["Director","IMDB Rating Normalizado"]].groupby("Director").mean()
    df_directores[df_directores["Director"].isin(["Jesús Franco","Lesley Selander"])].boxplot("IMDB Rating Normalizado",by="Director")
    plt.plot([1,2],media_por_ratings.loc[["Jesús Franco","Lesley Selander"]],"o")
    #Achico el rango del grafio
    plt.ylim(-1,4)
    plt.title("Comparación entre Ratings de directores")
    plt.suptitle(" ")
    plt.xlabel("Director")
    plt.ylabel("Ratings")

    #guardo el grafico como una imagen
    plt.savefig("comparacion.por.directores.normalizado.histograma.png")
    plt.close()
    
    

