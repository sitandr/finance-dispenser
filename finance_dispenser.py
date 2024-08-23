import argparse
from dataclasses import dataclass
import csv
from fractions import Fraction
from itertools import groupby
from termcolor import colored
import yaml
# pylint: disable-next=wildcard-import
from utils import *

parser = argparse.ArgumentParser(
    description="A program that helps dividing the expenses for a group of people.")
parser.add_argument("prefix", default="real_data/", nargs="?",
            help="""Prefix to be added to the names of files.
            For example: \"data/my_\" -> data/my_items.csv, data/my_rules.yml""")
parser.add_argument("--round", type=int, default=2, help="Number of digits to round the numbers")
parser.add_argument("--keep_negative", action="store_false", dest = "resolve_negative",
                    help="If enabled, allows negative values")

args = parser.parse_args()
file = args.prefix + "items.csv"

with open(args.prefix + "rules.yml", encoding="utf-8") as f:
    rules = yaml.safe_load(f)

groups = rules['groups']

groups = {n: set(g) for (n, g) in groups.items()}
all_p = set.union(*groups.values())

def check_exists(v: str|set[str]|list[str]) -> None:
    '''Check if value is a valid set of people'''
    if isinstance(v, set):
        for s in v:
            assert s in all_p, "\"" + str(v) + "\" not in names list: " + str(all_p)
    elif isinstance(v, str):
        assert v in all_p, "\"" + str(v) + "\" not in names list: " + str(all_p)
    else:
        raise ValueError(str(v) + " is not a name or set of names")

@dataclass
class Transaction:
    '''Data class that describes single transaction'''
    from_: str|set[str]
    to_: str|set[str]
    name: str
    value: float
    frac: int|float|Fraction
    comment: str
    order: int

operations: list[Transaction] = []
balance: dict[str, list[float]] = {p: [] for p in all_p }

def pay(_from, _to, frac=1, comment="", order=0):
    '''Create transaction associated with this item'''
    just_pay(_from, _to, this['name'], this['price'], frac, comment, order)

def just_pay(_from, _to, name, value, frac=1, comment="", order=0):
    '''Create a transaction out of nothing with specified name'''
    check_exists(_from)
    check_exists(_to)

    assert isinstance(name, str), f"Transaction name: \"{name}\" must be string"
    assert isinstance(value, int|float|Fraction), f"Transaction sum: \"{value}\" must be number"
    assert isinstance(frac, int|float|Fraction), f"Transaction fraction \"{frac}\" must be number"
    assert isinstance(comment, str), f"Transaction name: \"{comment}\" must be string"
    assert isinstance(order, int|float|Fraction), f"Transaction fraction \"{order}\" must be number"

    if frac < 0 and args.resolve_negative:
        frac = -frac
        _from, _to = _to, _from

    if value < 0 and args.resolve_negative:
        value = -value
        _from, _to = _to, _from

    operations.append(Transaction(_from, _to, name, float(value), frac, comment, order))

if "preamble" in rules:
    # pylint: disable-next=exec-used
    exec(rules['preamble'], {"all": all_p, "Frac": Fraction, "just_pay": just_pay} | groups)

def comment_strip(csv_file):
    '''Returns a generator stripping all comments'''
    for row in csv_file:
        raw = row.split('#')[0].strip()
        if raw:
            yield raw

with open(file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(comment_strip(f), delimiter=";")
    for item in reader:
        item = {n: convert_value(v) for (n, v) in item.items()}

        this = item
        var = {} # local variables

        # pylint: disable-next=exec-used
        exec(rules['rules'],
             item | {"all": all_p, "pay": pay, "Frac": Fraction, "just_pay": just_pay, "var": var}
             | groups)

operations.sort(key=lambda op:
    (op.order,
     "".join(op.from_),
     op.comment,
     "".join(op.to_)))

print()
print()

for (k, transact) in groupby(operations, key=lambda op: (op.from_, op.to_, op.frac, op.comment)):
    transact = list(transact)

    names = [colored(t.name, "cyan") + colored(f"({display_float(t.value)})", "yellow")
             for t in transact]
    money = sum((t.value for t in transact)) * k[2]

    from_cost = float(money / check_len(k[0]))
    to_cost = float(money / check_len(k[1]))

    for p in into_iterable(k[0]):
        balance[p].append(-from_cost)

    for p in into_iterable(k[1]):
        balance[p].append(to_cost)

    from_cost = display_float(round(from_cost, args.round))
    to_cost = display_float(round(to_cost, args.round))

    print(colored(group_display(k[0]), "magenta"), colored("\t->", "magenta"),
          check_len(k[0]), "×", colored(f"{from_cost:7}", "red"), end=" ")
    inner = f"{f"(x{str(round_any(k[2], 2 + max(0, args.round)))})" if k[2] != 1 else "":-^15}"
    print(colored("\t--", "magenta")
          + colored(inner, "light_cyan") + colored("->\t", "magenta"), end=" ")
    print(check_len(k[1]), "×", colored(f"{to_cost:7}", "yellow"),
          colored("\t->", "magenta"), colored(group_display(k[1]), "green"), end=": \t")
    print(f"{(", ".join(names)):36}", end="")
    if k[3] != "":
        print(colored("\t# " + k[3], "dark_grey"), end="")
    print()

print()

for p in sorted(balance):
    print(f"{p:10}", end=": \t")
    print(" ".join(
        (f"{balance_color(f"{display_float(round(b, args.round)):+}", b)
            .replace("+", "+ ").replace("-", "- "):9}"
         for b in balance[p])), end="\n\t\t")
    print("=", balance_color(round(sum(balance[p]), args.round)))
    print()
