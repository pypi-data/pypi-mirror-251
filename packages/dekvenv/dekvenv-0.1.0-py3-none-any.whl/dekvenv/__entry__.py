from .utils.common import shell_line
from .command import app


def main():
    shell_line('pdm config check_update false')
    shell_line('pdm config install.cache on')
    app()
