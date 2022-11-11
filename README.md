# Singularity

## Avance 1: Léxico Sintaxis

-   Se definió a Singularity como un lenguaje orientado a objetos
-   Se crearon las primeras versiones de los diagramas de sintaxis
-   Creación del lexer
    -   Creación de casos de prueba usando PyTest
-   Primera versión del Parser
    -   Hay errores de sintaxis inesperados que se necesitan solucionar

## Avance 2: Semántica básica de variables y Cubo Semántico

-   Se corrigieron los errores iniciales del parser
-   Se modificaron algunos diagramas de sintaxis
-   Se terminó el cubo semántico
-   Se inició con la tabla de variables

## Avance 3: Semántica, Generación de Código de Expresiones y Estatutos Lineales

-   Se corrigieron mucho más a fondo los problemas presentes en la gramática
-   Se inició la implementaci´øn de algunos puntos neurálgicos
-   Se corrigió el error de la declaración de variables globales

## Avance 4: Generación de Código de Estatutos Condicionales: Ciclos

-   Se inició con la generación de cuádruplos para estatuso lineales
    -   Lectura, Escritura y Return
    -   Operaciones aritméticas
    -   Operaciones booleanas

## Avance 5: Generación de Código de Funciones

-   Se agregaron los puntos neurálgicos para la generación de estatutos no lineales:
    -   IF
    -   WHILE
-   Se agregaron la mayoría de los puntos neurálgicos para la declaración y llamada de funciones
    -   Falta terminar algunos puntos y solucionar bugs
-   Se creó la maquina virtual y ya procesa el código de operacion de OUTPUT
