from src.exceptions import (
    UsuarioVacio,
    ContrasenaVacia,
    UsuarioEspacios,
    ContrasenaEspacios
)

class Login:
    def __init__(self, usuario, contrasena):
        # Se valida que los campos no vengan mal (vacíos o espacios)
        self._validar_usuario(usuario)
        self._validar_contrasena(contrasena)
        self.usuario = usuario
        self.contrasena = contrasena

    def _validar_usuario(self, usuario):
        if not usuario:
            raise UsuarioVacio("El nombre de usuario es obligatorio")
        if usuario.strip() == "":
            raise UsuarioEspacios("El usuario no puede contener solo espacios")

    def _validar_contrasena(self, contrasena):
        if not contrasena:
            raise ContrasenaVacia("La contraseña es obligatoria")
        if contrasena.strip() == "":
            raise ContrasenaEspacios("La contraseña no puede contener solo espacios")

    def __str__(self):
        return f"Login(usuario='{self.usuario}')"