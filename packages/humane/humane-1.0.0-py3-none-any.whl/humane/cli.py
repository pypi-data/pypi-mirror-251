import click
from humane.emojihash import emoji_hash
from humane.humanid import (
    MAX_N,
    Wordlist,
    human_id,
    short_human_id,
    total_possibilities,
)


@click.group()
def main():
    pass


@main.command()
@click.argument("string", required=False)
@click.option("--short", "-s", is_flag=True, help="Short option")
def id(string, short):
    id_generator = short_human_id if short else human_id
    click.echo(id_generator(string))


@main.command()
@click.argument("string", required=False)
def emoji_id(string):
    click.echo(emoji_hash(string))


@main.command()
@click.argument("type", type=click.Choice(["id", "emoji", "short"]))
def entropy(type):
    if type == "id":
        total = total_possibilities(
            [
                Wordlist.ADJECTIVES,
                Wordlist.ANIMALS,
                Wordlist.ADVERBS,
                Wordlist.VERBS,
            ],
            start=MAX_N,
        )
    elif type == "emoji":
        total = 256**4
    elif type == "short":
        total = total_possibilities(
            [
                Wordlist.ADJECTIVES,
                Wordlist.ANIMALS,
            ],
            start=MAX_N,
        )

    click.echo(f"{total:,}")


if __name__ == "__main__":
    main()
