import subprocess
import sys
from typing import List


def execute_command_and_print(command: List[str]) -> None:
    print(execute_command(command))


def execute_command(command: List[str]) -> str:
    try:
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        output = result.stdout
        return output
    except subprocess.CalledProcessError as error:
        output = error.stdout
        error_output = error.stderr

        print(f"Command '{command}' failed with exit code {error.returncode}.")
        print("Output:\n", output)
        print("Error output:\n", error_output)
        sys.exit(1)


__all__ = [
    "execute_command",
    "execute_command_and_print",
]
