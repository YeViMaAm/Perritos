from src.exceptions import (
    UsuarioNoExiste,
    ContrasenaIncorrecta,
    UsuarioVacio,
    ContrasenaVacia,
    UsuarioEspacios,
    ContrasenaEspacios
)

class Login:

    def __init__(self, usuario, contrasena):
        self._validar_usuario(usuario)
        self._validar_contrasena(contrasena)
        self.contrasena = contrasena

    def _validar_usuario(self, usuario):
        if not usuario:
            raise UsuarioVacio("El usuario no puede estar vacio")

        if usuario.strip() == "":
            raise UsuarioEspacios("El usuario no puede contener solo espacios")

        if usuario != "candy":
            raise UsuarioNoExiste(f"El usuario no está registrado: {usuario}")

    def _validar_contrasena(self, contrasena):
        if not contrasena:
            raise ContrasenaVacia("La contraseña no puede estar vacía")

        if contrasena.strip() == "":
            raise ContrasenaEspacios("La contraseña no puede contener solo espacios")

        if contrasena != "candy159":
            raise ContrasenaIncorrecta(f"La contraseña es incorrecta: {contrasena}")

    def __str__(self):
        return f"Login(usuario='{self.usuario}')"