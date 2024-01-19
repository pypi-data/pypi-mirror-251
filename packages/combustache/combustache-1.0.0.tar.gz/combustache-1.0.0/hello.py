import combustache


class C:
    hello = False
    # def hello(self):
    #     return True


template = '{{hello.hello}}'
data = {'hello': C()}


def lowercase_bool(val):
    if val is None:
        return ''
    if isinstance(val, bool):
        return str(val).lower()
    return str(val)


out = combustache.render(template, data, stringify=lowercase_bool)
print(out)
