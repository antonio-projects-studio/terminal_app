__all__ = ["TFormatting", "Languages"]

from enum import StrEnum
from typing import Any


class Languages(StrEnum):
    CPP = "c++"
    PYTHON = "python"
    JAVA = "java"


class TFormatting(StrEnum):
    MDASH = "&#8212"
    ANTONIO = "@Antonio_Rodriges"

    @staticmethod
    def hashtag(value: str) -> str:
        return f"#{value}"

    @staticmethod
    def bold(value: str) -> str:
        return f"<b>{value}</b>"

    @staticmethod
    def italic(value: str) -> str:
        return f"<i>{value}</i>"

    @staticmethod
    def code(value: str) -> str:
        return f"<code>{value}</code>"

    @staticmethod
    def strike(value: str) -> str:
        return f"<strike>{value}</strike>"

    @staticmethod
    def underline(value: str) -> str:
        return f"<underline>{value}</underline>"

    @staticmethod
    def pre(value: str, language: Languages) -> str:
        return f'<pre language="{language}">{value}</pre>'

    @staticmethod
    def dict_formatting(data: dict[str, Any]) -> str:
        return "\n\n".join([f"{name + ":"}\n{value}" for name, value in data.items()])

    @staticmethod
    def list_formatting(data: list[Any], start: int = 1) -> str:
        return "\n".join([f"{ind + start}. {x}" for ind, x in enumerate(data)])

    @staticmethod
    def notice(message: str) -> str:
        return "Notice: " + message

    @staticmethod
    def error(message: str) -> str:
        return "ERROR: " + message

    @staticmethod
    def command(command: str) -> str:
        return f"/{command}"

    @staticmethod
    def commands(commands: list[Any]) -> str:
        return "\n".join([f"{getattr(command, "command")} {TFormatting.MDASH} {getattr(command, "description")}"for command in commands])

    @staticmethod
    def done_emoji(message: str) -> str:
        return f"✅ {message}"

    @staticmethod
    def fail_emoji(message: str) -> str:
        return f"❌ {message}"   

    @staticmethod
    def notice_emoji(message: str) -> str:
        return f"⚠️ {message}"  
    
    @staticmethod
    def error_emoji(message: str) -> str:
        return f"⛔ {message}"   

    @staticmethod
    def new_emoji(message: str) -> str:
        return f"🆕 {message}"   
    
    @staticmethod
    def in_process_emoji(message: str) -> str:
        return f"⏳ {message}"  
    
