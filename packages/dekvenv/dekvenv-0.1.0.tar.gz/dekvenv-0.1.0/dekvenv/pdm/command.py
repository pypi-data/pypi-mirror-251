import sys
import typer
from ..utils.file import remove_path
from ..utils.common import shell_line
from .core import get_pdm_cache_dir, get_pdm_cache_dir_hash

app = typer.Typer(add_completion=False)


@app.command(
    context_settings=dict(resilient_parsing=True)
)
def install():
    argv = sys.argv[sys.argv.index(install.__name__) + 1:]
    shell_line(f'pdm install {" ".join(argv)}')


@app.command()
def clear():
    shell_line(f'pdm cache clear')
    remove_path(get_pdm_cache_dir())


@app.command()
def clear_hash():
    remove_path(get_pdm_cache_dir_hash())
