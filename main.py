import logging
import logging.config
from cli import Cli
from config import LOG_CONF


def main():
    """ The main function executes the program """
    logging.config.fileConfig(LOG_CONF)
    cli = Cli()
    cli.parse_arguments_advanced()
    # try:
    #     ret = cli.args_handel()
    #     if ret is not None:
    #         print(ret)
    # except Exception as ex:
    #     logging.error(f'failed to handel args, error: {ex}')

    ret = cli.args_handel()


if __name__ == '__main__':
    # main()
    print(__name__)