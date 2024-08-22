import csv
import yaml
from fractions import Fraction
from itertools import groupby
from dataclasses import dataclass
from utils import *
from termcolor import colored

file = "real_data/items.csv"

rules = yaml.safe_load(open("real_data/rules.yml", encoding="utf-8"))

groups = rules['groups']

groups = {n: set(g) for (n, g) in groups.items()}
all = set.union(*groups.values())

def check_exists(v: str|set[str]|list[str]) -> None:
    if type(v) == set:
        for s in v:
            assert s in all, "\"" + str(v) + "\" not in names list: " + str(all)
    elif type(v) == str:
        assert v in all, "\"" + str(v) + "\" not in names list: " + str(all)
    else:
        raise ValueError(str(v) + " is not a name or set of names")

operations = []
balance: dict[str, list[float]] = {p: [] for p in all }


@dataclass
class Transaction:
    from_: str|set[str]
    to_: str|set[str]
    item: dict
    frac: int|float|Fraction
    comment: str
    order: int

def pay(_from, _to, frac=1, comment="", order=0):
    check_exists(_from)
    check_exists(_to)
    operations.append(Transaction(_from, _to, this, frac, comment, order))

with open(file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for item in reader:
        item = {n: convert_value(v) for (n, v) in item.items()}
        global this
        this = item

        exec(rules['rules'], item | {"all": all, "pay": pay, "Frac": Fraction} | groups)

operations.sort(key=lambda op: (op.comment, hash(next(iter(into_iterable(op.from_)))), hash(next(iter(into_iterable(op.to_))))))
operations.sort(key=lambda op: op.order)

print()
print()

for (k, transact) in groupby(operations, key=lambda op: (op.from_, op.to_, op.frac, op.comment)):
    transact = list(transact)

    names = [colored(t.item['name'], "cyan") + colored(f"({t.item['price']})", "yellow") for t in transact]
    money = sum((t.item['price'] for t in transact)) * k[2]
    
    from_cost = round(float(money / check_len(k[0])), 2)
    to_cost = round(float(money / check_len(k[1])), 2)
    
    for p in into_iterable(k[0]):
        balance[p].append(-from_cost)
    
    for p in into_iterable(k[1]):
        balance[p].append(to_cost)

    print(colored(group_display(k[0]), "magenta"), colored("\t->", "magenta"), check_len(k[0]), "×", colored(f"{from_cost:7}", "red"), end=" ")
    inner = "{:-^15}".format(f"(x{str(round_any(k[2], 2))})" if k[2] != 1 else "")
    print(colored("\t--", "magenta") + colored(inner, "light_cyan") + colored("->\t", "magenta"), end=" ")
    print(check_len(k[1]), "×", colored(to_cost, "yellow"), colored("\t->", "magenta"), colored(group_display(k[1]), "green"), end=": \t")
    print("{:36}".format(", ".join(names)), end="")
    if k[3] != "":
        print(colored("\t# " + k[3], "dark_grey"), end="")
    print()

print()

for p in sorted(balance):
    print(f"{p:10}", end=": \t")
    print(" ".join((f"{balance_color(f"{b:+}", b).replace("+", "+ ").replace("-", "- "):9}" for b in balance[p])), end="\n\t\t")
    print("=", balance_color(round(sum(balance[p]), 2)))
    print()