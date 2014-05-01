import sys
from socos import process_cmd, shell

def main():
    """ main switches between (non-)interactive mode """
    args = sys.argv[1:]

    if args:
        # process command and exit
        process_cmd(args)
    else:
        # start interactive shell
        shell()

if __name__ == '__main__':
    main()
