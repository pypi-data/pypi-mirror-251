import dataclasses
import json
import os
from pathlib import Path

from lipsgit.defaults import DEFAULT_EMOJIS
from lipsgit.exceptions import LipsgitConfigNotFoundException
from lipsgit.models import Emoji


class LipsgitStorage:
    LIPGIT_DIR = f"{Path.home()}/.lipsgit"

    def __init__(self):
        # TODO: Doesn't need to be a class but will probably want to in the future
        pass

    def initialise(self):
        if not os.path.exists(self.LIPGIT_DIR):
            os.makedirs(self.LIPGIT_DIR)
        emoji_config_path = self._get_emoji_config_path()
        if not os.path.exists(emoji_config_path):
            with open(emoji_config_path, "w") as file:
                json.dump({"emojis": DEFAULT_EMOJIS}, file)

    def load_commit_emojis(self):
        emoji_config_path = self._get_emoji_config_path()
        if not os.path.exists(emoji_config_path):
            raise LipsgitConfigNotFoundException()
        with open(emoji_config_path, "r") as file:
            data = json.load(file)
        if data is None or "emojis" not in data:
            raise LipsgitConfigNotFoundException()
        return [Emoji(**emoji_data) for emoji_data in data["emojis"]]

    def store_commit_emojis(self, emojis: list[Emoji]) -> None:
        emoji_config_path = self._get_emoji_config_path()
        emoji_dict = {"emojis": [dataclasses.asdict(emoji) for emoji in emojis]}
        with open(emoji_config_path, "w") as json_file:
            json.dump(emoji_dict, json_file)

    @staticmethod
    def get_title_from_commit_file(commit_file_path: str) -> str:
        with open(commit_file_path, "r") as file:
            lines = file.readlines()
        return lines[0]

    @staticmethod
    def override_commit_message(
        commit_file_path: str, commit_emoji: Emoji
    ) -> None:
        with open(commit_file_path, "r") as file:
            lines = file.readlines()

        # Modify the first line by adding your string at the beginning
        lines[0] = f"{commit_emoji.character} {lines[0]}"

        # Open the file in write mode to overwrite its content
        with open(commit_file_path, "w") as file:
            file.writelines(lines)

    def _get_emoji_config_path(self) -> str:
        return os.path.join(self.LIPGIT_DIR, "emoji-data.json")
