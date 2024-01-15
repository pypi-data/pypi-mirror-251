# TODO: add Fraction

import operator
from fractions import Fraction
from typing import Callable, Iterable, SupportsIndex

from .templatelib.utils import _inplace, common_rational

__all__ = ['Dimension']

_DIM_VAR = ('L', 'M', 'T', 'I', 'H', 'N', 'J')
_DIM_NUM = len(_DIM_VAR)


def _unpack_vector():
    def __getter(i): return lambda self: self[i]  # closure
    return (property(__getter(i)) for i in range(_DIM_NUM))


def _unary_op(op: Callable[[Fraction], Fraction]):
    '''unary operation: +v, -v.'''

    def __op(self: 'Dimension') -> 'Dimension': 
        return Dimension.unpack(map(op, self))
    return __op


def _vector_add(op: Callable[[Fraction, Fraction], Fraction]):
    '''vector addition: v + u, v - u.'''

    def __op(self: 'Dimension', other: 'Dimension') -> 'Dimension':
        return Dimension.unpack(map(op, self, other))
    return __op, _inplace(__op)


def _scalar_mul(op: Callable[[Fraction, int | Fraction], Fraction]):
    '''scalar multiplication: c * v, v / c.'''

    def __op(self: 'Dimension', c: int | Fraction) -> 'Dimension':
        return Dimension.unpack(op(x, c) for x in self)
    return __op, _inplace(__op)


class Dimension:
    __slots__ = ('__vector',)

    def __init__(self, L=0, M=0, T=0, I=0, H=0, N=0, J=0) -> None:
        dimension_vector = (L, M, T, I, H, N, J)
        self.__vector = tuple(map(common_rational, dimension_vector))

    @classmethod
    def unpack(cls, iterable: dict | Iterable, /): 
        if isinstance(iterable, dict):
            return cls(**iterable)
        return cls(*iterable)

    def __getitem__(self, key: SupportsIndex): return self.__vector[key]

    def __iter__(self): return iter(self.__vector)

    L, M, T, I, H, N, J = _unpack_vector()
    length, mass, time, electric_current, thermodynamic_temperature, \
        amount_of_substance, luminous_intensity = L, M, T, I, H, N, J

    def __repr__(self) -> str:
        para = ', '.join(f'{var}={val}' for var, val in zip(_DIM_VAR, self))
        return f'{self.__class__.__name__}({para})'

    def __str__(self) -> str: return '(' + ', '.join(map(str, self)) + ')'

    def __len__(self) -> int: return _DIM_NUM

    def __hash__(self) -> int: return hash(self.__vector)

    def __eq__(self, other: 'Dimension') -> bool:
        return self.__vector == other.__vector

    __pos__ = _unary_op(operator.pos)
    __neg__ = _unary_op(operator.neg)

    __add__, __iadd__ = _vector_add(operator.add)
    __sub__, __isub__ = _vector_add(operator.sub)

    __mul__, __imul__ = _scalar_mul(operator.mul)
    __rmul__ = __mul__
    __truediv__, __itruediv__ = _scalar_mul(operator.truediv)
    

if __name__ == '__main__':
    a = '''length
    mass
    time
    electric current
    thermodynamic temperature
    amount of substance
    luminous intensity'''
    print(a.replace(' ', '_').upper())
