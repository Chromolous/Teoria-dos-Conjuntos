from _collections_abc import Iterable

class Conjunto:
    nome:str
    __objects:list


class Conjunto:
    nome:str
    __objects:list
    
    def __init__(cls, iterable: Iterable, nome:str = "CONJUNTO"):
        cls.nome = nome.upper()
        objs = []
        for val in iterable:
            if val in objs:
                continue
            
            objs.append(val)
        
        cls.__objects = list(iterable)


    def uniao(self, s:Conjunto):
        output = self.__objects.copy()
        for i in s:
            if not i in self:
                output.append(i)
        return Conjunto(output, f"{self.nome} ∪ {s.nome}")
    
    def __add__(self, s:Conjunto):
        return Conjunto(self.uniao(s), f"{self.nome} ∪ {s.nome}")
    
    
    def interseccao(self, s:Conjunto):
        output = []
        for i in s:
            if i in self:
                output.append(i)

        return Conjunto(output, f"{self.nome} ∩ {s.nome}")
    
    def __xor__(self, s:Conjunto):
        return Conjunto(self.interseccao(s), f"{self.nome} ∩ {s.nome}")
    
    
    def diferenca(self, s:Conjunto):
        output = self.__objects.copy()
        for i in s:
            if i in self:
                output.remove(i)
        return Conjunto(output, f"{self.nome} - {s.nome}")
    
    def __sub__(self, s:Conjunto):
        return Conjunto(self.diferenca(s), f"{self.nome} - {s.nome}")
    
    
    def check_igual(self, s:Conjunto):
        return self.__objects == s.__objects
    
    def __eq__(self, s:Conjunto):
        return self.check_igual(s)
    
    
    def check_subconjunto(self, s:Iterable):
        return all(elem in s for elem in self.__objects)
    
    def __lshift__(self, s:Iterable):
        return self.check_subconjunto(s)
    
    
    def check_superconjunto(self, s:Iterable):
        return all(elem in self.__objects for elem in s)
    
    def __rshift__(self, s:Iterable):
        return self.check_superconjunto(s)
    
    
    def check_diferente(self, s:Conjunto):
        return self.__objects != s.__objects
    
    def __ne__(self, s:Conjunto):
        return self.check_diferente(s)
    
    
    def produto(self, s):
        ite = [self.__objects]
        try:
            ite.append(s.__objects)
        except:
            ite.extend([c.__objects for c in s])
        
        resultados = Conjunto.n_arias(ite)

        try:
            return Conjunto(resultados, f" × ".join([self.nome]+[s.nome]))
        except:
            return Conjunto(resultados, f" × ".join([self.nome]+[c.nome for c in s]))
    
    def __mul__(self, s:Conjunto):
        return self.produto(s)
    
    
    def __str__(self):
        val = ", ".join([str(i) for i in self])
        
        return self.nome + " = {" + val + "}"
    
    def __repr__(self):
        val = ", ".join([str(i) for i in self])
        
        return self.nome + " = {" + val + "}"
    
    def __iter__(self):
        return iter(self.__objects)
    
    @staticmethod
    def conversor(text:str):
        temp = text.replace(" ","")
        temp = temp.split("=")

        nome = temp[0]
        valores = []
        
        inicio = temp[1].find("{")
        fim = temp[1].find("}")

        tempValores = temp[1][(inicio+1):fim].split(",")
        tempValoresCopy = tempValores.copy()
        
        for val in tempValoresCopy:
            if val in valores:
                continue
            
            valores.append(val)
        
        return Conjunto(valores, nome)
    
    @staticmethod
    def n_arias(s, atual = []):
        if not s:
            return [atual]
        
        resultados = []
        
        for item in s[0]:
            resultados.extend(Conjunto.n_arias(s[1:], atual+[item,]))
            
        return resultados
    
   
if __name__ == "__main__": 
    a = Conjunto([1,2,3,4,5], "A")
    b = Conjunto([4,5,6,7,8], "B")
    c = Conjunto([1,2,3,4,5], "C")
    d = Conjunto([4,5], "D")
    e = Conjunto([1,2,3], "E")
    f = Conjunto([(5,1),(4,1)], "F")
    
    # União
    print(a+b)
    print(a.uniao(b))
    
    # Intersecção
    print(a^b)
    print(a.interseccao(b))
    
    # Diferença
    print(a-b)
    print(a.diferenca(b))
    
    # Igualdade
    print(a == b)
    print(a.check_igual(b))
    
    # Subconjunto
    print(a << b)
    print(a.check_subconjunto(b))
    
    # Desigualdade
    print(a != b)
    print(a.check_diferente(b))
    
    # Produto cartesiano
    print(a*b)
    print(a.produto(b))
    
    # Relação n-ária
    A = Conjunto([1,2], "A")
    B = Conjunto([2], "B")
    C = Conjunto([2,3], "C")

    print(A*B*C) # Aqui ele faz a binária de A x B e depois a binária de (A x B) x C
    print(A.produto([B,C])) # Para ter uma relação terciária é necessário chamar a função 'produto' e passar os conjuntos em uma lista
    print(A.produto(B).produto(C)) # Aqui é equivalente a fazer 'A*B*C'