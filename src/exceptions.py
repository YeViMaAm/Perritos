class UsuarioNoExiste (Exception):
    """Se lanza cuando el usuario ingresado no esta registrado"""
    pass

class ContrasenaIncorrecta (Exception):
    """Se lanza cuando la contraseña es incorrecta"""
    pass

class UsuarioVacio(Exception):
    """Se lanza cuando el usuario ingresado esta vacio"""
    pass

class ContrasenaVacia (Exception):
    """Se lanza cuando la contraseña esta vacia"""
    pass

class UsuarioEspacios (Exception):
    """Se lanza cuando el usuario ingresado solo contine espacios"""
    pass

class ContrasenaEspacios (Exception):
    """Se lanza cuando la contraseña ingresada solo contiene espacios"""
    pass



