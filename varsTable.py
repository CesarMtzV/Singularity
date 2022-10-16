class VariablesTable:
    "Esta clase contiene los métodos y variables necesarias para manejar la tabla de variables del compilador"

    def __init__(self) -> None:
        self.vars_table = {
            "global" : {
                "type" : None,
                "vars" : {}
            }
        }
        self.initialized = False
        self.program_name = ""
        self.current_function = ""
        self.current_function_type = ""
        self.current_var = ""
        self.current_type = ""
        self.current_array_size = 0
        self.global_scope = True

    def add_function(self, p):
        """
        Agregar una funcion al diccionario de funciones
        """

        self.current_function = p[-1]

        if self.current_function not in self.vars_table:
            self.vars_table[self.current_function] = {
                "type": self.current_function_type,
                "vars": {},
            }
            # print(self.vars_table)
        else:
            raise VarsTableException(
                f"Function '{self.current_function}' has already been declared!"
            )

    def add_function_parameters(self, p):
        """
        Agregar los parametros de una funcion a la tabla de simbolos
        """

        self.current_var = p[-1]

        if self.current_var not in self.vars_table[self.current_function]["vars"]:
            self.vars_table[self.current_function]["vars"][self.current_var] = {
                "type": self.current_type
            }
        else:
            raise VarsTableException(
                f"Variable '{self.current_var}' has already been declared as another parameter!"
            )
    
    def add_variable(self, p):
        """Agregar una variable a la tabla de simbolos usando el scope correcto (global o local)"""
        current_var = p[-1] # TODO: Hay que revisar otra forma de obtener los demás parámetros (tipo, si es arreglo o matriz, etc)
        
        # Revisar si el current_scope es global y la variable ya se habia declarado
        if self.global_scope:
            if current_var not in self.vars_table["global"]["vars"]:
                self.vars_table["global"]["vars"][current_var] = {
                    "type" : "VARIABLE GLOBAL" # TODO: Cambiar VARIABLE por el parámetro correcto. Esto es solo un dummy
                }
            else:
                raise VarsTableException(f"Global variable '{current_var}' already exists")
        else:
            if current_var not in self.vars_table[self.current_function]["vars"]:
                self.vars_table[self.current_function]["vars"][current_var] = {
                    "type" : "VARIABLE LOCAL" # TODO: Cambiar VARIABLE por el parámetro correcto.
                }
            else:
                raise VarsTableException(f"Local variable '{current_var}' already exists")


class VarsTableException(Exception):
    """Clase personalizada para los tipos de errores en la tabla de variables"""

    pass
