# Dibuja tus mapas en R usando archivos de formato Shapefile

Este breve tutorial te mostrará como graficar los mapas y modificar sus atributos. Al finalizar el tutorial podrás crear un mapa de densidad poblacional como el mostrado a continuación.

![alt text](grafica2.png)

## Comenzando 🚀
Para que todos las librerías se instalen correctamente es recomendable instalar las última versión de [R](https://cran.r-project.org/) y su IDE [RStudio](https://www.rstudio.com/) con su correspondiente complemento [RTools](https://cran.r-project.org/bin/windows/Rtools/rtools40.html).

Para este artículo vamos a utilizar archivos de formato Shapefile. Si todavía no sabes de qué se trata, te explicamos a continuación.

Un archivo Shapefile contiene al menos:
* .shp - Un archivo tipo shape, es la geometría misma.
* .shx - Un archivo tipo index, tiene las posiciones indexadas del archivo shp.
* .dbf - un archivo tipo attribute, tiene los atributos de cada forma en una columna, es de tipo dBase IV.

Adicionalmente la carpeta donde se encuentran dichos archivos pueden contener otros archivos de formato .prj o .sbn que aportan más datos de la geometria, o que pueden ser usados en otros programas de sistemas de información geógrafico.

La librería que nos ayudara a importar este tipo de archivos es ```rgdal```, y la librería que convertira los archivos importados en una tabla de datos es ```broom``` (los datos que nos interesan dentro las tablas son latitud y longitud en formato decimal que son coordenadas geográficas de nuestro planeta estas se convierten a nuestros datos x e y para nuestro gráfico) al tenerla en una tabla podemos usar la opción de graficarla como polígonos usando ```ggplot2```.


#### Donde conseguir los archivos shapefile
Muchos de estos archivos Shapefile representan mapas de nuestros Estados, por lo que estan disponibles de manera gratuita en la mayoria de los casos. Otros son de paga y están más completos y/o actualizados y/o poseen datos específicos. Aqui algunos web que ofrecen mapas.}

[data.humdata.org](https://data.humdata.org/) Para shapefiles varios países del mundo. (Algunos están desactualizados)

[geo.gob.bo](https://geo.gob.bo/geonetwork/srv/spa/catalog.search#/home) Para shapefiles de Bolivia

Es recomendable buscar dentro de las bases de datos de instituciones gubernamentales de los lugares donde quieras hacer los mapas.

### Instalación de pre-requisitos 🔧 📋

Necesitaremos las siguientes librerías para nuestro ejemplo. Encaso de que no se las tenga instaladas podemos usar los siguientes comandos:

```python
install.packages("ggplot2")    # Librería para graficar
install.packages("rgdal")      # Librería para abrir archivo de formato shapefiles (datos geográficos)
install.packages("broom")      # Librería usada para extraer datos del archivo importado de shapefiles
install.packages("tidyverse")  # Librería usada par juntar tablas
install.packages("rio")        # Librería usada para importar datos de archivos csv
install.packages("dplyr")     #Librería usada para agrupar por valores de columnas
install.packages("extrafont") # Librería usada para modificar e importar los font de windows.

```
_(Recuerde que para ejecutar una linea de Comando en el Editor de RStudio Es con Ctrl+Enter o puede escribirlo directamento en la Consola)_

## Preparación de los datos para graficar ⚙️

Nuestra base de datos fue descargada [GeoBolivia](https://geo.gob.bo), [INE Bolivia](https://www.ine.gob.bo/) y [geodatos.net](https://www.geodatos.net/coordenadas/bolivia), una vez descargados los datos fueron depurados para sólo tener los datos de nuestro interés (Puede descargar los datos depurados aquí)
Abrimos nuestras librerías requeridas con:
```python
library(ggplot2)    
library(rgdal)       
library(broom)      
library(tidyverse)  
library(rio)
library(dplyr)
library(extrafont)
```
Redireccionamos el directorio actual a nuestro directorio de trabajo.

```python
setwd("../mypath/") # Redirecciona el directo actual a nuestro directorio de trabajo

```
Importando nuestros archivos shapefiles.
```python
shapefile = readOGR(dsn = ".",layer = "departamentos_geo", encoding = 'utf-8', use_iconv = TRUE)
```
- ```dsn``` directorio dentro de la carpeta donde se encuentran ficheros shapefiles, si los shapefiles estan dentro del directorio actual simplemente se pone "."
- ```encoding, use_iconv``` Indica a la función que debe leerse con la codificación "utf-8" y que si debe activarse la codificación con "TRUE". esto es necesario pues nuestro archivo importado, pues contiene caracteres con "ñ" y vocales con tíldes.

Para observar la estructura de nuestro shapefile importado use ```View(shapefile)```.

Extrayendo datos en geotable para graficar y mostrando su cabecera  
```
geotable=tidy(shapefile)
head(geotable)
```
```python
> head(geotable)
# A tibble: 6 x 7
   long   lat order hole  piece group id   
  <dbl> <dbl> <int> <lgl> <fct> <fct> <chr>
1 -65.8 -18.0     1 FALSE 1     0.1   0    
2 -65.8 -18.0     2 FALSE 1     0.1   0    
3 -65.8 -18.0     3 FALSE 1     0.1   0    
4 -65.8 -18.0     4 FALSE 1     0.1   0    
5 -65.8 -18.0     5 FALSE 1     0.1   0    
6 -65.8 -18.0     6 FALSE 1     0.1   0    
```
Notesé que geotable no poseé las etiquetas de los nombres de las regiones a graficar, esto lo arreglamos con:

```python
#Añadiendo una columna id para poder juntar las columnas de nuestro geotable con los datos correspondientes
shapefile$id<-row.names(shapefile)

#Añadiendo a geotable los datos que faltan de shapefile, lo junta por el id
geotable<-left_join(geotable,shapefile@data, by = "id")
```
Ahora puede notar que se le añadió el nombre a sus respectivas coordenadas, use para ver ```head(geotable)```
Funciones auxiliares:
* ```shapefile$id <- ``` Crea una nueva columna en shapefile o la reemplaza.
* ```row.names(shapefile) ``` Extrae los nombres de las filas del shapefile que por defecto es una numeración que va desde 0 y coincide con el id de nuestro geotable.
* ```shapefile@data ``` Accede a la tabla o dataframe "data" de nuestro shapefile.
* ```left_join(tabla1, tabla2, by = clave) ``` Junta dos tablas por izquierda, es decir añade valores que faltan de "tabla2" a la "tabla1" de acuerdo al código "clave" o columna común.

Ahora importamos nuestra tabla con los datos de población por departamento con(con ```header=TRUE``` nos aseguramos que la primera fila sean los nombres de las columnas):

```python
#Importando la tabla de datos de población
poblacion<-import("departamentospoblacion.csv", header=TRUE)
```
Notesé que cambiamos el nombre nuestra columna de en población DEPARTAMENTO por DEPARTAMEN para que coincidan nuestra culumnas para luego poderlas juntar con ```left_join()```.
```python
#Cambiando el nombre de la columna de DEPARTAMENTO POR DEPARTAMEN para poder juntar tablas segun nombre
#Dado que el nombre de los departamentos dentro del shapefile es DEPARTAMEN vemos conveniente cambiarlo a este.
colnames(poblacion)[colnames(poblacion)=="DEPARTAMENTO"]<-"DEPARTAMEN"
#Juntamos en datos ambas tablas
datos<-left_join(geotable,poblacion, by="DEPARTAMEN")
```
## Mapa con ggplot2 ⚙️
Ahora podemos graficar :
```python
ggplot() +
  geom_polygon(data=datos, aes(x=long, y=lat, group=group, fill=Poblacion2022)) +
  coord_equal()+labs(fill="POBLACION")
```
* ```geom_polygon(data, aes(x,y,group,fill))```Dibuja poligonos con la tabla "data" muestra la estetica con "aes()", x, y son los valores en ejes de las absisas y las ordenadas, estan agrupadas por el valor de la columna "group" y rellenadas con base a los valores de la columna "fill".
* ```coord_equal()```Obliga a la grafica que la relación entre coordenadas sea 1:1.
* ```lab(fill)```Pone el título a la leyenda con "fill".

![alt text](grafica1.png)

## Mejorando la presentación de nuestro mapa ⚙️
Hay varias cosas que podemos modifcar para mejorar la apariencia de nuestra gráfica, como poner un título, cambiar los colores, cambiar el fondo, cambiar el formato de nuestra layenda, en esta sección mostramos como hacer esos cambios para nuestro ejemplo.

Inicialmente podemos extraer los valores de población y ponerlo como etiquetas dentro de nuestro mapa, para obtener sus ubicaciones dentro del mapa obtenemos un promedio de las coordenadas máximas y mínimas con funciones de la libería ```dplyr```
``` python
etiquetas_poblacion <- datos %>% group_by(DEPARTAMEN) %>%
  summarise(label_long=mean(range(long)), label_lat=mean(range(lat)),
            pob=mean(Poblacion2022))
```
Qué hicimos?

* ```tabla0 %>% funcion0 %>% funcion1 ...```%>% Conocido como pipe operatortoma como argumento la "tabla0" para la "funcion0" y luego los resultados de la "funcion0" las utiliza como argumentos para "función1" y así sucesivamente.
* ```group_by(col) %>% summarise(col1=accion1, col2=accion2 ...)``` Agrupa los datos en función del valor de columna "col" y con "summarise()" usa los datos agrupados para devolver nuevos valores "col1", "col2" ... que pueden estar en función de los valores que estan agrupados.
* ```range(c)``` Extrae los valores maximo y mínimo de un rango de datos "c".
* ```mean(d)```Devuelve el valor medio del vector d.
Si queremos incluir nuevas fuentes para el tipo de letra para nuestro mapa usamos los siguientes comandos(nos pedirá confirmación para realizar la importación de fuentes y tardará unos minutos en hacer la importación, con el comando ```fonts() ``` veremos las fuentes disponiles):
```
extrafont::font_import("C:/Windows/Fonts")
loadfonts(device = "win")
fonts()
```
Con nuestras etiquetas podemos mejorar la visualización de datos, Usamos lo siguientes comandos para incluir las etiquetas y mejorar la apariencia.
```python
ggplot() +
  geom_polygon(data=datos, aes(x=long, y=lat, group=group, fill=Poblacion2022)) +
  coord_equal()+ theme_void() +
  geom_text(size=4.5,alpha=0.9,fontface="bold", data = etiquetas_poblacion,
            mapping = aes(x = label_long, y = label_lat,
                          label = format(pob, big.mark=" "), color=pob)) +
  labs(title="Población estimada de Bolivia por departamentos para el año 2020",
       fill="Habitantes",caption="Datos:INE Boliva; GeoDatos: GeoBolivia") +
  scale_colour_gradientn(colours = c("black", "black","white","white","white"),
                         guide="none") +
  scale_fill_continuous(low = "#C4FFD1", high = "#05693E", guide="colorbar",
                      labels = scales::label_number(big.mark=" ")) +
  theme(plot.title=element_text(size=14,face="bold", family="Helvetica",hjust = 0.5),
        legend.title = element_text(size = 12, family="Rubik"),
        plot.caption = element_text(family="Helvetica"))
```    
* ```theme_void()``` Eliminamos el fondo y los ejes de nuestra gráfica.
* ```geom_text(size, alpha, fontface, data mapping=aes(x,y,label),color)``` Dibuja texto dentro del mapa sacando datos de "data" con las coordenadas "x" e"y" muestra los valores de la columna "label" las diferencia con el valor de la columna "color". Con "size", "alpha" y "fontface" etablecemos el tamaño, la opacidad y la estetica del texto respectivamente.
* ```format(v, big.mark)``` Le da el formato al valor "v" de separación de miles con "big.mark" (En nuestro caso el separados de miles es sólo el espacio" ").
* ```labs(title, fill, caption)``` Pone el texto de los títulos, con "title", "fill", "caption" se pone el texto del título, la leyenda y el pie del gráfico respectivamente.
* ```scale_colour_gradientn(colours,guide)``` Aplica una escala de colores a todos los valores asignados a la argumento "color" en nuestro ejemplo tenemos asignado color dentro de la función  "geom_text(...aes(..color=pob...)...)"", es decir los valores de "pob" estarán coloreados según los valores de "colours". (la sintaxis "color" "colors" puenden intercambiarse sin problema con "colour" y "colours"). "guide = "none" " evita que la leyenda de esta escala se muestre.
* ```scale_fill_continuous(low, high, guide, labels)``` Aplica una escala de colores continua a los valores asginados a "fill" en nuestro ejemplo tenemos asignado "fill" dentro del a función geom_polygon(... aes(...fill = Poblacion2022...)...), es decir los valores de la columna "Poblacion2022" estaran afectados por esta función. en "low" determinamos el color que va a tener el valor más bajo de "fill" y con "high" el color que va a tener el más alto valor. "guide" nos permite mostrar nuestra leyenda en forma de colorbar. con "labels" modificamos la apariencia en la escala de nuestro colorbar.
* ```scales::label_number(big.mark=" ")``` llama a la librería "scales" y aplica la función "label_number()" Con esto modificamos la apariencia de los números de nesutra leyeda poniendole un espacio " " como separador de miles.(Podemos hacer esto en vez de usar scales::funcion() en vez de  library(scales) funcion())
* ```theme(plot.title, legend.title, plot.caption)``` Modificamos con "plot.title", "legend.title" y "plot.caption" la apariencia del título, el título de la leyenda y el pie de gráfico respectivamente.
* ```element_text(size, face, family, hjust)``` Modificamos con "size", "face", "family" y "hjust" el tamaño, la estética, el tipo de texto, y la posición en horizontal del texto.

![alt text](grafica2.png)

## Añadiendo puntos a nuestro mapa ⚙️

Incluyamos la ubicación de ciudades capitales de departamento a nuestro mapa.

```python
#Importamos la localización de las ciudades capitales
ciudades = import("ciudades.csv")

ggplot() +
  geom_polygon(data=datos, aes(x=long, y=lat, group=group, fill=DEPARTAMEN),
               color="gray", size=0.5) +
  geom_point(alpha=0.7,data=ciudades, mapping = aes(x=lat, y=long,colour=Ciudad),
             size=5) +
  coord_equal()+labs(title="Capitales de Departamento en Bolivia",
                     color="Ciudades Capitales",caption="Fuente: geodatos.net") +
  scale_fill_brewer(palette = 'PuBuGn', guide="none") +
  scale_color_manual(values=rainbow(9)) +
    theme_void() +
  theme(plot.title=element_text(size=14,face="bold", family="Helvetica",hjust = 0.5),
        legend.title = element_text(size = 12, family="Rubik"),
        plot.caption = element_text(family="Helvetica"))
```
* ```geom_point(alpha, data, mapping = aes(x, y, colour), size)``` Grafica puntos en el plot, con "alpha" "data", "size" modificamos la opacidad, tabla a usarse y el tamaño de los puntos, con mapping asignamos la estética, "x" e "y" asignamos las columnas para los valores de los ejes y con "colour" la columna que se va usar para asignarles colores, a este se le puede asignar un solo color también si se quiere.

* ```scale_fill_brewer(palette, guide)``` Es una función que aplica una escala de colores tipo brewer a todos los objetos asignados a "fill"."pallete" permite la selección de una paleta especifica y guide asigna la pressentación de la leyenda.
* ```scale_color_manual(values)``` Aplica una escala de color manual a todos lo objetos asignado a "color". "values" asginamos los colores de nuestra escala.
* ```raibow(9)``` Devuelve un vector con 9 colores del arcoiris.

![altext](grafica3.png)
#### Como asignar los colores
Puedes asignar los colores simplemente usando su nombre en inglés. Para el blanco es **white**, para el rojo, **red**. También puedes usar su código hexadeciamal, como  **#FF4500** para el rojo anaranjado. Puedes agruparlos en una escala de colores, usando la función `c("red","#FF4500"...)`. Una página recomendable para seleccionar colores y obtener su código de color con un click es [r-chart.com/colors/](https://r-charts.com/colors/).
Tambien puede usar la funciones auxiliares que ofrec R como scale_color/fill_brewer/viridis_ estas proporcionan escalas predefinidas que podrían mejorar el impacto visual.

## Com guardar nuestros mapas ✒️
RStudio ofrece la posiblidad e exportar fácilmente desde su menú ubicado encima de la vista previa del gráfico "Export". Pero veces podemos optar por guardar nuestro mapa con mayor calidad o cierto formato, para ello podemos usar ggsave() que nos permite exportar o guardar nuestro último gráfico ejecutado.


```python
ggsave(filename="grafica1.png", path = ".../mypath/", scale=1, device="png", dpi=320)
```

Guarda el mapa con el nombre "filename" en la ruta "path" con la escala y formato de "scale" y "device". COn "dpi" indicamos la cantidad de pixeles por pulgada que es la calida de nuestro archivo a exportar.

[Descarga lo archivos de este ejemplo](https://github.com/)

## Autores ✒️

* **Ever Vino** - ** - [EverVino](https://github.com/EverVino)

## Licencia 📄

Bajo la Licencia (CC BY SA 4.0)

## Referencias 📄

* [Instituto Nacional de Estadística Bolivia](https://www.ine.gob.bo) 📢
* [geo](https://www.rdocumentation.org)
* [Robinlovelace](https://github.com/Robinlovelace/Creating-maps-in-R)
* [Documentacion de R](https://www.rdocumentation.org)

---
