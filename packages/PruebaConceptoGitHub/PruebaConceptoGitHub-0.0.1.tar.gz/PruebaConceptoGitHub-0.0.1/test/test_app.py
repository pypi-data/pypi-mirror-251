import unittest
import sys,os
sys.path.append(os.getcwd())
from funciones.app import OperacionesNumeros

class test_clase(unittest.TestCase):
    
    def test_suma(self):
        valor_a=2
        valor_b=2
        ope=OperacionesNumeros(a=valor_a,b=valor_b)
        resultado_suma=ope.Suma()
        self.assertEqual(resultado_suma,valor_a+valor_b)
        
        
    def test_multiplicacion(self):
        valor_a=2
        valor_b=2
        ope=OperacionesNumeros(a=valor_a,b=valor_b)
        resultado_multiplicacion=ope.multiplicacion()
        self.assertEqual(resultado_multiplicacion,valor_a*valor_b)
        
    def test_resta(self):
        valor_a=2
        valor_b=2
        ope=OperacionesNumeros(a=valor_a,b=valor_b)
        resultado_resta=ope.resta()
        self.assertEqual(resultado_resta,valor_a-valor_b)
        
    def test_division(self):
        valor_a=2
        valor_b_no_cero=2
        valor_b_cero=0
        ope_no_cero=OperacionesNumeros(a=valor_a,b=valor_b_no_cero)
        resultado_division_no_cero=ope_no_cero.division()
        self.assertEqual(resultado_division_no_cero,valor_a/valor_b_no_cero)
        self.assertRaises(ZeroDivisionError,OperacionesNumeros(a=valor_a,b=valor_b_cero).division)
        
    def test_potenciacion(self):
        valor_a=2
        valor_b=2
        ope=OperacionesNumeros(a=valor_a, b=valor_b)
        resultado_potenciacion=ope.potenciacion()
        self.assertEqual(resultado_potenciacion,valor_a**valor_b)

    def test_radicacion(self):
        valor_a=2
        valor_b_no_cero=2
        valor_b_cero=0
        ope_no_cero=OperacionesNumeros(a=valor_a,b=valor_b_no_cero)
        resultado_radicacion_no_cero=ope_no_cero.radicacion()
        self.assertEqual(resultado_radicacion_no_cero,valor_a**(1/valor_b_no_cero))
        self.assertRaises(ZeroDivisionError,OperacionesNumeros(a=valor_a,b=valor_b_cero).radicacion)
