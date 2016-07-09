from api.rcon import RemoteConsole, AuthenticationError, ConnectionError
from argparse import ArgumentParser
from getpass import getpass
import six

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
            if command.startswith("help"):
                response = response.replace("/", "\n/")
            print(response)


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
