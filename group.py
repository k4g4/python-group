'''This module provides the Group class, which models groups from group theory.'''

from inspect import signature
from itertools import product
from functools import total_ordering, reduce

__author__ = 'kaga'

@total_ordering
class Group:
    '''Create and model a group with a set of elements and an operation over the set.'''

    def __init__(self, elems, op):
        self._elems = set(elems)

        #Operation check
        if not callable(op) or len(signature(op).parameters) != 2:
            raise TypeError('operation must be callable and take 2 arguments')
        self.op = op

        #Closure check
        if any(op(*ab) not in self._elems for ab in product(self._elems, repeat=2)):
            raise TypeError('the closure property is not satisfied')

        #Associativity check
        is_assoc = lambda x, y, z: op(op(x, y), z) == op(x, op(y, z))
        if any(not is_assoc(*abc) for abc in product(self._elems, repeat=3)):
            raise TypeError('the associativity property is not satisfied')

        #Identity check
        for e in self._elems:
            if all(op(e, a) == op(a, e) == a for a in self._elems):
                self.e = e
                break
        else:
            raise TypeError('the identity property is not satisfied')

        #Inverse check
        has_inverse = lambda x: any(op(x, a) == self.e for a in self._elems)
        if any(not has_inverse(a) for a in self._elems):
            raise TypeError('the inverse property is not satisfied')

    @property
    def elems(self):
        return self._elems

    @property
    def identity(self):
        return self.e

    def __repr__(self):
        return f'Group({self._elems}, {self.op.__name__})'

    def __str__(self):
        return f'<{self._elems}, {self.op.__name__}>'

    def __iter__(self):
        return iter(self._elems)

    def __lt__(self, other):
        if isinstance(other, Group):
            return self._elems < other.elems
        else:
            return self._elems < other

    def __contains__(self, elem):
        return elem in self._elems

    def __len__(self):
        return len(self._elems)

    def operate(self, *elems):
        if any(elem not in self._elems for elem in elems):
            raise ValueError('all elements must be members of the group')
        return reduce(self.op, elems)

    def inverse(self, elem):
        if elem not in self._elems:
            raise ValueError('the element provided is not a member of the group')
        return next(a for a in self._elems if self.op(a, elem) == self.e)

    def is_abelian(self):
        return all(self.op(a, b) == self.op(b, a) for a, b in product(self._elems, repeat=2))

    '''
    def is_cyclic(self):
        pass
    '''
