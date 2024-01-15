from enum import Enum


class TerminalColors(Enum):
    Red = "\033[91m"
    Green = "\033[92m"
    Blue = "\033[94m"
    Cyan = "\033[96m"
    White = "\033[97m"
    Yellow = "\033[93m"
    Magenta = "\033[95m"
    Grey = "\033[90m"
    Black = "\033[90m"
    Default = "\033[99m"

    # special colors
    Warning = "\033[93m"
    Error = "\033[91m"
    Success = "\033[92m"


class TerminalStyling(Enum):
    Header = "\033[95m"
    EndCharacter = "\033[0m"
    Bold = "\033[1m"
    Underline = "\033[4m"


__all__ = ["TerminalColors", "TerminalStyling"]
