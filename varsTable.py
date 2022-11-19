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
        self.constants_table = {
            'int': {}, 
            'float': {}, 
            'bool': {}, 
            'string': {}
        }
        self.current_function = ""
        self.current_type = ""
        self.current_array_size = 0
        self.global_scope = True
        self.function_signature = []
        self.current_class = None
        self.attr_id = 0
        self.current_method = None
        self.method_signature = []

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
                "start_position" : None,
                "size" : {
                    "vars" : { "int" : 0, "float" : 0, "bool" : 0, "string" : 0},
                    "vars_temp" : { "int" : 0, "float" : 0, "bool" : 0, "string" : 0 , "pointer" : 0},
                }
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
        Agregar los parametros de una funcion a la tabla de variables y tabla de parámetros
        """

        if param_name not in self.vars_table[self.current_function]["vars"]:
            
            # Tabla de variables
            self.vars_table[self.current_function]["vars"][param_name] = {
                "type": self.current_type,
                "memory_position" : memory.malloc(1, "local", self.current_type)
            }

            # Sumar al contador de variables
            self.vars_table[self.current_function]["size"]["vars"][self.current_type] += 1

            # Tabla de parámetros
            self.function_signature.append(self.current_type)
            self.vars_table[self.current_function]["PARAMETER_TABLE"] = self.function_signature

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
                    "dimensions" : 0
                }
            else:
                raise VarsTableException(f"Global variable '{current_var}' already exists")
        else:
            if current_var not in self.vars_table[self.current_function]["vars"]:

                # Agregar a la tabla de variables de la funcion
                self.vars_table[self.current_function]["vars"][current_var] = {
                    "type" : self.current_type,
                    "dimensions" : 0
                }

                # Sumar al contador de variables
                # self.vars_table[self.current_function]["size"]["vars"][self.current_type] += 1

            else:
                raise VarsTableException(f"Local variable '{current_var}' already exists")
    
    def assign_memory(self, var :str, size :int, dim :int):
        # Revisar si el current_scope es global y la variable ya se habia declarado
        if self.global_scope:
            if var in self.vars_table["global"]["vars"]:
                self.vars_table["global"]["vars"][var]["memory_position"] = memory.malloc(size, "global", self.current_type)
            else:
                raise VarsTableException(f"Global variable '{var}' does not exist")
        else:
            if var in self.vars_table[self.current_function]["vars"]:

                # Agregar memoria a la variable
                self.vars_table[self.current_function]["vars"][var]["memory_position"] = memory.malloc(size, "local", self.current_type)

                # Sumar al contador de variables
                self.vars_table[self.current_function]["size"]["vars"][self.current_type] += size

            else:
                raise VarsTableException(f"Local variable '{var}' does not exist")
    
    def exists(self, var):
        if var in self.vars_table["global"]["vars"]:
            return "global"
        elif var in self.vars_table[self.current_function]["vars"]:
            return self.current_function
        else:
            raise VarsTableException(f"Variable '{var}' does not exist")
    
    def add_dimensions(self, var):
        if var in self.vars_table["global"]["vars"]:
            self.vars_table["global"]["vars"][var]["dimensions"] += 1
        elif var in self.vars_table[self.current_function]["vars"]:
            self.vars_table[self.current_function]["vars"][var]["dimensions"] += 1
    
    def add_class(self, class_name):
        """Agregar una clase al mismo nivel que las funciones y el scope global"""
        if class_name not in self.vars_table:
            self.vars_table[class_name] = {
                "type" : "class",
                "attributes" : {},
                "constructor" : [],
                "methods" : {},
                "size" : { "int" : 0, "float" : 0, "bool" : 0, "string" : 0},
                
            }
            self.current_class = class_name
        else:
            raise VarsTableException(f"Class '{class_name}' already exists")
    
    def add_attribute(self, attribute_name):
        """Agregar un atributo a la clase actual"""
        if attribute_name not in self.vars_table[self.current_class]["attributes"]:
            self.vars_table[self.current_class]["attributes"][attribute_name] = {
                "type" : self.current_type,
                "memory_position" : memory.malloc(1, "local", self.current_type),
                "id" : self.attr_id
            }
            # Crear la firma del constructor
            self.vars_table[self.current_class]["constructor"].append(self.current_type)
            
            # Id para asignar variables
            self.attr_id += 1

            # Sumar el número de variables usadas
            self.vars_table[self.current_class]["size"][self.current_type] += 1
        else:
            raise VarsTableException(f"Attribute '{attribute_name}' already exists")
    
    def add_method(self, method_name :str, is_void_method :bool) -> None:
        """
        Agregar un método a la clase
        """

        self.current_method = method_name

        if is_void_method:
            self.current_type = "void"
        
        if self.current_method not in self.vars_table[self.current_class]["methods"]:

            # Agregar el método
            self.vars_table[self.current_class]["methods"][self.current_method] = {
                "type": self.current_type,
                "vars": {},
                "start_position" : None,
                "size" : {
                    "vars" : { "int" : 0, "float" : 0, "bool" : 0, "string" : 0},
                    "vars_temp" : { "int" : 0, "float" : 0, "bool" : 0, "string" : 0 , "pointer" : 0},
                }
            }

            # Parche Guadalupano para métodos tipo
            if not is_void_method:
                # Revisar si ya existe un atributo con el nombre del método
                if self.current_method not in self.vars_table[self.current_class]["attributes"]:
                    self.vars_table[self.current_class]["attributes"][self.current_method] = {
                        "type": self.current_type,
                        "memory_position": memory.malloc(1, "local", self.current_type)
                    }
                    # Sumar el número de variables usadas
                    self.vars_table[self.current_class]["size"][self.current_type] += 1
                else:
                    raise VarsTableException(f"Method '{self.current_method}' already exists as another attribute")

        else:
            raise VarsTableException(
                f"Function '{self.current_function}' has already been declared!"
            )

    def add_method_parameters(self, param_name :str):
        """
        Agregar los parametros de un método a la tabla de variables y tabla de parámetros
        """

        if param_name not in self.vars_table[self.current_class]["methods"][self.current_method]["vars"]:
            
            # Tabla de variables
            self.vars_table[self.current_class]["methods"][self.current_method]["vars"][param_name] = {
                "type": self.current_type,
                "memory_position" : memory.malloc(1, "local", self.current_type)
            }

            # Sumar el número de variables usadas
            self.vars_table[self.current_class]["size"][self.current_type] += 1

            # Tabla de parámetros
            self.method_signature.append(self.current_type)
            self.vars_table[self.current_class]["methods"][self.current_method]["PARAMETER_TABLE"] = self.method_signature

        else:
            raise VarsTableException(
                f"Parameter '{param_name}' has already been declared as another parameter or attribute"
            )

class VarsTableException(Exception):
    """Clase personalizada para los tipos de errores en la tabla de variables"""

    pass
