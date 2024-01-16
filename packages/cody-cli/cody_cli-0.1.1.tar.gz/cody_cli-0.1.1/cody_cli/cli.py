import io
import click
from openai import OpenAI


@click.group()
def cli():
    pass


@cli.command()
@click.argument("source", type=click.File("rt", encoding="utf-8"))
@click.option(
    "-m", "--model", default="gpt-3.5-turbo", help="OpenAI model option. (i.e. gpt-4)"
)
def code(source: io.TextIOWrapper, model: str) -> None:
    """Code completion"""
    client = OpenAI()
    prompt = source.read()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a code assistant, an expert in python, django, and react native. "
                           "You only write code, no comments, no explanations, just code.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    click.echo(response.choices[0].message.content)


if __name__ == "__main__":
    cli()
