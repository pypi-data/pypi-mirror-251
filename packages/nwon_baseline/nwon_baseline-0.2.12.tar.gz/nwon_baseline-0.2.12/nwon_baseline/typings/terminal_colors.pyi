from enum import Enum

class TerminalColors(Enum):
    Red: str
    Green: str
    Blue: str
    Cyan: str
    White: str
    Yellow: str
    Magenta: str
    Grey: str
    Black: str
    Default: str
    Warning: str
    Error: str
    Success: str

class TerminalStyling(Enum):
    Header: str
    EndCharacter: str
    Bold: str
    Underline: str
