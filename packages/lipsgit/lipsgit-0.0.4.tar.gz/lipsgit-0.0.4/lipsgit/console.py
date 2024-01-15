import inquirer
from inquirer import List
from rich.console import Console

from lipsgit.models import Emoji


class LipsgitConsole(Console):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_new_emoji_details() -> Emoji:
        questions = [
            inquirer.Text("character", message="📰 Emoji Character"),
            inquirer.Text("description", message="📝 Emoji Description"),
        ]
        answers = inquirer.prompt(questions)

        return Emoji(**answers)

    @staticmethod
    def get_commit_message_details() -> dict[str, str]:
        questions = [
            inquirer.Text("title", message="📰 Commit title"),
            inquirer.Text("description", message="📝 Commit description"),
        ]
        answers = inquirer.prompt(questions)

        return answers

    @staticmethod
    def get_emoji_choice(emoji_choices: list[Emoji]) -> Emoji:
        emoji_choice_dict = {
            f"{emoji.character} - {emoji.description}": emoji
            for emoji in emoji_choices
        }
        questions = [
            List(
                "emoji",
                message="😃 Commit Emoji",
                choices=emoji_choice_dict.keys(),
                carousel=True,
            ),
        ]
        answers = inquirer.prompt(questions)

        return emoji_choice_dict[answers["emoji"]]

    @staticmethod
    def _emoji_choice_list_prompt(choices: list[Emoji]) -> List:
        emoji_choice_dict = {
            f"{emoji.character} - {emoji.description}": emoji.character
            for emoji in choices
        }
        return List(
            "emoji",
            message="😃 Commit Emoji",
            choices=emoji_choice_dict.keys(),
        )
