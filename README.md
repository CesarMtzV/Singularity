# Singularity

## Manual de usuario

### Requerimientos del proyecto

Para ejecutar el proyecto, es necesario contar con **Python 3** y tener instalada la librería de [PLY](https://www.dabeaz.com/ply/).

### Estructura básica del programa

Un programa escrito en _Singularity_ tiene la siguiente estructura:

```
VARIABLES_GLOBALES (opcionales)

CLASES (opcionales)

FUNCIONES (opcionales)

main(){
    output << "HELLO WORLD";
}
```

### Creación de variables

_Singularity_ cuenta con la capacidad de manejar variables Int, Float, Bool, y String. Además de arreglos y matrices de los tipos antes mencionados.

Ejemplo:

```
int a;
float b;
bool t;
string s;
```

Las variables siempre son declaradas al inicio del programa y al inicio de cada función y método de clase. Los nombres de las variables deben comenzar con una letra, y solo pueden contener letras y dígitos.

### Operaciones aritméticas

Las operaciones aritméticas permitidas son Suma, Resta, Multiplicación y División. Las operaciones se pueden realizar tanto con número constantes o con variables previamente declaradas.

Ejemplo:

```
int a;
int b;
int result;

main(){

    a = 2;
    b = 4;

    result = 3 + 3;
    output << result;

    result = a + b;
    output << result;

    result = a - b;
    output << result;

    result = a * b;
    output << result;

    result = a / b;
    output << result;

}
```

### Condicionales

Las condiciones se manejan con un `if` y `else`. _Singularity_ maneja los siguientes operadores relacionales:

-   Menor que: `<`
-   Mayor que: `>`
-   Menor o igual que: `<=`
-   Mayor o igual que: `>=`
-   Igual: `==`
-   No igual: `!=`
-   AND: `&&`
-   OR: `||`

Ejemplo:

```
int x;
int y;
bool b;
bool c;


main(){

    x = 10;
    y = 5;

    if(x >= 5){
        output << "HELLO";
    } else {
        output << "WORLD;
    }

}

```

### Ciclos

Se cuenta con dos tipos de ciclos: `while` y `for`. Para el ciclo `for` se debe haber declarado previamente la variable que se usará como iterador.

Ejemplo:

```
int x;
int y;

main(){

    x = 0;

    while(x < 10){
        output << x;
        x = x + 1;
    }

    for (y in range(1, 10)){
        output << y;
    }

}
```

### Funciones

Las funciones se declaran despues de las variables y antes de la función main. Su declaración debe iniciar con la palabra `function` y se debe especificar el tipo de retorno, si no tiene se debe especificar su tipo como `void`.

Al momento de hacer una llamada a la función, se debe añadir al inicio el caracter `@`.

Ejemplo:

```
int globalVar;

function int test1(int x, int y){
    x = y + 1;

    return x;
}

function void test2(){
    output << "Hello world";
}

main(){

    globalVar = @test1(1, 2);

    @test2();

}
```

### Clases

Las clases se declaran después de las variables y antes de las funciones. Cada clase contiene sus atributos, métodos y constructor. El constructor debe llevar el mismo orden en el que se declararon los atributos.

Los métodos llevan la misma estructura que las funciones, con la excepción que deben iniciar con la palabra `method`.

Ejemplo:

```
class ejemplo {
    attributes:
        int attr1;
        float attr2;

    constructor:
        ejemplo(int, float);

    methods:
        method void metodo1(int a, int b){
            a = b + 1;
            output<<"Metodo";
        }

}

function void testFunction(int a){
    output << "test";
}

main(){
    output << "Hello";


}
```

Nota: Esta versión de _Singularity_ no cuenta con la instanciación de los objetos, polimorfismo y herencia. Solo la declaración de clases y su generación de cuádruplos, así como el guardado de información en el directorio de variables.

### Ejecución del programa

Para ejecutar un programa de _Singularity_, se debe ejecutar con **Python 3** el programa de **VM.py**, incluyendo como argumento en el comando el nombre del archivo que contiene el código a ejecutar.

Ejemplo:

```bash
python3 VM.py testSingularity.txt
```

Esto genera un archivo `output.sgo` el cual es leido por la máquina virtual y después ejecutado.

## Bitácora de avances

### Avance 1: Léxico Sintaxis

-   Se definió a Singularity como un lenguaje orientado a objetos
-   Se crearon las primeras versiones de los diagramas de sintaxis
-   Creación del lexer
    -   Creación de casos de prueba usando PyTest
-   Primera versión del Parser
    -   Hay errores de sintaxis inesperados que se necesitan solucionar

### Avance 2: Semántica básica de variables y Cubo Semántico

-   Se corrigieron los errores iniciales del parser
-   Se modificaron algunos diagramas de sintaxis
-   Se terminó el cubo semántico
-   Se inició con la tabla de variables

### Avance 3: Semántica, Generación de Código de Expresiones y Estatutos Lineales

-   Se corrigieron mucho más a fondo los problemas presentes en la gramática
-   Se inició la implementaci´øn de algunos puntos neurálgicos
-   Se corrigió el error de la declaración de variables globales

### Avance 4: Generación de Código de Estatutos Condicionales: Ciclos

-   Se inició con la generación de cuádruplos para estatuso lineales
    -   Lectura, Escritura y Return
    -   Operaciones aritméticas
    -   Operaciones booleanas

### Avance 5: Generación de Código de Funciones

-   Se agregaron los puntos neurálgicos para la generación de estatutos no lineales:
    -   IF
    -   WHILE
-   Se agregaron la mayoría de los puntos neurálgicos para la declaración y llamada de funciones
    -   Falta terminar algunos puntos y solucionar bugs
-   Se creó la maquina virtual y ya procesa el código de operacion de OUTPUT

### Avance 6: Generación de Código de Arreglos y Ejecución de estatutos secuenciales y condicionales en Máquina Virtual

-   Se terminó la generación de cuádruplos para funciones
-   Ejecución de código para ASSIGN y OUTPUT
-   Ejecución de código para sumas, restas, multiplicación y división
-   Inicialización de memoria en la Máquina Virtual
-   Ejecución de código de condicionales
-   Generación de cuádruplos para arreglos y matrices

### Avance 7: Máquina virtual: Ejecución de módulos y arreglos y Generación de cuádruplos para clases

-   Creación de cuádruplos para los métodos de clases
-   Clases se guardan en el directorio de funciones
-   Corrección de errores de cuádruplos en arreglos y matrices
-   Primera versión de la documentación
-   Ejecución de ciclos
-   Ejecución de funciones
-   Ejecución del RETURN
