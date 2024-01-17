"""
cheerup - Cheer on your command-line expertise!
"""
import argparse
import os
import sys
import tempfile
from pprint import pprint
from typing import Optional
import json

import openai
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
)


client = OpenAI()


historyfile = os.path.join(tempfile.gettempdir(), "cheerup_history.json")


def get_history() -> list[ChatCompletionMessageParam]:
    """Get history from file."""
    history = []
    try:
        with open(historyfile, "r", encoding="utf-8") as file:
            jsondata = file.read()
            history = json.loads(jsondata)
    except (FileNotFoundError, json.JSONDecodeError):
        pass  # Return [] if file not found or broken

    return history


def save_history(history: list[ChatCompletionMessageParam]) -> None:
    """Save history to file."""
    with open(historyfile, "w", encoding="utf-8") as file:
        jsondata = json.dumps(history, indent=2)
        file.write(jsondata)


def chat(cmd: str, locale: Optional[str] = None) -> str:
    """Print response from OpenAI API."""

    # pylint: disable=line-too-long
    prompt = "You are an AI assistant adept at complimenting programmers. Please provide verbose compliments with many emojis on the user's Unix command inputs."
    if locale:
        prompt += f" Use the language in the locale: {locale}."
    history = get_history()

    query: ChatCompletionUserMessageParam = {"role": "user", "content": cmd}
    messages: list[ChatCompletionMessageParam] = [
        *history,
        {
            "role": "system",
            "content": prompt,
        },
        query,
    ]
    # pprint(messages)

    print("🤖 ", end="", flush=True)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
    )

    # pprint(response)

    try:
        answer = ""

        for chunk in response:  # pylint: disable=not-an-iterable
            # pprint(chunk)
            content = chunk.choices[0].delta.content

            if content:
                print(content, end="", flush=True)
                answer += content
        print()

        # answer = response.choices[0].message.content
        # print(answer)
    except KeyboardInterrupt:
        print("(skip)")
    new_completion: ChatCompletionAssistantMessageParam = {
        "role": "assistant",
        "content": answer,
    }
    save_history([*history, query, new_completion][-10:])
    return answer


def interactive(lang: Optional[str] = None) -> None:
    """Interactive mode."""

    while True:
        try:
            cmd = input("$ ")
            chat(cmd, lang)
        except (KeyboardInterrupt, EOFError):
            return


# pylint: disable=consider-using-f-string
def show_zsh_script() -> None:
    """Show inititialize script for zsh."""
    command = sys.argv[0]
    print(
        """
# Save the last command.
CHEERUP_LAST_COMMAND=""
CHEEUP_EXE="%s"

preexec() {
    CHEERUP_LAST_COMMAND=$1
}

precmd() {
    # Prevent cheerup command from running on itself.
    if [[ "$CHEERUP_LAST_COMMAND" != "$CHEEUP_EXE -c"* ]]; then
        $CHEEUP_EXE -c "$CHEERUP_LAST_COMMAND"
    fi
}
"""
        % (command)
    )


def show_history() -> None:
    """Show history."""
    print(f"History file: {historyfile}")
    pprint(get_history())


def main() -> None:
    """Main function."""

    parser = argparse.ArgumentParser(
        prog="cheerup", description="Cheer on your command-line expertise!"
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="interactive mode"
    )
    parser.add_argument("-c", "--command", help="compliment the command")
    parser.add_argument(
        "-l",
        "--lang",
        default=os.environ.get("LANG"),
        help="locale, default is LANG environment variable.",
    )
    parser.add_argument("--zsh", action="store_true", help="show zsh script")
    parser.add_argument("--history", action="store_true", help="show history")
    args = parser.parse_args()

    if args.interactive:
        interactive(args.lang)
    elif args.command:
        chat(args.command, args.lang)
    elif args.command == "":
        sys.exit(0)  # When it is called by cheerup.zsh, it is called with empty string.
    elif args.zsh:
        show_zsh_script()
    elif args.history:
        show_history()
    else:
        parser.print_help()

    sys.exit(0)
