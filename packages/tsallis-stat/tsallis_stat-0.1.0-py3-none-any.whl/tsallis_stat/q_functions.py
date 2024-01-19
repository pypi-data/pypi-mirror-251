import numpy as np

from tsallis_stat.q_algebra import QAlgebra

def exp_q(x: QAlgebra) -> QAlgebra:
    v = x._value
    q = x._q
    ret = np.maximum(0, 1 + (1 - q) * v) ** (1 / (1 - q))
    return QAlgebra(ret, q)

def log_q(x: QAlgebra) -> QAlgebra:
    v = x._value
    q = x._q
    ret = (v ** (1 - q) - 1) / (1 - q)
    return QAlgebra(ret, q)

def tsallis_entropy(p: QAlgebra) -> float:
    v = p._value
    assert np.all(v >= 0), "Probabilities must be non-negative"
    assert np.isclose(np.sum(v), 1), "Probabilities must sum to one"
    q = p._q
    return (1 - np.sum(v ** q)) / (1 - q)

def q_entropy(p: QAlgebra) -> float:
    v = p._value
    assert np.all(v >= 0), "Probabilities must be non-negative"
    assert np.isclose(np.sum(v), 1), "Probabilities must sum to one"
    q = p._q
    return - np.sum(v * log_q(p).value - v) / (2 - q)
    
    