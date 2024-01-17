import math
import typing

__all__ = ['Vector']




def _div(a, b) -> int:
    ans, remainder = divmod(a, b)
    if type(ans) is not int:
        raise TypeError(ans)
    if remainder:
        raise ValueError(remainder)
    return ans




class _Description(typing.NamedTuple):
    x: int = 0
    y: int = 0
    z: int = 0




class _Digest(typing.NamedTuple):
    x: float = 0.0
    y: float = 0.0
    def radius(self) -> float:
        return sum((a ** 2) for a in self) ** .5
    def angle(self) -> float:
        try:
            ratio = self.x / self.radius()
        except ZeroDivisionError:
            return float('nan')
        ans = math.acos(ratio)
        if self.y < 0:
            ans *= -1
        return ans

    


class Vector:


    #   dunder

    def __abs__(self) -> typing.Union[int, float]:
        desc = self.description()
        values = list(set(desc) - {0})
        if len(values) == 1:
            return abs(values.pop())
        return self.digest().radius()

    def __add__(self, other) -> typing.Self:
        cls = type(self)
        if type(other) is not cls:
            raise TypeError
        return cls(0, self._y + other._y, self._z + other._z)

    def __bool__(self) -> bool:
        return any(self.description())

    def __eq__(self, other) -> bool:
        cls = type(self)
        if type(other) is not cls:
            return False
        return self.description() == other.description()

    def __float__(self) -> float:
        return float('nan') if self else .0

    def __hash__(self) -> int:
        return self.description().__hash__()

    def __init__(self, *args, **kwargs) -> None:
        desc = _Description(*args, **kwargs)
        for a in desc:
            if type(a) is not int:
                raise TypeError(a)
        self._y = desc.y - desc.x
        self._z = desc.z - desc.x

    def __int__(self) -> int:
        return int(float(self))
    
    def __mul__(self, other) -> typing.Union[float, typing.Self]:
        cls = type(self)
        if type(other) is not cls:
            return cls(
                0, 
                self._y * other, 
                self._z * other,
            )
        return (
            (self._y * other._y)
            + (self._z * other._z)
            + (-.5 * self._y * other._z)
            + (-.5 * self._z * other._y)
        )

    def __neg__(self) -> typing.Self:
        cls = type(self)
        return cls(0, -self._y, -self._z)

    def __pow__(self, other:int) -> typing.Union[float, typing.Self]:
        if type(other) is not int:
            raise TypeError(other)
        if other < 0:
            raise ValueError(other)
        ans = 1
        for i in range(other):
            ans *= self
        return ans

    def __rmul__(self, other) -> typing.Self:
        cls = type(self)
        return cls(
            0, 
            other * self._y, 
            other * self._z,
        )

    def __sub__(self, other) -> typing.Self:
        return self + (-other)

    def __truediv__(self, other) -> typing.Self:
        cls = type(self)
        y = _div(self._y, other)
        z = _div(self._z, other)
        ans = cls(0, y, z)
        return ans


    #   public
    def description(self, tare='x') -> _Description:
        tare = {
            'x':0,
            'y':1,
            'z':2,
        }[tare]
        if tare == 0:
            return _Description(0, self._y, self._z)
        if tare == 1:
            return _Description(-self._y, 0, self._z - self._y)
        if tare == 2:
            return _Description(-self._z, self._y - self._z, 0)
        raise NotImplementedError
    
    def digest(self) -> _Digest:
        x = (3 ** .5) * .5 * self._y
        y = (-.5 * self._y) + self._z
        ans = _Digest(x, y)
        return ans
    
    def factorize(self) -> typing.Tuple[int, typing.Self]:
        scale = math.gcd(
            abs(self._y), 
            abs(self._z),
        )
        hint = self / scale
        return (scale, hint)
    
    def hflip(self) -> typing.Self:
        cls = type(self)
        ans = cls(self._y, 0, self._z)
        return ans
    
    @classmethod
    def linear_dependence(cls, *vectors) -> bool:
        errors = list()
        for v in vectors:
            if type(v) is not cls:
                errors.append(TypeError(v))
        if len(errors):
            raise ExceptionGroup("Non-Vectors given!", errors)
        if len(vectors) > 2:
            return True
        if len(vectors) < 2:
            return not all(vectors)
        v, w = vectors
        return (v._y * w._z) == (v._z * w._y)
    
    def rotate(self, amount:int) -> typing.Self:
        cls = type(self)
        if type(amount) is not int:
            raise TypeError(amount)
        vector = self
        if amount % 2:
            amount += 3
            vector = -vector
        amount %= 6
        if amount == 0:
            return cls(0, vector._y, vector._z)
        if amount == 2:
            return cls(vector._z, 0, vector._y)
        if amount == 4:
            return cls(vector._y, vector._z, 0)
        raise NotImplementedError

    def vflip(self) -> typing.Self:
        cls = type(self)
        ans = cls(-self._y, 0, -self._z)
        return ans


