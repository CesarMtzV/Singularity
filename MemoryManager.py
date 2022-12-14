class MemoryManager:
    """
    Esta clase contiene todos los limites de memoria para los tipos de variables.
    Tambien se encarga de guardar las variables y retornar al Generador de Codigo Intermedio
    la direccion de memoria correspondiente.
    """

    def __init__(self) -> None:
        
        # Memoria global
        self.global_int         = 1000
        self.global_temp_int    = 2000
        
        self.global_float       = 3000
        self.global_temp_float  = 4000
        
        self.global_bool        = 5000
        self.global_temp_bool   = 6000

        self.global_string      = 7000
        self.global_temp_string = 8000


        # Memoria local
        self.local_int          = 9000
        self.local_temp_int     = 10000
        
        self.local_float        = 11000
        self.local_temp_float   = 12000
        
        self.local_bool         = 13000
        self.local_temp_bool    = 14000

        self.local_string       = 15000
        self.local_temp_string  = 16000


        # Memoria constante
        self.const_int         = 17000
        self.const_float        = 18000
        self.const_bool         = 19000
        self.const_string       = 20000
        
        # Memoria pointer
        self.pointer            = 21000
        
        self.global_ints = []
        self.global_temp_ints = []
        
        self.global_floats = [] 
        self.global_temp_floats = []
        
        self.global_bools = []
        self.global_temp_bools = []
        
        self.global_strings = []
        self.global_temp_strings = []
        
        self.local_ints = []
        self.local_temp_ints = []
        
        self.local_floats = []
        self.local_temp_floats = []
        
        self.local_bools = []
        self.local_temp_bools = []
        
        self.local_strings = []
        self.local_temp_strings = []
        
        self.const_ints = []
        self.const_floats = []
        self.const_bools = []
        self.const_strings = []
        
        self.pointers = []
        
        self.local_ints_stack = []
        self.local_floats_stack = []
        self.local_bools_stack = []
        self.local_strings_stack = []

        self.temp_ints_stack = []
        self.temp_floats_stack = []
        self.temp_bools_stack = []
        self.temp_strings_stack = []
        self.temp_pointers_stack = [] 
        
    
    def resetLocalMemory(self):
        self.local_ints_stack.append(self.local_ints)
        self.local_ints = []

        self.local_floats_stack.append(self.local_floats)
        self.local_floats = []
    
        self.local_bools_stack.append(self.local_bools)
        self.local_bools = []
    
        self.local_strings_stack.append(self.local_strings)
        self.local_strings = []

    
    def resetTempMemory(self):
        self.temp_ints_stack.append(self.local_temp_ints)
        self.local_temp_ints = []
        
        self.temp_floats_stack.append(self.local_temp_floats)
        self.local_temp_floats = []
        
        self.temp_bools_stack.append(self.local_temp_bools)
        self.local_temp_bools = []
    
        self.temp_strings_stack.append(self.local_temp_strings)
        self.local_temp_strings = []
        
        self.temp_pointers_stack.append(self.pointers)
        self.pointers = []
        
    def malloc(self, size :int, scope: str, type :str) -> int:
        """
        Retorna un entero que representa la memoria donde esta guardada la variable.
        Scopes disponibles:
        - global
        - local
        - local_temp
        - constant
        """

        # TODO: Checar si tambien cambiar temporales globales
        if scope == "global":

            # INT GLOBAL VARIABLES
            if type == "int":
                if self.global_int < 2000:
                    assigned_address = self.global_int
                    self.global_int += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many GLOBAL INT variables")
            elif type == "temp_int":
                if self.global_temp_int < 3000:
                    assigned_address = self.global_temp_int
                    self.global_temp_int += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many GLOBAL TEMP INT variables")
            
            # FLOAT GLOBAL VARIABLES
            elif type == "float":
                if self.global_float < 4000:
                    assigned_address = self.global_float
                    self.global_float += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many GLOBAL FLOAT variables")
            elif type == "temp_float":
                if self.global_temp_float < 5000:
                    assigned_address = self.global_temp_float
                    self.global_temp_float += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many GLOBAL TEMP FLOAT variables")
            
            # BOOL GLOBAL VARIABLES
            elif type == "bool":
                if self.global_bool < 6000:
                    assigned_address = self.global_bool
                    self.global_bool += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many GLOBAL BOOL variables")
            elif type == "temp_bool":
                if self.global_temp_bool < 7000:
                    assigned_address = self.global_temp_bool
                    self.global_temp_bool += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many GLOBAL TEMP BOOL variables")
            
            # STRING GLOBAL VARIABLES
            elif type == "string":
                if self.global_string < 8000:
                    assigned_address = self.global_string
                    self.global_string += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many GLOBAL STRING variables")
            elif type == "temp_string":
                if self.global_temp_string < 9000:
                    assigned_address = self.global_temp_string
                    self.global_temp_string += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many GLOBAL TEMP STRING variables")
            else:
                raise MemoryManagerException(f"Undefined type: {type}")

        elif scope == "local":

            # INT LOCAL VARIABLES
            if type == "int":
                if self.local_int < 10000:
                    assigned_address = self.local_int
                    self.local_int += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many LOCAL INT variables")
            
            # FLOAT LOCAL VARIABLES
            elif type == "float":
                if self.local_float < 12000:
                    assigned_address = self.local_float
                    self.local_float += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many LOCAL FLOAT variables")
            
            # BOOL LOCAL VARIABLES
            elif type == "bool":
                if self.local_bool < 14000:
                    assigned_address = self.local_bool
                    self.local_bool += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many LOCAL BOOL variables")
            
            # STRING LOCAL VARIABLES
            elif type == "string":
                if self.local_string < 16000:
                    assigned_address = self.local_string
                    self.local_string += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many LOCAL STRING variables")
            
            else:
                raise MemoryManagerException(f"Undefined type: {type}")
         
        elif scope == "local_temp":
            if type == "int":
                if self.local_temp_int < 11000:
                    assigned_address = self.local_temp_int
                    self.local_temp_int += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many LOCAL TEMP INT variables")
            elif type == "float":
                if self.local_temp_float < 13000:
                    assigned_address = self.local_temp_float
                    self.local_temp_float += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many LOCAL TEMP FLOAT variables")
            elif type == "bool":
                if self.local_temp_bool < 15000:
                    assigned_address = self.local_temp_bool
                    self.local_temp_bool += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many LOCAL TEMP BOOL variables")
            elif type == "string":
                if self.local_temp_string < 17000:
                    assigned_address = self.local_temp_string
                    self.local_temp_string += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many LOCAL TEMP STRING variables")
            elif type == "pointer":
                if self.pointer < 22000:
                    assigned_address = self.pointer
                    self.pointer += size
                    return assigned_address

        elif scope == "constant":
            if type == "int":
                if self.const_int < 18000:
                    assigned_address = self.const_int
                    self.const_int += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many CONST INT variables")
            elif type == "float":
                if self.const_float < 19000:
                    assigned_address = self.const_float
                    self.const_float += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many CONST FLOAT variables")
            elif type == "bool":
                if self.const_bool < 20000:
                    assigned_address = self.const_bool
                    self.const_bool += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many CONST BOOL variables")
            elif type == "string":
                if self.const_string < 21000:
                    assigned_address = self.const_string
                    self.const_string += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many CONST STRING variables")
            else:
                raise MemoryManagerException(f"Undefined type: {type}")
        
        else:
            raise MemoryManagerException(f"Undefined scope: {scope}")

    def dealloc(self):
        # Memoria local
        self.local_int          = 9000
        self.local_temp_int     = 10000
        
        self.local_float        = 11000
        self.local_temp_float   = 12000
        
        self.local_bool         = 13000
        self.local_temp_bool    = 14000

        self.local_string       = 15000
        self.local_temp_string  = 16000

        self.pointer            = 21000


class MemoryManagerException(Exception):
    """Clase personalizada para los tipos de errores en el Memory Manager"""

    pass
