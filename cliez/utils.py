# -*- coding: utf-8 -*-


# for python,@see  _AttributeDict
# class dict2obj(object):
#     def __init__(self, d):
#         for a, b in d.items():
#             if isinstance(b, (list, tuple)):
#                setattr(self, a, [dict2obj(x) if isinstance(x, dict) else x for x in b])
#             else:
#                setattr(self, a, dict2obj(b) if isinstance(b, dict) else b)

class _AttributeDict(dict):
    """
    Dictionary subclass enabling attribute lookup/assignment of keys/values.
    Code From fabric.utils

    For example::

        >>> m = _AttributeDict({'foo': 'bar'})
        >>> m.foo
        'bar'
        >>> m.foo = 'not bar'
        >>> m['foo']
        'not bar'

    ``_AttributeDict`` objects also provide ``.first()`` which acts like
    ``.get()`` but accepts multiple keys as arguments, and returns the value of
    the first hit, e.g.::

        >>> m = _AttributeDict({'foo': 'bar', 'biz': 'baz'})
        >>> m.first('wrong', 'incorrect', 'foo', 'biz')
        'bar'

    """
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            # to conform with __getattr__ spec
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

    def first(self, *names):
        for name in names:
            value = self.get(name)
            if value:
                return value







