from __future__ import annotations
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from generative_agent import ChatInfo
    from gigachat.models import Messages, MessagesRole

from pprint import pprint
import sys
from textwrap import dedent

ORIG_STDOUT = sys.stdout

class AttentionPrint:

    DEFAULT_LOG: str | None = None
    DEFAULT_CNT = 20
    HTML =  \
    dedent(
    """
    <html>
    <head>
        <title>
            {name}
        </title>
    </head>
        <body style="background-color:rgba(47,49,60,255);">
            <h1 style={color}>{name}</h1>
            <h2 style={color}>Metadata</h2>
            <div style={color}>{metadata}</div>
            <h2 style={color}>Dialog</h2>
            {body}
        </body>
    </html>
    """
    ).strip()

    def __init__(self, name: str, cnt: int = DEFAULT_CNT, point: bool = False):
        self.name = name
        self.point = point
        self.cnt = cnt

    @staticmethod
    def notice(name: str = "Notice", cnt: int = DEFAULT_CNT) -> str:
        half_len: int = int((cnt - len(name)) / 2)
        result = "!" + "-" * half_len + name + "-" * half_len + "!"
        result += "\n"
        return result

    @staticmethod
    def pretty_list(data: list, exclude: list=[]) -> str:
        result: str = ""
        for ind, item in enumerate(data):
            if item not in exclude:
                result += f"{ind}. {item}"
                if ind != len(data) - 1:
                    result += "\n"

        return result

    def __enter__(self):
        if self.point is True:
            name = "Start" + " " + self.name
        else:
            name = self.name

        print(self.notice(name, self.cnt))

        return self

    @staticmethod
    def pprint(data: Any):
        pprint(data)

    @staticmethod
    def plog_agent_chat_txt(
        chat: ChatInfo,
        path: str | None = DEFAULT_LOG,
        mode: str = "a",
        with_color: bool = False
    ):
        metadata: dict = {}
        for agent in chat.participants:
            metadata[agent.name] = agent.metadata()

        if mode not in ["w", "a"]:
            print("Incorrect logging mode")
            return
        if path:
            with open(path, mode) as f:

                sys.stdout = f
 
                print(chat.name)

                for message in chat.chat_history:
                    print(end="\n\n")
                    color = ""
                    # if with_color:
                        # color = message.message.agent.color.txt
                    
                    print(repr(message))

                if metadata:
                    print("\nMETADATA\n")
                    for agent, data in metadata.items():
                        print(f"{agent.upper()} ")
                        AttentionPrint.pprint(data)
                        print("\n")

                sys.stdout = ORIG_STDOUT

    @staticmethod
    def plog_gigachat_dialog_html(
        messages: list[Messages],
        name: str = "data",
        metadata: dict = {},
        path: str | None = DEFAULT_LOG,
        mode: str = "a",
    ):

        if mode not in ["w", "a"]:
            print("Incorrect logging mode")
            return
        if path:
            with open(path, mode) as f:

                sys.stdout = f
                colors = {
                    MessagesRole.SYSTEM: "color:rgba(167,155,228,255);",
                    MessagesRole.ASSISTANT: "color:rgba(72,179,123,255);",
                    MessagesRole.USER: "color:rgba(123,189,203,255);"
                }
                html = dedent(
                """
                <html>
                <head>
                    <title>
                        {name}
                    </title>
                </head>
                    <body style="background-color:rgba(47,49,60,255);">
                        <h1 style={color}>{name}</h1>
                        <h2 style={color}>Metadata</h2>
                        <div style={color}>{metadata}</div>
                        <h2 style={color}>Dialog</h2>
                        {body}
                    </body>
                </html>
                """
                ).strip()
                
                body: str = ""
                cnt: int = -1

                for message in messages:
                    body += "\n\n"
                    color = colors[message.role]
                    
                    number = f'<p style={colors[MessagesRole.SYSTEM]}>\n#{(cnt := cnt + 1)}</p>' if message.role == MessagesRole.USER else ''

                    body += f"<div>{number}<p style={color}>\nRole: {message.role}<br/>\n{message.content.replace("\n", "<br/>\n")}\n</p></div>"
                    
                data: str = ""
                if metadata:
                    for key, value in metadata.items():
                        data += f"{key}: {value}<br/>\n"
                        
                print(html.format(name=name, body=body, metadata=data, color=colors[MessagesRole.SYSTEM]))

                sys.stdout = ORIG_STDOUT

    @staticmethod
    def plog(
        data: Any,
        name: str = "data",
        desc: dict[str, str] = {},
        path: str | None = DEFAULT_LOG,
        mode: str = "a",
        pretty_list: bool = False,
    ):
        if mode not in ["w", "a"]:
            print("Incorrect logging mode")
            return
        if path:
            with open(path, mode) as f:

                sys.stdout = f
                with AttentionPrint(name=name) as log:

                    print(f"{name} = ", end="")
                    if pretty_list:
                        log.pprint(data)

                    else:
                        if isinstance(data, dict):
                            log.pprint(data)
                        else:
                            print(data)

                    if desc:
                        print("\n")
                        for key, value in desc.items():
                            print(f"{key.upper()} ", value, end="\n")

                sys.stdout = ORIG_STDOUT

    def __exit__(self, type, value, traceback):
        print("\n" * 2)
        if self.point is True:
            name = "End" + " " + self.name
        else:
            name = ""

        print(self.notice(name, self.cnt))

        print("\n")
