from api.rcon import RemoteConsole, AuthenticationError, ConnectionError
from argparse import ArgumentParser
from getpass import getpass
import six, colorama, re

"""
Minecraft RCON Client Console
"""


def parse_arguments():
    """ Provides host and port options for command-line use.

    @return: options namespace based on provided arguments
    """
    parser = ArgumentParser(description="Connect to a Minecraft RCON server")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="default: 127.0.0.1"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=25575,
        help="default: 25575"
    )
    parser.add_argument(
        "--password",
        help="rcon password"
    )
    return parser.parse_args()


def get_input(prompt):

    input_func = None

    if six.PY2:
        input_func = raw_input
    else:
        input_func = input

    return input_func(prompt)


def rcon_shell(rcon):
    """ Reads a command from the prompt, sends it to the server, processes the
    response, and returns the output to the user. Allows quitting with "quit"
    or "q", and adds newlines to help page output to improve readability.

    @param rcon: Instance of api.rcon.RemoteConsole()
    """
    print("\n  Welcome to the rcon shell. Enter commands here to send them")
    print("  to the RCON server. To quit, type \"quit\" or \"q\".\n")

    while True:
        command = get_input("rcon> ")
        if command in ["quit", "q"]:
            return
        response, response_id = rcon.send(command)
        if response:
            print(multiple_replace(color_map, response.decode('UTF-8')))

color_map = {'§0': '\033[30m',
'§1': '\033[34m',
'§2': '\033[32m',
'§3': '\033[34m',
'§4': '\033[31m',
'§5': '\033[35m',
'§6': '\033[33m',
'§7': '\033[37m',
'§8': '\033[37m',
'§9': '\033[34m',
'§a': '\033[32m',
'§b': '\033[34m',
'§c': '\033[31m',
'§d': '\033[35m',
'§e': '\033[33m',
'§f': '\033[37m'
}

def multiple_replace(dict, text):

  """ Replace in 'text' all occurences of any key in the given
  dictionary by its corresponding value.  Returns the new tring."""

  # Create a regular expression  from the dictionary keys
  regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

  # For each match, look-up corresponding value in dictionary
  return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) + '\033[0m'

def main():
    """ Reads command-line arguments, connects to the RCON server, and starts
    the rcon_shell loop. Handles exceptions and interrupts, and disconnects
    when finished.
    """
    options = parse_arguments()
    rcon = None
    print("Connecting to %s:%d..." % (options.host, options.port))
    if options.password:
        password = options.password
    else:
        password = getpass()
    try:
        rcon = RemoteConsole(
            options.host,
            options.port,
            password
        )
        rcon_shell(rcon)
    except ConnectionError:
        print("Connection failed.")
        exit(1)
    except AuthenticationError:
        print("Authentication failed.")
    except KeyboardInterrupt:
        print('')
    finally:
        if rcon:
            rcon.disconnect()
        print("Disconnected.")

if __name__ == "__main__":
    main()
