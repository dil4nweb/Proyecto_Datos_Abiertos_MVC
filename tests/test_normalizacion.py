import unittest
from models.datos_model import normalizar

class PruebaNormalizacion(unittest.TestCase):
    def test_mismo_json_mismo_id(self):
        a = {'idioma': 'Español', 'formato': 'PDF'}
        b = {'formato': 'PDF', 'idioma': 'Español'}
        self.assertEqual(normalizar(a)[0], normalizar(b)[0])

    def test_cambio_contenido_cambia_id(self):
        self.assertNotEqual(normalizar({'formato': 'PDF'})[0], normalizar({'formato': 'CSV'})[0])

if __name__ == '__main__':
    unittest.main()
