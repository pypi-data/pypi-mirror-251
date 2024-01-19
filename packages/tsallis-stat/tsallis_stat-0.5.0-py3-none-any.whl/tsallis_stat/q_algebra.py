from typing import SupportsIndex
import numpy as np


QValueType = int | float | np.ndarray


class QAlgebra:
    def __init__(self, q: float) -> None:
        self._q = q

    def set_q(self, q: float) -> None:
        self._q = q

    @property
    def q(self) -> float:
        return self._q

    def mul(self, x: QValueType, y: QValueType) -> QValueType:
        q = self._q
        if q == 1:
            return x * y
        return np.maximum(0, x ** (1 - q) + y ** (1 - q) - 1) ** (1 / (1 - q))

    def div(self, x: QValueType, y: QValueType) -> QValueType:
        q = self._q
        if q == 1:
            return x / y
        return np.maximum(0, x ** (1 - q) - y ** (1 - q) + 1) ** (1 / (1 - q))

    def matmul(self, x: QValueType, y: QValueType) -> QValueType:
        q = self._q
        if q == 1:
            return x @ y
        if x.ndim == 1 and y.ndim == 1:
            ret = np.sum(self.mul(x, y))
        elif x.ndim == 2 and y.ndim == 1:
            assert x.shape[1] == y.shape[0]
            ret: np.ndarray = np.sum(self.mul(x, y), axis=1)
            assert ret.shape == (x.shape[0],)
        elif x.ndim == 1 and y.ndim == 2:
            assert x.shape[0] == y.shape[0]
            ret: np.ndarray = np.sum(self.mul(y.T, x), axis=1)
            assert ret.shape == (y.shape[1],)
        elif x.ndim == 2 and y.ndim == 2:
            assert x.shape[1] == y.shape[0]
            ret = np.array(
                [np.sum(self.mul(x, y[:, i]), axis=1) for i in range(y.shape[1])]
            )
            assert ret.shape == (x.shape[0], y.shape[1])
        else:
            raise NotImplementedError
        return ret

    def pow(self, x: QValueType, n: int) -> QValueType:
        q = self._q
        assert n > 0, "n must be positive"
        if isinstance(x, np.ndarray):
            if q == 1:
                return np.linalg.matrix_power(x, n)
            assert (x.ndim == 2) & (x.shape[0] == x.shape[1])
            ret = x
            for _ in range(n - 1):
                ret = self.matmul(ret, x)
            assert ret.shape == x.shape
            return ret
        else:
            if q == 1:
                return x ** n
            ret = x
            for _ in range(n - 1):
                ret = self.mul(ret, x)
            return ret

    def exp(self, x: QValueType) -> QValueType:
        q = self._q
        if q == 1:
            return np.exp(x)
        ret = np.maximum(0, 1 + (1 - q) * x) ** (1 / (1 - q))
        return ret

    def log(self, x: QValueType) -> QValueType:
        q = self._q
        if q == 1:
            return np.log(x)
        ret = (x ** (1 - q) - 1) / (1 - q)
        return ret

    def tsallis_entropy(self, x: np.ndarray) -> float:
        q = self._q
        assert np.all(x >= 0), "Probabilities must be non-negative"
        assert np.isclose(np.sum(x), 1), "Probabilities must sum to one"
        if q == 1:
            return -np.sum(x * np.log(x))
        return (1 - np.sum(x**q)) / (1 - q)

    def q_entropy(self, x: np.ndarray) -> float:
        q = self._q
        assert np.all(x >= 0), "Probabilities must be non-negative"
        assert np.isclose(np.sum(x), 1), "Probabilities must sum to one"
        if q == 1:
            return -np.sum(x * np.log(x))
        return -np.sum(x * self.log(x) - x) / (2 - q)


# class QAlgebra:
#     def __init__(self, value: int | float | np.ndarray, q: float) -> None:
#         if isinstance(value, QAlgebra):
#             raise NotImplementedError
#         else:
#             self._value = np.array(value)
#         self._q = q

#     @property
#     def value(self) -> np.ndarray:
#         return self._value

#     @property
#     def q(self) -> float:
#         return self._q

#     @property
#     def T(self) -> "QAlgebra":
#         return QAlgebra(self._value.T, self._q)

#     def __getitem__(self, key: SupportsIndex) -> "QAlgebra":
#         new_value = self._value[key]
#         return QAlgebra(new_value, self._q)

#     def __setitem__(self, key: SupportsIndex, value: QValueType) -> None:
#         self._value[key] = np.array(value)

#     def __len__(self) -> int:
#         return len(self._value)

#     def __add__(self, other: "QAlgebra") -> "QAlgebra":
#         assert self._q == other._q, "Parameter q must be the same"
#         new_value = self._value + other._value
#         return QAlgebra(new_value, self._q)

#     def __sub__(self, other: "QAlgebra") -> "QAlgebra":
#         assert self._q == other._q, "Parameter q must be the same"
#         new_value = self._value - other._value
#         return QAlgebra(new_value, self._q)

#     def __mul__(self, other: "QAlgebra") -> "QAlgebra":
#         assert self._q == other._q, "Parameter q must be the same"
#         x = self._value
#         y = other._value
#         q = self._q
#         new_value = np.maximum(0, x ** (1 - q) + y ** (1 - q) - 1) ** (1 / (1 - q))
#         return QAlgebra(new_value, q)

#     def __truediv__(self, other: "QAlgebra") -> "QAlgebra":
#         assert self._q == other._q, "Parameter q must be the same"
#         x = self._value
#         y = other._value
#         q = self._q
#         new_value = np.maximum(0, x ** (1 - q) - y ** (1 - q) + 1) ** (1 / (1 - q))
#         assert new_value.shape == x.shape
#         return QAlgebra(new_value, q)

#     def __matmul__(self, other: "QAlgebra") -> "QAlgebra":
#         assert self._q == other._q, "Parameter q must be the same"
#         x = self._value
#         y = other._value
#         q = self._q
#         if x.ndim == 1 and y.ndim == 1:
#             new_value = np.sum((self * other).value)
#         elif x.ndim == 2 and y.ndim == 1:
#             assert x.shape[1] == y.shape[0]
#             new_value: np.ndarray = np.sum((self * other).value, axis=1)
#             assert new_value.shape == (x.shape[0],)
#         elif x.ndim == 1 and y.ndim == 2:
#             assert x.shape[0] == y.shape[0]
#             new_value = np.sum((other.T * self).value, axis=1)
#             assert new_value.shape == (y.shape[0],)
#         elif x.ndim == 2 and y.ndim == 2:
#             assert x.shape[1] == y.shape[0]
#             new_value = np.array([np.sum((self * other[:, i]).value, axis=1) for i in range(y.shape[1])])
#         else:
#             raise NotImplementedError
#         return QAlgebra(new_value, q)

#     def __eq__(self, other: "QAlgebra") -> bool:
#         assert self._q == other._q, "Parameter q must be the same"
#         ret = np.allclose(self._value, other._value)
#         return ret

#     def __ne__(self, other: "QAlgebra") -> bool:
#         assert self._q == other._q, "Parameter q must be the same"
#         ret = not np.allclose(self._value, other._value)
#         return ret

#     def __lt__(self, other: "QAlgebra") -> bool:
#         assert self._q == other._q, "Parameter q must be the same"
#         ret = np.all(self._value < other._value)
#         return ret

#     def __le__(self, other: "QAlgebra") -> bool:
#         assert self._q == other._q, "Parameter q must be the same"
#         ret = np.all(self._value <= other._value)
#         return ret

#     def __gt__(self, other: "QAlgebra") -> bool:
#         assert self._q == other._q, "Parameter q must be the same"
#         ret = np.all(self._value > other._value)
#         return ret

#     def __ge__(self, other: "QAlgebra") -> bool:
#         assert self._q == other._q, "Parameter q must be the same"
#         ret = np.all(self._value >= other._value)
#         return ret

#     def __str__(self) -> str:
#         return f"QAlgebra({self._value}, {self._q})"
