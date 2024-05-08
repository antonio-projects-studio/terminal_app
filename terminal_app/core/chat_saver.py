from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from generative_agent import ChatInfo
    from settings import FolderOption

import os
from pathlib import Path

from .stdout_decoration import AttentionPrint


class ChatSaver:

    def __init__(self, folder: Path) -> None:
        self.folder = folder

    @staticmethod
    def generated_directory_name(name: str, x=0) -> str:
        dir_name = (name + ("_" + str(x) if x != 0 else "")).strip()
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
            return dir_name
        else:
            return ChatSaver.generated_directory_name(name, x + 1)

    def save_chat(
        self,
        chat: ChatInfo,
        folder: FolderOption,
        with_json: bool = False,
    ) -> None:
        folder_path = Path(
            self.generated_directory_name((self.folder / folder / chat.name).as_posix())
        )

        print(f"\nSaved the data in a folder {folder_path}")

        # if with_json:
        #     with open(folder_path / "json.txt", "w") as file:
        #         file.write(
        #             json.dumps(
        #                 [asdict(message) for message in chat.chat_history],
        #                 indent=4,
        #             )
        #         )

        AttentionPrint.plog_agent_chat_txt(
            chat,
            path=(folder_path / "dialog.txt").as_posix(),
            mode="w",
            with_color=True,
        )
        # AttentionPrint.plog_gigachat_dialog_html(
        #     chat,
        #     name=dir_name,
        #     metadata=metadata,
        #     path=(folder_path / "dialog.html").as_posix(),
        #     mode="w",
        # )
