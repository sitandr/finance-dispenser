from fractions import Fraction
from termcolor import colored


def convert_value(s: str | None) -> str | int | float | Fraction | None:
    if s == None or len(s) == 0:
        return None

    if s.isdigit():
        return int(s)

    if s.replace(".", "", 1).isdigit():
        return float(s)

    if s.replace("/", "", 1).isdigit():
        return Fraction(s)

    return s


def check_len(s: str | list[str] | set[str]):
    if type(s) == str:
        return 1
    if len(s) == 0:
        return 1
    return len(s)


def group_display(s: str | list[str] | set[str]) -> str:
    if type(s) == set or type(s) == list:
        return str(", ".join(sorted(s)))
    return str(s)


def into_iterable(s: str | list[str] | set[str]):
    if type(s) == str:
        return [s]
    return s


def balance_color(s, n=None) -> str:
    if n == None:
        n = s
    if n > 0:
        return colored(s, "yellow")
    if n < 0:
        return colored(s, "red")
    return colored(s, "white")


def round_any(n: int | float | Fraction, digits=2):
    if type(n) == float:
        return round(n, digits)
    if type(n) == Fraction:
        if n.denominator > 10:
            return round(float(n), digits)
    return n


def display_float(n: float) -> int | float:
    if n % 1 == 0:
        return int(n)
    return n
