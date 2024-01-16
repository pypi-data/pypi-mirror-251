import logging


class PauliHamiltonian:
    """
    direct for isQ 
    """    

    def __init__(self, nq):
        self._nq = nq
        self._xi = []
        self._P = []
        self._dH = 0  # constant energy

    def copy(self):
        new = PauliHamiltonian(self._nq) 
        new.xi = list(self._xi)
        new.P = list(self._P) 
        new.dH = self._dH
        return new 

    def setOneTerm(self, xi, p):
        self._xi.append(xi)
        self._P.append(p)
        return self

    def setOneTerm_byXYZ(self, xi, X=[], Y=[], Z=[]):
        # X = [] contains all site which are acted by X ,
        p = [0] * self._nq
        for i in range(self._nq):
            if i in X:
                p[i] = 1
            elif i in Y:
                p[i] = 2
            elif i in Z:
                p[i] = 3
        self._xi.append(xi)
        self._P.append(p)

    def add_dH(self, dH):
        self._dH += dH
        return self

    def getQn(self):
        """deprecated method, use getNq instead
        """        
        logging.warning("deprecated method, use getNq instead")
        return self._nq
    
    def getNq(self):
        return self._nq 

    def get_factor(self):
        return self._xi

    def get_pauliOperators(self):
        return self._P

    def simplify(self):
        table = {}
        for i in range(len(self._P)):
            key = str(self._P[i])
            if key not in table:
                table[key] = {
                    "xi": self._xi[i],
                    "op": list(self._P[i]),
                }
            else:
                table[key]["xi"] += self._xi[i]
        self._xi, self._P = [], []
        for k in table:
            xi = table[k]["xi"]
            if xi != 0:
                self._P.append(table[k]["op"])
                self._xi.append(table[k]["xi"])
        return self 

    def __hash__(self) -> int:
        return hash(str(hash(tuple(self._xi))) + str(hash(str(self._P))) + str(id(self)))
    
    def __len__(self):
        return len(self._P)
    
    def getdH(self):
        return self._dH
    
    def __add__(self,other):
        new = self.copy()
        if type(other) in [self.__class__]:
            for j in range(len(other.xi)):
                new.xi.append( other.xi[j] )
                new.P.append( other.P[j] )
            new.dH += other.dH 
        else:
            try:
                new.dH += float(other)
            except:
                raise Exception(f"unsupported adding with {type(other)}")
        return new 
    
    def __mul__(self,other):
        try:
            f = float(other)
            new = self.copy()
            new.xi = [ x*f for x in new.xi]
            new.dH *= f 
            return new 
        except:
            raise Exception(f"unsupported multiplexing with {type(other)}")
        
    def __repr__(self):
        def print_p(n):
            return ['I','X','Y','Z'][n]
        def print_P(P):
            return "".join([ print_p(i) for i in P])
        def print_one_line(i):
            return f"             {print_P(self._P[i])}: {self._xi[i]}"
        lines = "\n".join([ print_one_line(i)  for i in range(len(self._xi)) ])
        return f'''
        Pauli operators:
{lines}
        '''
