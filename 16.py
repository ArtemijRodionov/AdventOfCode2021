import fileinput
import functools
import operator
from io import StringIO


def to_bin(hex_number):
    return bin(int('1' + hex_number, base=16))[3:]


def to_dec(bin_number):
    return int(bin_number, base=2)


class Parser:

    def __init__(self, data):
        self._data = data
        self.position = data.tell()

    @classmethod
    def read(self, data):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __repr__(self):
        return '<{} {}>'.format(
            type(self).__name__,
            ' '.join([
                '{}={}'.format(x, getattr(self, x))
                for x in sorted(dir(self))
                if not x.startswith('_') and x != 'read'
            ])
        )


class OperatorLength(Parser):

    def __init__(self, length, data):
        self.length = length
        super().__init__(data)

    @classmethod
    def read(cls, data):
        return cls(to_dec(data.read(15)), data)

    def __iter__(self):
        while self._data.tell() - self.position < self.length:
            yield from Packet.read(self._data)
        assert self._data.tell() - self.position == self.length


class OperatorNumber(Parser):

    def __init__(self, number, data):
        self.number = number
        super().__init__(data)

    @classmethod
    def read(cls, data):
        return cls(to_dec(data.read(11)), data)

    def __iter__(self):
        for _ in range(self.number):
            yield from Packet.read(self._data)


class Operator(Parser):

    def __init__(self, type_id, data):
        self.type_id = type_id
        assert self.type_id in {0, 1}
        super().__init__(data)

    @classmethod
    def read(cls, data):
        return cls(to_dec(data.read(1)), data)

    def __iter__(self):
        if self.type_id == 0:
            yield from OperatorLength.read(self._data)
        elif self.type_id == 1:
            yield from OperatorNumber.read(self._data)


class Literal(Parser):

    def __init__(self, start, value, data):
        self.start = start
        self.value = value
        assert self.start in {0, 1}
        super().__init__(data)

    @classmethod
    def read(cls, data):
        return cls(to_dec(data.read(1)), to_dec(data.read(4)), data)

    def __iter__(self):
        yield self
        if self.start == 1:
            yield from Literal.read(self._data)


class Packet(Parser):

    def __init__(self, version, type_id, data):
        self.version = version
        self.type_id = type_id
        super().__init__(data)

    @classmethod
    def read(cls, data):
        return cls(to_dec(data.read(3)), to_dec(data.read(3)), data)

    def __iter__(self):
        yield self
        if self.type_id == 4:
            yield from Literal.read(self._data)
        else:
            yield from Operator.read(self._data)
        yield EndPacket(self)


class EndPacket(Parser):
    
    def __init__(self, packet):
        self.position = packet.position
        self.version = packet.version
        self.type_id = packet.type_id


def eval_literal(xs):
    return sum(x.value << (i * 4) for i, x in enumerate(reversed(xs)))


def eval_packet(packets, ops):
    if (s := next(packets, None)) is None:
        return []

    if isinstance(s, Packet):
        fn = ops[s.type_id]
        args = eval_packet(packets, ops)
        return [fn(args)] + eval_packet(packets, ops)
    elif isinstance(s, EndPacket):
        return []
    elif isinstance(s, Literal):
        return [s] + eval_packet(packets, ops)

    raise NotImplementedError()


def eval_packets(packets):
    ops = {
        0: sum,
        1: functools.partial(functools.reduce, operator.mul),
        2: min,
        3: max,
        4: eval_literal,
        5: lambda xs: int(xs[0] > xs[1]),
        6: lambda xs: int(xs[0] < xs[1]),
        7: lambda xs: int(xs[0] == xs[1]),
    }
    return eval_packet(iter(packets), ops)


def print_packets(packets):
    J = lambda xs: ', '.join(map(str, xs))
    ops = {
        0: lambda xs: 'sum({})'.format(J(xs)),
        1: lambda xs: 'mul({})'.format(J(xs)),
        2: lambda xs: 'min({})'.format(J(xs)),
        3: lambda xs: 'max({})'.format(J(xs)),
        4: lambda xs: str(eval_literal(xs)),
        5: lambda xs: 'gt({})'.format(J(xs)),
        6: lambda xs: 'ls({})'.format(J(xs)),
        7: lambda xs: 'eq({})'.format(J(xs)),
    }
    print('{} == {}'.format(
        eval_packet(iter(packets), ops)[0],
        eval_packets(packets)[0]
    ))


def sum_versions(xs):
    return sum([
        x.version for x in xs
        if isinstance(x, Packet)
    ])


payload = to_bin(next(fileinput.input()).strip())
packets = list(Packet.read(StringIO(payload)))
print(sum_versions(packets))
print(eval_packets(packets))
print_packets(packets)
