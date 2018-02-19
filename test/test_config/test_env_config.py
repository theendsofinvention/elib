# coding=utf-8


def test_env_config(dummy_config):
    with open(f'.env', 'w') as stream:
        stream.write('''
debug=true
string=some string
integer=1
some_list=[caribou, gopher, moose]
namespace_key=value
''')
    cfg = dummy_config('test')
    assert cfg.debug is True
    assert cfg.string == 'some string'
    assert cfg.integer is 1
    assert cfg.some_list == ['caribou', 'gopher', 'moose']
    assert cfg.namespace_key == 'value'
