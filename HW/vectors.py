class MyVector:
    def __init__(self, pos):
        self.pos = pos
    
    def get_vector(self):
        return self.pos
    
    def __mul__(self, other):
        if ((len(self.pos)>len(other.pos)) or (len(self.pos)<len(other.pos))):
            return "Impossible to dot product, two different dimensions given"
        sum = 0
        for i in range(0, len(self.pos)):
            sum += (self.pos[i] * other.pos[i])
        return sum
    
    def __add__(self, other):
        addition = []
        for i in range(0, len(self.pos)):
            addition.append(self.pos[i] + other.pos[i])
        return MyVector(addition)
    
    def norm(self):
        normval = 0.0
        for i in range(0, len(self.pos)):
            normval += self.pos[i]**2
        normval = normval ** 0.5
        return normval

if __name__ == "__main__":
    a = MyVector([2, 5, 2])
    b = MyVector([2, 2, 1])

    print(a.get_vector())
    print(b.get_vector())
    print(a.norm())
    c = a + b
    print(c.get_vector())