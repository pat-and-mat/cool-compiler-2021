import typer
from pathlib import Path
from coolpyler.errors import InvalidInputFileError
from coolpyler.lexer import CoolLexer


def report_and_exit(errors):
    if len(errors) == 0:
        raise typer.Exit(code=0)

    for error in errors:
        typer.echo(f"({error.line},{error.column}) - {error.type}: {error.msg}")
    raise typer.Exit(code=1)


def coolpyler(input: Path, output: Path = None):
    errors = []

    if not input.is_file:
        errors.append(InvalidInputFileError(str(input)))

    if len(errors) > 0:
        report_and_exit(errors)

    code = input.read_text()  # noqa: F841

    lexer = CoolLexer(errors)
    tokens = lexer.tokenize(code)
    list(tokens)

    if len(errors) > 0:
        report_and_exit(errors)

    if output is None:
        output = input.with_suffix(".mips")


if __name__ == "__main__":
    typer.run(coolpyler)
