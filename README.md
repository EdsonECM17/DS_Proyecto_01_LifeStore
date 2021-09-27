# DS_Proyecto_01_LifeStore
 Codigo para dar solución al proyecto 1 del Curso de Data Science de Emtech.
 
## Descripción del proyecto
LifeStore es una tienda en linea de productos de computación. Recientemente, se ha detectado una acumulación de inventario, así como reducción en las búsquedas y ventas de muchos productos de su catálogo.

En el presente proyecto, se desarrolla un programa que permita al usuario acceder a registros de la empresa y poder hacer distintos tipos de consultas. Para poder realizar cualquier consultas, es necesario verificar que el usuario pueda ver dicha información, por lo que también se incluya una validación de ingreso.

Los usuarios permitidos se encuentran definidos en un archivo .CSV, donde se guardan datos como el nombre de la persona, su nombre de usuario y contraseña.

## Instrucciones de uso
Al usar librerías externas, es necesario tenerlas instaladas en el ambiente donde se vaya a ejecutar el programa para garantizar un ejecución correcta. La primera condición para garantizar la ejecución es que el ambiente virtual cuente con Python instalado. A continuación se describen instrucciones para primer uso y cualquier uso posterior.

### Primer uso
Después de descargar el repositorio, se accede por consola a la carpeta code.

En la misma consola, se ejecuta el siguiente comando para instalar la herramienta virtualenv. Esta herramienta se usa para crear ambientes virtuales. Una vez que se tenga la librería, se ejecuta un comando para crear un ambiente virtual y otro comando para activarlo.


```console
pip3 install virtualenv
python -m virtualenv venv
.\venv\Scripts\activate
foo
```
A continuación, se instalan las librerías de terceros de Python que el programa necesita. Para eso, solo se tiene que ejecutar la siguiente linea de comando en la misma consola. El archivo \emph{requirements.txt} cuenta con una lista de todas las librerías necesarias y va instalando cada una en el ambiente virtual.

```console
pip install -r requirements.txt
foo
```

Una vez que se tenga todo instalado, ya se puede ejecutar la función principal. Esto también se puede ejecutar desde la consola, con el comando. 

```console
python .\PROYECTO-01-CASTANEDA-EDSON.py
foo
```

### Usos posteriores
Para usos posteriores, no es necesario instalar librerías a menos que se hagan cambios importantes en el repositorio con nuevas herramientas. Para ejecutar el programa ya con todas las librerías, únicamente hay que activar primero el ambiente virtual desde la carpeta code, y ejecutar la función principal.

```console
.\venv\Scripts\activate
```
```console
python .\PROYECTO-01-CASTANEDA-EDSON.py
foo
```