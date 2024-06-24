# Proyecto TFG: Implementación de Métodos de Generación Procedimental de Contenidos Basados en Machine Learning para el Juego Binding of Isaac

## Contexto del proyecto

Este proyecto de Trabajo de Fin de Grado (TFG) se enfoca en la generación de niveles para el juego Binding of Isaac utilizando algoritmos genéticos y autómatas celulares. Aunque el clon del juego no es completamente original, mi contribución principal ha sido en la generación de niveles donde se centra mi Trabajo de Fin de Grado.

## The Binding of Isaac: Python

#### Copia del videojuego The Binding of Isaac ([2011](https://store.steampowered.com/app/113200/The_Binding_of_Isaac), [2014](https://store.steampowered.com/app/250900/The_Binding_of_Isaac_Rebirth/))

**The Binding of Isaac** es un shooter en 2D con niveles generados automáticamente y elementos de juegos de rol y **roguelike**. Acompañando a Isaac en sus aventuras, los jugadores encontrarán numerosos tesoros inusuales que cambiarán la apariencia de Isaac y le otorgarán habilidades sobrehumanas para derrotar a hordas de criaturas misteriosas, descubrir muchos secretos y abrirse paso hacia la salvación.

### Lanzamiento

1. Instalar la versión de python **3.10**+
(Probado en la versión **3.10.12**)
2. Clonar el repositorio y navegar hacia él:
```commandline
git clone git@github.com:manuelvico0102/Generacion-Procedimental-The-Binding-of-Isaac.git
cd ./Generacion-Procedimental-The-Binding-of-Isaac
```

3. Instale todas las bibliotecas enumeradas en el archivo `requiremenets.txt`:
```commandline
pip install -r ./requirements.txt
```

4. Iniciar el juego:
```commandline
python ./main.py
```

5. Para recopilar el archivo .exe, debe instalar la biblioteca **pyinstaller** y ejecutar el siguiente comando.
```
pyinstaller --onefile --noconsole --icon="./src/data/images/icon/64x64.ico" --add-data="./src/*:." ./main.py
```

6. El ejecutable se encontrará en la carpeta `dist`.


### Capturas de pantalla
![isaac_IPU55ODdsb](https://user-images.githubusercontent.com/104463209/215344266-21f53dc1-2f5f-46b0-9c60-246aeca3a754.png)
![isaac_2XHjvtHyfc](https://user-images.githubusercontent.com/104463209/215344280-3b2338db-5f86-469e-b109-7487e46fa72d.png)
![isaac_XZxB7cC1A9](https://user-images.githubusercontent.com/104463209/215344300-e97a3a59-0826-4c84-9bd6-f4e24f5fb280.png)
![isaac_CUBLM1jKSM](https://user-images.githubusercontent.com/104463209/215344301-43a5dd86-60a0-46d7-8e86-ed1911395c1e.png)
![isaac_SlTizpsGhf](https://user-images.githubusercontent.com/104463209/215344303-4f7429f5-0218-463b-87c5-8281e5ff4208.png)
![isaac_ZLJmv4O1KA](https://user-images.githubusercontent.com/104463209/215344306-8ae8b4fa-7bbd-4c11-aa13-40c14ed945e5.png)
![isaac_d6y5od8WbZ](https://user-images.githubusercontent.com/104463209/215344311-ae9b537e-16ad-4ad8-8a40-781df2877e44.png)
![isaac_hbMbEcGsDO](https://user-images.githubusercontent.com/104463209/215344317-f50f5e60-d73d-4c33-ab05-3f68c221e3dc.png)

### Parte explicativa.

El proyecto original "The Binding of Isaac: Python" fue creado por un equipo de tres personas del Liceo de la Academia Yandex (Kirill Lesov, Ivan Dyadechkov y Rostislav Zagitov)

Para la implementación, se utilizaron las bibliotecas **pygame** (para dibujar sprites y manejar colisiones) y **sqlite3** (para guardar los resultados de las ejecuciones).

En este proyecto de fin de grado, se ha trabajado con la generación de niveles para mejorar el proyecto original, como se menciona al comienzo.
