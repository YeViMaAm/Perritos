import pytest 
from src.login import login
from src.exceptions import  (UsuarioNoExiste, ContrasenaIncorrecta, UsuarioVacio, ContrasenaVacia, UsuarioEspacios, ContrasenaEspacios)


def test_login_correcto():
    usuario_login = login("candy", "candy159")
    assert usuario_login.usuario == "candy"
    assert usuario_login.contrasena == "candy159"

def test_usuario_vacio():
    with pytest.raises(UsuarioVacio):
        login("", "candy159")

def test_usuario_solo_espacios():
    with pytest.raises(UsuarioEspacios):
        login("   ", "candy159")

def test_contrasena_vacia():
    with pytest.raises(ContrasenaVacia):
        login("candy", "")

def test_contrasena_solo_espacios():
    with pytest.raises(ContrasenaEspacios):
        login("candy", "   ")

def test_usuario_no_existe():
    with pytest.raises(UsuarioNoExiste):
        login("Pedro", "candy159")

def test_contrasena_incorrecta():
    with pytest.raises(ContrasenaIncorrecta):
        login("candy", "123")