from nwon_baseline.typings import TerminalColors, TerminalStyling


def print_red(text: str):
    print_color(text, TerminalColors.Red)


def print_green(text: str):
    print_color(text, TerminalColors.Green)


def print_blue(text: str):
    print_color(text, TerminalColors.Blue)


def print_cyan(text: str):
    print_color(text, TerminalColors.Cyan)


def print_white(text: str):
    print_color(text, TerminalColors.White)


def print_yellow(text: str):
    print_color(text, TerminalColors.Yellow)


def print_magenta(text: str):
    print_color(text, TerminalColors.Magenta)


def print_grey(text: str):
    print_color(text, TerminalColors.Grey)


def print_black(text: str):
    print_color(text, TerminalColors.Black)


def print_default(text: str):
    print_color(text, TerminalColors.Default)


def print_warning(text: str):
    print_color(text, TerminalColors.Warning)


def print_error(text: str):
    print_color(text, TerminalColors.Error)


def print_success(text: str):
    print_color(text, TerminalColors.Success)


def print_color(text: str, color: "TerminalColors") -> None:
    print(f"{color.value}{text}{TerminalStyling.EndCharacter.value}")
