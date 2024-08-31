This is a small cli app I made for my hikes to split the expenses with friends (see also my [another hike dispenser project](https://github.com/sitandr/hike-dispenser) for proper distribution of mass, volumes and other things). Of course, there are already apps for this, but they are pretty bad at handling complex situations, so here it is.

This is what the output looks like:

![Example output](https://github.com/user-attachments/assets/b6bba828-7cd2-46ec-a112-4c17876782c4)

## Example

Let's start with example of what I can call a simplified "complex situation":

Imagine you and your friends decided to throw a party. There was **Bob**, who immediately decided to buy a few pizzas. It turned out one of them was a pineapple pizza (because Bob loves them), so some friends refused to eat it.

Then **Eve** buys ice-cream, but it turns out it contains nuts that some of you (let them be **Tom** and **Alice**) are allergic to. So **Tom** buys ice-cream for himself and **Alice**, by the way he grabs a bottle of lemonade for everyone.

After that **Eve** asks her friend, **Evan**, who doesn't participate in the party at all, to bring a package of cookies. But everyone if already fed up, so the package is left half full. **Eve** decides to take them home.

I could continue the story for a much longer time, but let's stop at this.

Sounds like a headache to sum up using pen & paper or dragging cells in Excel? It certainly is. I forgot to mention that everyone wants a clear visual computation to be sure you don't defraud them.

Let's start with collecting data and put it into basic CSV format (with optional comments). I came up with this:

![Example CSV](https://github.com/user-attachments/assets/1b7f0a3f-0f26-4843-8a40-7aa256b601c6)

Note the knowledge that is not present in this file: consumption groups of people, meaning of tags and columns and the whole logic of payments.

So we will need some other file, describing _what to do with this data_. We will use human-readable `yaml` format for that. Let's start with describing our groups:

```yaml
groups:
  main: # maun party group
    - Bob
    - Tom
    - Alice
    - Eve
    - Jake

  nut_allergic:
    - Tom
    - Alice

  pineappleaters:
    - Alice
    - Bob
    - Jake

  others:
    - Evan # didn't even participate in the party
```

Now let's write the rule to work with data and payments. Code will be written on python (why bother with smth else?). I will assume you know python well, so here is the code:

```py
rules: |
  # code is simple and repetitive for demonstration purposes
  # in your code you can do anything you wish
  match tag: # cases of possible `tag`s
    case None:
      if to == None:
        # simple case: everyone pays to buyer
        # using external function:
        # pay(from, to, fraction=1, comment="", order=0)
        pay(main, buyer)
      else:
        # a single person pays to buyer
        # order=10 means this transaction will go in the end
        pay(to, buyer, order=10)
    case "P":
      pay(pineappleaters, buyer, comment="Pineapple product")
    case "N":
      pay(main - nut_allergic, buyer, comment="Nut product") # everyone pays except nut-allergic
    case _:
      raise ValueError(f"Wrong tag: {tag}")

  if taken_by != None:
    # someone took this thing, so they should pay
    pay(taken_by, main, left_ratio, comment="Taken home")
```

This is enough to generate the output:

![Example output](https://github.com/user-attachments/assets/b6bba828-7cd2-46ec-a112-4c17876782c4)

Actually, there is also an option to directly create payments and an option to add arbitrary code before applying rules to the main columns. 

With this we can make the code a bit more readable by removing the last line of csv (about debt) and adding to the `yml`:

```yml
preamble: |
  just_pay("Bob", "Jake", "Lost bet", value=50, comment="Bob lost a bet to Jake")
```

## How does it work?

Short answer will disappoint you: `exec`. This means _launching arbitrary rules_ may be extremely **dangerous**. Note this in case you would decide to make the web-server out of this thing or _just run the code of other users_ (please look at code first at least!).

However, that gives an _unlimited power_ for paying rules, and putting them in `yml` files makes things compact and easily switchable.

## Reference

Available variables at execution:

- _(only for `rules`, not `preamble`)_ Csv fields of current row as variables with the same name
- All payment groups (represented by sets) as variables with the same name
- `all_p` set that has every person represented in `groups`.
- `fractions.Fraction` as `Frac` to make better use of fractional numbers
- A dictionary named `var` that is shared among all executions for storing variables. Initially empty.
- _(only for `rules`, not `preamble`)_ `pay` function
- `just_pay` function

Order of rules execution is guaranteed to be in order they are in csv (though I wouldn't recommend to rely on it).

Signatures:

```
pay(_from, _to, frac=1, comment="", order=0)

Creates a transaction from _from to _to with multiplier `frac` and comment. The transactions are ordered by `order`.

Name and price is taken from `name` and `price` corresponding csv fields.
```

```
just_pay(_from, _to, name, value, frac=1, comment="", order=0)

Creates a transaction with fields similar to pay, but name and value are set manually.
```

