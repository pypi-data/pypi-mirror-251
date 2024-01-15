class OperacionesNumeros:

    def __init__(self,a:float,b:float):
        self.a=a
        self.b=b
    
    def Suma(self):
        return self.a+self.b
    
    def resta(self):
        return self.a-self.b
    
    def multiplicacion(self):
        return self.a*self.b

    def division(self):
        if self.b==0:
            raise ZeroDivisionError()
        return self.a/self.b
        
    def potenciacion(self):
        return self.a**self.b
    
    def radicacion(self):
        if self.b==0:
            raise ZeroDivisionError()
        return self.a**(1/self.b)