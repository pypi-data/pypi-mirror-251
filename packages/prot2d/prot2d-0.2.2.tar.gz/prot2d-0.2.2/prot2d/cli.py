import typer
from .Main import check_pdb_path
from .Helper_functions import count_residues

app = typer.Typer()

app.command()(check_pdb_path)
app.command()(count_residues)

if __name__ == "__main__":
    app()