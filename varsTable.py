class VariablesTable:
    "Esta clase contiene los métodos y variables necesarias para manejar la tabla de variables del compilador"

    def __init__(self) -> None:
        self.vars_table = {}
        self.program_name = ""
        self.current_function = ""
        self.current_function_type = ""
        self.current_var = ""
        self.current_type = ""
        self.current_array_size = 0

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

    def add_global_variable(self, p):
        """Agregar una variable global a la tabla de simbolos"""

        self.current_var = p[-1]

        if self.current_var not in self.vars_table["global"]["vars"]:
            self.vars_table["global"]["vars"][self.current_var] = {
                "type": self.current_type
            }
        else:
            raise VarsTableException(
                f'Global variable \'{self.current_var}\' has already been declared!'
            )

    def add_local_variable(self, p):
        """Agregar una variable local a la tabla de simbolos"""

        self.current_var = p[-1]

        print(self.current_var)
        print(self.vars_table)
        if self.current_var not in self.vars_table[self.current_function]["vars"]:
            self.vars_table["global"]["vars"][self.current_var] = {
                "type": self.current_type
            }
        else:
            raise VarsTableException(
                f'Global variable \'{self.current_var}\' has already been declared!'
            )


class VarsTableException(Exception):
    """Clase personalizada para los tipos de errores en la tabla de variables"""

    pass
