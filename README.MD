
# Proyecto 2 - Gráficas por Computadora

En el presente proyecto se buscó demostrar los conocimientos adquiridos durante la segunda parte del curso Gráficas por Computadora.

Se buscó entregar un Ray Tracer simple en donde se trató de recrear la escena seleccionada para el proyecto por medio de figuras, siendo estas discos y triángulos. Tomando también esto en cuenta se cargaron distintos modelos obj los cuales eran conformados por triángulos. 

Se renderizaron más de 1000 figuras y se aplicaron 4 materiales en donde uno era refractivo, otro material era reflectivo y los demás materiales eran opacos. 

Finalmente cabe mencionar que se aplicaron distintas luces en la escena, tal como: AmbientLight, DirectionalLight y SpotLight, y se renderizó un Enviroment Map para darle un fondo a la escena.

## Referencia/Escena seleccionada

![Scene](https://user-images.githubusercontent.com/64711979/196333490-0bc41275-896d-426f-8a20-9d637494f70d.jpg)


## Renderización

![output](https://user-images.githubusercontent.com/64711979/196333736-dda0f3bb-7b73-4d5c-9f4f-bae05f630784.jpg)

## Escena sin spot light vs Escena con spot light

![Before&After](https://user-images.githubusercontent.com/64711979/196334151-af9f0b6b-82a8-4036-8063-122674512cd7.png)

## Escena con spotlight y taza

![spotlight](https://user-images.githubusercontent.com/64711979/196334652-6afd401e-2df6-4d15-8372-d0bc15b105fd.jpg)


## Observación

Tomar en cuenta que a los modelos se les disminuyó manualmente la cantidad de triángulos en Blender dado que de lo contrario el tiempo de renderizaje hubiera sido mayor.


## 

## ¿Cómo correr el proyecto?

Correr el siguiente comando:

```bash
  python Raytracer.py
```
esperar un par de horas y chequear el resultado en el archivo output.bmp

