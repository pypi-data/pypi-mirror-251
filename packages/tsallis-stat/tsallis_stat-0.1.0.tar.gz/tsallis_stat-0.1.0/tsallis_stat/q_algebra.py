from typing import SupportsIndex
import numpy as np


QValueType = int | float | np.ndarray

class QAlgebra:
    def __init__(self, value: int | float | np.ndarray, q: float) -> None:
        if isinstance(value, QAlgebra):
            raise NotImplementedError
        else:
            self._value = np.array(value)
        self._q = q

    @property
    def value(self) -> np.ndarray:
        return self._value
    
    @property
    def q(self) -> float:
        return self._q
    
    @property
    def T(self) -> "QAlgebra":
        return QAlgebra(self._value.T, self._q)
    
    def __getitem__(self, key: SupportsIndex) -> "QAlgebra":
        new_value = self._value[key]
        return QAlgebra(new_value, self._q)
    
    def __setitem__(self, key: SupportsIndex, value: QValueType) -> None:
        self._value[key] = np.array(value)

    def __len__(self) -> int:
        return len(self._value)

    def __add__(self, other: "QAlgebra") -> "QAlgebra":
        assert self._q == other._q, "Parameter q must be the same"
        new_value = self._value + other._value
        return QAlgebra(new_value, self._q)
    
    def __sub__(self, other: "QAlgebra") -> "QAlgebra":
        assert self._q == other._q, "Parameter q must be the same"
        new_value = self._value - other._value
        return QAlgebra(new_value, self._q)
    
    def __mul__(self, other: "QAlgebra") -> "QAlgebra":
        assert self._q == other._q, "Parameter q must be the same"
        x = self._value
        y = other._value
        q = self._q
        new_value = np.maximum(0, x ** (1 - q) + y ** (1 - q) - 1) ** (1 / (1 - q))
        return QAlgebra(new_value, q)
    
    def __truediv__(self, other: "QAlgebra") -> "QAlgebra":
        assert self._q == other._q, "Parameter q must be the same"
        x = self._value
        y = other._value
        q = self._q
        new_value = np.maximum(0, x ** (1 - q) - y ** (1 - q) + 1) ** (1 / (1 - q))
        assert new_value.shape == x.shape
        return QAlgebra(new_value, q)

    def __matmul__(self, other: "QAlgebra") -> "QAlgebra":
        assert self._q == other._q, "Parameter q must be the same"
        x = self._value
        y = other._value
        q = self._q
        if x.ndim == 1 and y.ndim == 1:
            new_value = np.sum((self * other).value)
        elif x.ndim == 2 and y.ndim == 1:
            assert x.shape[1] == y.shape[0]
            new_value: np.ndarray = np.sum((self * other).value, axis=1)
            assert new_value.shape == (x.shape[0],)
        elif x.ndim == 1 and y.ndim == 2:
            assert x.shape[0] == y.shape[0]
            new_value = np.sum((other.T * self).value, axis=1)
            assert new_value.shape == (y.shape[0],)
        elif x.ndim == 2 and y.ndim == 2:
            assert x.shape[1] == y.shape[0]
            new_value = np.array([np.sum((self * other[:, i]).value, axis=1) for i in range(y.shape[1])])
        else:
            raise NotImplementedError
        return QAlgebra(new_value, q)

    def __eq__(self, other: "QAlgebra") -> bool:
        assert self._q == other._q, "Parameter q must be the same"
        ret = np.allclose(self._value, other._value)
        return ret
    
    def __ne__(self, other: "QAlgebra") -> bool:
        assert self._q == other._q, "Parameter q must be the same"
        ret = not np.allclose(self._value, other._value)
        return ret
    
    def __lt__(self, other: "QAlgebra") -> bool:
        assert self._q == other._q, "Parameter q must be the same"
        ret = np.all(self._value < other._value)
        return ret
    
    def __le__(self, other: "QAlgebra") -> bool:
        assert self._q == other._q, "Parameter q must be the same"
        ret = np.all(self._value <= other._value)
        return ret
    
    def __gt__(self, other: "QAlgebra") -> bool:
        assert self._q == other._q, "Parameter q must be the same"
        ret = np.all(self._value > other._value)
        return ret
    
    def __ge__(self, other: "QAlgebra") -> bool:
        assert self._q == other._q, "Parameter q must be the same"
        ret = np.all(self._value >= other._value)
        return ret
    
    def __str__(self) -> str:
        return f"QAlgebra({self._value}, {self._q})"
    