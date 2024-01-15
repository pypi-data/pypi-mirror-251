import rich_click as click

from lipsgit.console import LipsgitConsole
from lipsgit.matching import semantic_commit_matching
from lipsgit.storage import LipsgitStorage
from lipsgit.git import git_commit, get_base_git_repo_path

lipsgit_console = LipsgitConsole()
lipsgit_storage = LipsgitStorage()


def entry_point():
    try:
        lipsgit()
    except (Exception, KeyboardInterrupt) as exception:
        lipsgit_console.print(exception, style="red")
        exit(0)


@click.group()
def lipsgit():
    """😍 Lipsgit - Command line tool for enabling pretty emoji commits"""


@lipsgit.command(name="init")
def initialise():
    """Initialize lipsgit configuration"""
    with lipsgit_console.status("Initialising lipsgit", spinner="dots"):
        lipsgit_storage.initialise()
    lipsgit_console.print("🏗️ lipsgit config has been initialised!")


@lipsgit.command(name="hook")
def emoji_hook():
    """Run lipsgit as part of a commit_message hook"""
    emoji_list = lipsgit_storage.load_commit_emojis()
    base_path = get_base_git_repo_path()
    if base_path is not None:
        commit_file_path = f"{base_path}/.git/COMMIT_EDITMSG"
        commit_title = lipsgit_storage.get_title_from_commit_file(
            commit_file_path
        )
        with lipsgit_console.status("Matching emoji to commit", spinner="dots"):
            emoji_choice = semantic_commit_matching(commit_title, emoji_list)[0]

        lipsgit_storage.override_commit_message(commit_file_path, emoji_choice)


@lipsgit.command(name="add")
def add_emoji():
    """Add a custom emoji entry to lipsgit"""
    emoji_list = lipsgit_storage.load_commit_emojis()
    new_emoji = lipsgit_console.get_new_emoji_details()
    with lipsgit_console.status("Adding emoji", spinner="dots"):
        emoji_list.append(new_emoji)
        lipsgit_storage.store_commit_emojis(emoji_list)
    lipsgit_console.print(
        f"[bold]{new_emoji.character}: {new_emoji.description}[/bold] added!"
    )


@lipsgit.command(name="commit")
@click.option(
    "--match",
    type=bool,
    is_flag=True,
    help="Use semantic commit matching to automatically choose an emoji",
)
def commit(match: bool):
    """Interactively commit with an emoji"""
    commit_details = lipsgit_console.get_commit_message_details()
    emoji_list = lipsgit_storage.load_commit_emojis()
    if match:
        with lipsgit_console.status("Matching emoji to commit", spinner="dots"):
            emoji_choice = semantic_commit_matching(
                commit_details["title"], emoji_list
            )[0]
    else:
        emoji_choice = lipsgit_console.get_emoji_choice(emoji_list)
    git_commit(
        f'{emoji_choice.character} {commit_details["title"]}',
        commit_details["description"],
    )
