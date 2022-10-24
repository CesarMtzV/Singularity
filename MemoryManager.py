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

    def malloc(self, size :int, scope: str, type :str) -> int:
        """
        Retorna un entero que representa la memoria donde esta guardada la variable
        """
    
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
            elif type == "temp_int":
                if self.local_temp_int < 11000:
                    assigned_address = self.local_temp_int
                    self.local_temp_int += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many LOCAL TEMP INT variables")
            
            # FLOAT GLOBAL VARIABLES
            elif type == "float":
                if self.local_float < 12000:
                    assigned_address = self.local_float
                    self.local_float += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many LOCAL FLOAT variables")
            elif type == "temp_float":
                if self.local_temp_float < 13000:
                    assigned_address = self.local_temp_float
                    self.local_temp_float += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many LOCAL TEMP FLOAT variables")
            
            # BOOL GLOBAL VARIABLES
            elif type == "bool":
                if self.local_bool < 14000:
                    assigned_address = self.local_bool
                    self.local_bool += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many LOCAL BOOL variables")
            elif type == "temp_bool":
                if self.local_temp_bool < 15000:
                    assigned_address = self.local_temp_bool
                    self.local_temp_bool += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many LOCAL TEMP BOOL variables")
            
            # STRING GLOBAL VARIABLES
            elif type == "string":
                if self.local_string < 16000:
                    assigned_address = self.local_string
                    self.local_string += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many LOCAL STRING variables")
            elif type == "temp_string":
                if self.local_temp_string < 17000:
                    assigned_address = self.local_temp_string
                    self.local_temp_string += size
                    return assigned_address
                else:
                    raise MemoryManagerException("Too many LOCAL TEMP STRING variables")
            else:
                raise MemoryManagerException(f"Undefined type: {type}")
         
        elif scope == "constant":
            # TODO: Revisar si tambien hay que agregar variables temporales para constantes
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




class MemoryManagerException(Exception):
    """Clase personalizada para los tipos de errores en el Memory Manager"""

    pass
