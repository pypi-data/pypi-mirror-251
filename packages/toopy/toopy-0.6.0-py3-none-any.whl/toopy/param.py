import numpy as np

class Param:
    def __init__(self, value, name="", min=None, max=None, step=None, 
                 prior=None):
            self.name = name
            self._type = type(value)
            self._type.__init__(value)
            self.min = self._type(self.minfunc(min))
            self.max = self._type(self.maxfunc(max))
            self.step = self._type(10**(self.scale(self)-1) if step is None else step)
            self.prior = prior

    def minfunc(self, minimum):
        if minimum is not None:
            return minimum
        
        if self.value <= 1:
            minimum = self.value / 10
        else:
            minimum = self.value / 4
    
        return np.round(minimum, -self.scale(minimum))
        
    def maxfunc(self, maximum):
        if maximum is not None:
            return maximum
        
        if self.value <= 1:
            maximum = self.value * 10
        else:
            maximum = self.value * 2
            
        return np.round(maximum, -self.scale(maximum))
       
    @staticmethod
    def scale(value):
        return int(np.floor(np.log10(np.abs(value))))

    def ParamClass(self, value):
        kwargs = self.__dict__.copy()
        _type = kwargs.pop("_type")
        ParamClass = type(self)
        return ParamClass(_type(value), **kwargs)

    def __mul__(self, other):
        return self.ParamClass(self._type(self) * other)

    def __div__(self, other):
        return self.ParamClass(self._type(self) / other)

    def __truediv__(self, other):
        return self.ParamClass(self._type(self) / other)

    def __add__(self, other):
        return self.ParamClass(self._type(self) + other)

    def __sub__(self, other):
        return self.ParamClass(self._type(self) - other)
    
    def __pow__(self, other):
        return self.ParamClass(self._type(self) ** other)

    def __repr__(self):
        pcls = str(self._type).split("'")[1]
        return f"<Param[{pcls}] '{self.name}': {self._type(self)} [{self.min}-{self.max}] step={self.step}>"

    @property
    def value(self):
        return self._type(self)



class FloatParam(Param, float):
    def __new__(self, value, name="", min=None, max=None, step=None, prior=None) -> float:
        return float.__new__(self, value)

class IntParam(Param, int):
    def __new__(self, value, name="", min=None, max=None, step=None, prior=None) -> int:
        return int.__new__(self, value)

class ArrayParam(Param):
    def __init__(self, value, name="", min=None, max=None, step=None, 
                 prior=None):
        self.name = name
        self._value = value
        self.min = self.minfunc(min)
        self.max = self.maxfunc(max)
        self.step = 10.0**(self.scale(value)-1) if step is None else step
        self.prior = prior

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value

    
    def minfunc(self, minimum):
        if minimum is not None:
            return minimum
        
        minimum = np.where(self.value <= 1, self.value / 10, self.value / 4)
        return np.array([np.round(m, -self.scale(m)) for m in minimum])
        
    def maxfunc(self, maximum):
        if maximum is not None:
            return maximum
        
        maximum = np.where(self.value <= 1, self.value * 10, self.value * 2)
        return np.array([np.round(m, -self.scale(m)) for m in maximum])
    
    @staticmethod
    def scale(value):
        return np.floor(np.log10(np.abs(value))).astype(int)
    