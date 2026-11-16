import unittest

from cliente import Cliente
from excepciones import ClienteDuplicadoError, ReservaError
from gestor import GestorSoftwareFJ


class TestGestor(unittest.TestCase):
    def setUp(self):
        self.g = GestorSoftwareFJ()
        self.ana = Cliente("Ana Pérez", "1002345678",
                           "ana@correo.com", "3001234567")

    def test_registrar_y_buscar(self):
        self.g.registrar(self.ana)
        self.assertIs(self.g.buscar_cliente("1002345678"), self.ana)
        self.assertIsNone(self.g.buscar_cliente("99999999"))

    def test_cliente_duplicado(self):
        self.g.registrar(self.ana)
        otra = Cliente("Ana P", "1002345678", "otra@correo.com", "3001234567")
        with self.assertRaises(ClienteDuplicadoError):
            self.g.registrar(otra)

    def test_objeto_no_registrable(self):
        with self.assertRaises(ReservaError):
            self.g.registrar("no soy una entidad")

    def test_intentar_no_detiene_el_sistema(self):
        self.assertIsNone(self.g.intentar("falla", lambda: Cliente("Solo nombre")))
        self.assertEqual(self.g.intentar("ok", lambda: 5), 5)


if __name__ == "__main__":
    unittest.main()