# Clase que contiene la estructura de error por defecto
class ApiError(Exception):
    code = 500
    description = "Error interno, por favor revise el log"

# Clase que contiene la estructura de un error de tipo Bad Request
class CallExternalServiceError(ApiError):
    code = 500
    description = "Error al consumir servicio externo, por favor revise los logs."  

# Clase que contiene la estructura de un error de tipo Bad Request
class BadRequest(ApiError):
    code = 400
    description = "Párametros de entrada invalidos, por favor revise los logs."

# Clase que contiene la estructura de un error de tipo Unauthorized
class Unauthorized(ApiError):
    code = 401
    description = "El token proporcionado no es valido o esta vencido, por favor valide e intente nuevamente."

# Clase que contiene la estructura de un error de tipo TokenNotFound
class TokenNotFound(ApiError):
    code = 401
    description = "El token es obligatorio, por favor valide e intente nuevamente."

# Clase que contiene la estructura de un error de tipo Forbidden    
class Forbidden(ApiError):
    code = 403
    description = "No esta autorizado para realizar esta operación, por favor valide con el administrador del sistema."      

# Clase que contiene la estructura de un error cuando la consulta no retorna registros
class NoRecordsFound(ApiError):
    code = 404
    description = "No se encontro información con los parámetros ingresados, por favor valide e intente nuevamente."  

# Clase que contiene la estructura de un error de tipo Bad Dates
class BadDates(ApiError):
    code = 400
    description = "Las fechas ingresadas son invalidas, el formato correto es 'AAAA-MM-DD'."

# Clase que contiene la estructura de un error de tipo Bad Time
class BadTime(ApiError):
    code = 400
    description = "el tiempo ingresado es invalido, el formato correto es 'HH:MM:SS'."

# Clase que contiene la estructura de un error cuando el token esta expirado
class ExpiredToken(ApiError):
    code = 401
    description = "El token ha expirado, por favor vuelva a iniciar sesión." 

# Clase que contiene la estructura de un error de tipo Bad Request
class InvalidToken(ApiError):
    code = 400
    description = "Token Invalido"