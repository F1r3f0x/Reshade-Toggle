"""
    Reshade Toggle
    Patricio Labin (@plabin)
    November 2018
"""


import json, os, argparse


RENDERERS = {
    'DX9':'d3d9.dll',
    'DX10+': 'dxgi.dll',
    'OGL': 'opengl32.dll'
    #'VULKAN': 'vk.dll'
}

class Game:
    def __init__(self, name, directory, renderer):
        self.name = name
        self.directory = directory
        self.renderer = renderer

if __name__ == '__main__':

    parser = argparse.ArgumentParser('Reshade Disabler', None, 'Disables or enables reshade to the games registered in a config file.')
    parser.add_argument('operation', type=str, choices=['deactivate', 'activate'])

    args = parser.parse_args()
    
    print('Reshade Toggle\n@f1r3f0x - 2018\n')
    print('Operation: ' + args.operation)

    # Get the config file
    config_json = None
    try: 
        fp = open('config.json', 'r')
        config_json = json.loads(fp.read())
    except FileNotFoundError as err:
        print('config.json FILE NOT FOUND')
        quit(1)
    except json.JSONDecodeError:
        print('Error at decoding the config file')
        quit(1)

    # Parse JSON
    games = []
    for record in config_json['games']:
        game = Game(
            record['name'],
            record['directory'],
            record['renderer']
        )
        if game.renderer not in RENDERERS.keys():
            print(f'The Game {game.name} has a wrong renderer')
            quit(1)

        games.append(game)

    # Do the thing
    for game in games:


        # Check if dll is there
        entries = [x.name for x in os.scandir(game.directory)]

        renderer_dll = RENDERERS[game.renderer]
        spaces = '_____'
        if renderer_dll or spaces+renderer_dll in entries:
            # do op
            try:
                if args.operation == 'deactivate':
                    os.rename(game.directory + f'/{renderer_dll}', game.directory + f'/{spaces}{renderer_dll}')
                if args.operation == 'activate':
                    os.rename(game.directory + f'/{spaces}{renderer_dll}', game.directory + f'/{renderer_dll}')
                print('Toggled ' + game.name + ' in path ' + game.directory)  
            except FileNotFoundError as err:
                print('\tCouldn\'t operate in game: ' + game.name + '. maybe is already toggled?')
        else:
            print(f'Can\'t find reshade in the folder of {game.name}')