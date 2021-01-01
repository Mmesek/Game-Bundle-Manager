from base import add_bundle, key
cmds, help_cmd = {}, {}
def command(**kwargs):
    def inner(f, **_kwargs):
        if 'help' in kwargs:
            help_cmd[str(f.__name__.lower())] = kwargs['help']
        if 'aliases' in kwargs:
            for alias in kwargs['aliases'].split(', '):
                if 'help' in kwargs:
                    help_cmd[alias] = kwargs['help']
                cmds[alias] = f
        else:
            cmds[str(f.__name__.lower())] = f
        return f
    return inner
def subcommand(main, **kwargs):
    def inner(f, **_kwargs):
        if not hasattr(cmds[main], 'subcmds'):
            cmds[main].subcmds = {}
        cmds[main].subcmds[str(f.__name__.lower())] = f
        return f
    return inner

@command()
def mcmd(subcmd, *args):
    print('Main cmd')
    mcmd.subcmds.get(subcmd, Invalid)()

@subcommand(main='mcmd')
def sub(*args):
    print('sub!')

names = {'game':[], 'platform':'Steam', 'price':12.0, 'cc':'USD'}
@command(aliases='game, platform, bundle, price, cc', help='Sets value')
def setter(value, key):
    if value == '':
        pass
    elif key == 'game':
        names[key].append((value, names['platform']))
    else:
        names[key] = value
    return names

@command(help='Adds bundle with games to database')
def add(*args):
    print(names)
    add_bundle(names['bundle'], names['game'], names['price'], names['cc'])
    names['game'].clear()

@command(help='Removes from database setted games')
def remove(*args):
    for game_name, platform in names['game']:
        key(game_name, platform, 1, False)

@command(help='Shows this message')
def help(*args):
    print('Available commands:')
    for msg in help_cmd:
        print(msg, '-', help_cmd[msg])

def Invalid(*args):
    print('Cmd not found')

batch = False
while True:
    i = input().split(' ',1)
    cmd = i[0]
    if cmd =='end':
        break
    if cmd == 'commit':
        batch = False
        continue
    if cmd == 'games':
        batch = True
        continue
    if batch:
        setter(' '.join(i), 'game')
        continue
    try:
        args = i[1]
    except:
        args = []
    cmds.get(cmd, Invalid)(args, cmd)