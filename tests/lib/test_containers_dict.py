from declarativeunittest import *
from construct import *
from construct.lib import *


def test_getitem():
    c = Container(a=1)
    assert c["a"] == 1
    assert c.a == 1
    assert raises(lambda: c.unknownkey) == AttributeError
    assert raises(lambda: c["unknownkey"]) == KeyError

def test_setitem():
    c = Container()
    c.a = 1
    assert c["a"] == 1
    assert c.a == 1
    c["a"] = 2
    assert c["a"] == 2
    assert c.a == 2

def test_delitem():
    c = Container(a=1, b=2)
    del c.a
    assert "a" not in c
    assert raises(lambda: c.a) == AttributeError
    assert raises(lambda: c["a"]) == KeyError
    del c["b"]
    assert "b" not in c
    assert raises(lambda: c.b) == AttributeError
    assert raises(lambda: c["b"]) == KeyError
    assert c == Container()
    assert list(c) == []

def test_ctor_empty():
    c = Container()
    assert len(c) == 0
    assert list(c.items()) == []
    assert c == Container()
    assert c == Container(c)
    assert c == Container({})
    assert c == Container([])

def test_ctor_chained():
    c = Container(a=1)(b=2)(c=3)(d=4)
    assert c == Container(c)

def test_ctor_dict():
    c = Container(a=1)(b=2)(c=3)(d=4)
    c = Container(c)
    assert len(c) == 4
    assert list(c.items()) == [('a',1),('b',2),('c',3),('d',4)]

def test_ctor_seqoftuples():
    c = Container([('a',1),('b',2),('c',3),('d',4)])
    assert len(c) == 4
    assert list(c.items()) == [('a',1),('b',2),('c',3),('d',4)]

@xfail(not supportskwordered, reason="ordered kw was introduced in 3.6")
def test_ctor_orderedkw():
    c = Container(a=1, b=2, c=3, d=4)
    d = Container(a=1)(b=2)(c=3)(d=4)
    assert c == d
    assert len(c) == len(d)
    assert list(c.items()) == list(d.items())

def test_keys():
    c = Container(a=1)(b=2)(c=3)(d=4)
    assert list(c.keys()) == ["a","b","c","d"]

def test_values():
    c = Container(a=1)(b=2)(c=3)(d=4)
    assert list(c.values()) == [1,2,3,4]

def test_items():
    c = Container(a=1)(b=2)(c=3)(d=4)
    assert list(c.items()) == [("a",1),("b",2),("c",3),("d",4)]

def test_iter():
    c = Container(a=1)(b=2)(c=3)(d=4)
    assert list(c) == list(c.keys())

def test_clear():
    c = Container(a=1)(b=2)(c=3)(d=4)
    c.clear()
    assert c == Container()
    assert list(c.items()) == []

def test_pop():
    c = Container(a=1)(b=2)(c=3)(d=4)
    assert c.pop("b") == 2
    assert c.pop("d") == 4
    assert c.pop("a") == 1
    assert c.pop("c") == 3
    assert raises(c.pop, "missing") == KeyError
    assert c == Container()

def test_popitem():
    c = Container(a=1)(b=2)(c=3)(d=4)
    assert c.popitem() == ("d",4)
    assert c.popitem() == ("c",3)
    assert c.popitem() == ("b",2)
    assert c.popitem() == ("a",1)
    assert raises(c.popitem) == IndexError

def test_update_dict():
    c = Container(a=1)(b=2)(c=3)(d=4)
    d = Container()
    d.update(c)
    assert d.a == 1
    assert d.b == 2
    assert d.c == 3
    assert d.d == 4
    assert c == d
    assert list(c.items()) == list(d.items())

def test_update_seqoftuples():
    c = Container(a=1)(b=2)(c=3)(d=4)
    d = Container()
    d.update([("a",1),("b",2),("c",3),("d",4)])
    assert d.a == 1
    assert d.b == 2
    assert d.c == 3
    assert d.d == 4
    assert c == d
    assert list(c.items()) == list(d.items())

def test_copy_method():
    c = Container(a=1)
    d = c.copy()
    assert c == d
    assert c is not d

def test_copy():
    from copy import copy, deepcopy

    c = Container(a=1)
    d = copy(c)
    assert c == d
    assert c is not d

def test_deepcopy():
    from copy import copy, deepcopy

    c = Container(a=1)
    d = deepcopy(c)
    d.a = 2
    assert c != d
    assert c is not d

def test_pickling():
    import pickle

    empty = Container()
    empty_unpickled = pickle.loads(pickle.dumps(empty))
    assert empty_unpickled == empty

    nested = Container(a=1)(b=Container())(c=3)(d=Container(e=4))
    nested_unpickled = pickle.loads(pickle.dumps(nested))
    assert nested_unpickled == nested

def test_eq():
    c = Container(a=1)(b=2)(c=3)(d=4)(e=5)
    d = Container(a=1)(b=2)(c=3)(d=4)(e=5)
    assert c == c
    assert c == d

@xfail(not supportsnumpy, reason="numpy is not installed?")
def test_eq_numpy():
    import numpy

    c = Container(arr=numpy.zeros(10, dtype=numpy.uint8))
    assert c == c

def test_ne():
    c = Container(a=1)(b=2)(c=3)
    d = Container(a=1)(b=2)(c=3)(d=4)(e=5)
    assert c != d
    assert d != c

def test_str_repr_empty():
    c = Container()
    assert str(c) == "Container: "
    assert repr(c) == "Container()"
    assert eval(repr(c)) == c

def test_str_repr():
    c = Container(a=1)(b=2)(c=3)
    assert str(c) == "Container: \n    a = 1\n    b = 2\n    c = 3"
    assert repr(c) == "Container(a=1)(b=2)(c=3)"
    assert eval(repr(c)) == c

def test_str_repr_nested():
    c = Container(a=1)(b=2)(c=Container())
    assert str(c) == "Container: \n    a = 1\n    b = 2\n    c = Container: "
    assert repr(c) == "Container(a=1)(b=2)(c=Container())"
    assert eval(repr(c)) == c

def test_str_repr_recursive():
    c = Container(a=1)(b=2)
    c.c = c
    assert str(c) == "Container: \n    a = 1\n    b = 2\n    c = <recursion detected>"
    assert repr(c) == "Container(a=1)(b=2)(c=<recursion detected>)"

def test_str_fullprinting():
    c = Container(data=b"\x01\x02\x034567890")
    assert str(c) == "Container: \n    data = \\x01\\x02\\x034567890 (total 10)"
    c = Container(data=u"\x01\x02\x034567890")
    assert str(c) == "Container: \n    data = \\x01\\x02\\x034567890 (total 10)"
    c = Container(data=b"\x01"*1024)
    assert str(c) == "Container: \n    data = \\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01... (truncated, total 1024)"
    c = Container(data=u"\x01"*1024)
    assert str(c) == "Container: \n    data = \\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01\\x01... (truncated, total 1024)"

def test_len_bool():
    c = Container(a=1)(b=2)(c=3)(d=4)
    assert len(c) == 4
    assert c
    c = Container()
    assert len(c) == 0
    assert not c

def test_in():
    c = Container(a=1)
    assert "a" in c
    assert "b" not in c

def test_regression_recursionlock():
    print("REGRESSION: recursion_lock() used to leave private keys.")
    c = Container()
    str(c); repr(c)
    assert not c