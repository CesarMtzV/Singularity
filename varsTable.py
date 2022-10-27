from MemoryManager import MemoryManager

memory = MemoryManager()

class VariablesTable:
    "Esta clase contiene los métodos y variables necesarias para manejar la tabla de variables del compilador"

    def __init__(self) -> None:
        self.vars_table = {
            "global" : {
                "type" : "global_function",
                "vars" : {}
            }
        }
        self.current_function = ""
        self.current_type = ""
        self.current_array_size = 0
        self.global_scope = True

    def add_function(self, function_name :str, is_void_function :bool) -> None:
        """
        Agregar una funcion al diccionario de funciones
        """

        self.current_function = function_name
        if is_void_function:
            self.current_type = "void"
        
        # Si la funcion no existe en tabla de variables
        if self.current_function not in self.vars_table:

            # Agregar la función
            self.vars_table[self.current_function] = {
                "type": self.current_type,
                "vars": {},
            }

            # Parche Guadalupano para funciones tipo
            if not is_void_function:
                # Revisar si ya existe una variable con el nombre de la funcion
                if self.current_function not in self.vars_table["global"]["vars"]:
                    self.vars_table["global"]["vars"][self.current_function] = {
                        "type": self.current_type,
                        "memory_position": memory.malloc(1, "global", self.current_type)
                    }
                else:
                    raise VarsTableException(f"Function '{self.current_function}' already exists as a global variable")
            
            # Liberar memoria local para las variables (en caso de tener mas de una funcion)
            memory.dealloc()

        else:
            raise VarsTableException(
                f"Function '{self.current_function}' has already been declared!"
            )

    def add_function_parameters(self, param_name):
        """
        Agregar los parametros de una funcion a la tabla de simbolos
        """

        if param_name not in self.vars_table[self.current_function]["vars"]:
            self.vars_table[self.current_function]["vars"][param_name] = {
                "type": self.current_type,
                "memory_position" : memory.malloc(1, "local", self.current_type)
            }
        else:
            raise VarsTableException(
                f"Variable '{param_name}' has already been declared as another parameter!"
            )
    
    def add_variable(self, p):
        """Agregar una variable a la tabla de simbolos usando el scope correcto (global o local)"""
        # TODO: Hay que revisar otra forma de obtener los demás parámetros (tipo, si es arreglo o matriz, etc)
        current_var = p[-1] 
        
        # Revisar si el current_scope es global y la variable ya se habia declarado
        if self.global_scope:
            if current_var not in self.vars_table["global"]["vars"]:
                self.vars_table["global"]["vars"][current_var] = {
                    "type" : self.current_type,
                    "memory_position" : memory.malloc(1, "global", self.current_type)
                }
            else:
                raise VarsTableException(f"Global variable '{current_var}' already exists")
        else:
            if current_var not in self.vars_table[self.current_function]["vars"]:
                self.vars_table[self.current_function]["vars"][current_var] = {
                    "type" : self.current_type,
                    "memory_position" : memory.malloc(1, "local", self.current_type)
                }
            else:
                raise VarsTableException(f"Local variable '{current_var}' already exists")


class VarsTableException(Exception):
    """Clase personalizada para los tipos de errores en la tabla de variables"""

    pass
