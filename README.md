This is a small cli app I made for my hikes to split the expenses with friends (see also my [another hike dispenser project](https://github.com/sitandr/hike-dispenser) for proper distribution of mass, volumes and other things). Of course, there are already apps for this, but they are pretty bad at handling complex situations, so here it is.

This is what the output looks like:

[]()

## Example

Let's start with example of what I can call a simplified "complex situation":

Imagine you and your friends decided to throw a party. There was **Bob**, who immediately decided to buy a few pizzas. It turned out one of them was a pineapple pizza (because Bob loves them), so some friends refused to eat it.

Then **Eve** buys ice-cream, but it turns out it contains nuts that some of you (let them be **Tom** and **Alice**) are allergic to. So **Tom** buys ice-cream for himself and **Alice**, by the way he grabs a bottle of lemonade for everyone.

After that **Eve** asks her friend, **Evan**, who doesn't participate in the party at all, to bring a package of cookies. But everyone if already fed up, so the package is left half full. **Eve** decides to take them home.

I could continue the story for a much longer time, but let's stop at this.

Sounds like a headache to sum up using pen & paper or dragging cells in Excel? It certainly is. I forgot to mention that everyone wants a clear visual computation to be sure you don't defraud them.

Let's start with collecting data and put it into basic CSV format (with optional comments). I came up with this:

<style>
.mtk1 {color: #d4d4d4;}
.mtk5 {color: #569cd6;}
.mtk15 {color: #dcdcaa;}
.mtk4 {color: #6a9955;}
.mtk11 {color: #ce9178;}
.mtk9 {color: #9cdcfe;}
.mtk6 {color: #b5cea8;}
</style>

<div class="view-lines monaco-mouse-cursor-text" role="presentation" aria-hidden="true" data-mprt="8" style="font-family: Consolas, &quot;Courier New&quot;, monospace; font-weight: normal; font-size: 14px; font-feature-settings: &quot;liga&quot; 0, &quot;calt&quot; 0; font-variation-settings: normal; line-height: 19px; letter-spacing: 0px; background: #111; padding: 1em"><div style="top:33px;height:19px;" class="view-line"><span><span class="mtk1">name;</span><span class="mtk5">price;</span><span class="mtk15">buyer;</span><span class="mtk4">tag;</span><span class="mtk11">to;</span><span class="mtk9">taken_by;</span><span class="mtk6">left_ratio</span></span></div><div style="top:52px;height:19px;" class="view-line"><span><span></span></span></div><div style="top:71px;height:19px;" class="view-line"><span><span class="mtk4">#&nbsp;(empty&nbsp;columns&nbsp;in&nbsp;the&nbsp;end&nbsp;may&nbsp;be&nbsp;omitted)</span></span></div><div style="top:90px;height:19px;" class="view-line"><span><span class="mtk4">#&nbsp;Bob&nbsp;bought&nbsp;pizza&nbsp;for&nbsp;everyone&nbsp;that&nbsp;cost&nbsp;100$</span></span></div><div style="top:109px;height:19px;" class="view-line"><span><span class="mtk4">#&nbsp;That&nbsp;means&nbsp;everyone&nbsp;should&nbsp;pay&nbsp;to&nbsp;Bob</span></span></div><div style="top:128px;height:19px;" class="view-line"><span><span class="mtk1">pizza_pepperoni;</span><span class="mtk5">40;</span><span class="mtk15">Bob</span></span></div><div style="top:147px;height:19px;" class="view-line"><span><span class="mtk1">pizza_margherita;</span><span class="mtk5">60;</span><span class="mtk15">Bob</span></span></div><div style="top:166px;height:19px;" class="view-line"><span><span></span></span></div><div style="top:185px;height:19px;" class="view-line"><span><span class="mtk4">#&nbsp;Then&nbsp;Bob&nbsp;bought&nbsp;some...&nbsp;pinapple&nbsp;pizza.</span></span></div><div style="top:204px;height:19px;" class="view-line"><span><span class="mtk4">#&nbsp;Many&nbsp;didn't&nbsp;like&nbsp;it&nbsp;and&nbsp;didn't&nbsp;eat&nbsp;this&nbsp;pizza.</span></span></div><div style="top:223px;height:19px;" class="view-line"><span><span class="mtk4">#&nbsp;P&nbsp;means&nbsp;"Pineapple"&nbsp;tag</span></span></div><div style="top:242px;height:19px;" class="view-line"><span><span class="mtk1">pineapple_pizza;</span><span class="mtk5">50;</span><span class="mtk15">Bob;</span><span class="mtk4">P</span></span></div><div style="top:261px;height:19px;" class="view-line"><span><span></span></span></div><div style="top:280px;height:19px;" class="view-line"><span><span class="mtk4">#&nbsp;Tom&nbsp;brought&nbsp;some&nbsp;lemonade</span></span></div><div style="top:299px;height:19px;" class="view-line"><span><span class="mtk1">lemonade;</span><span class="mtk5">20;</span><span class="mtk15">Tom</span></span></div><div style="top:318px;height:19px;" class="view-line"><span><span></span></span></div><div style="top:337px;height:19px;" class="view-line"><span><span class="mtk4">#&nbsp;Eve&nbsp;bought&nbsp;big&nbsp;ice-cream&nbsp;with&nbsp;nuts&nbsp;to&nbsp;everyone</span></span></div><div style="top:356px;height:19px;" class="view-line"><span><span class="mtk4">#&nbsp;but&nbsp;Tom&nbsp;and&nbsp;Alice&nbsp;are&nbsp;allergic&nbsp;to&nbsp;nuts&nbsp;(N)!</span></span></div><div style="top:375px;height:19px;" class="view-line"><span><span class="mtk1">nuts-ice-cream;</span><span class="mtk5">90;</span><span class="mtk15">Eve;</span><span class="mtk4">N</span></span></div><div style="top:394px;height:19px;" class="view-line"><span><span></span></span></div><div style="top:413px;height:19px;" class="view-line"><span><span class="mtk4">#&nbsp;Tom&nbsp;bought&nbsp;some&nbsp;ice-cream&nbsp;for&nbsp;himself&nbsp;and&nbsp;Alice</span></span></div><div style="top:432px;height:19px;" class="view-line"><span><span class="mtk1">ice-cream;</span><span class="mtk5">70;</span><span class="mtk15">Bob;</span><span class="mtk4">;</span><span class="mtk11">Alice</span></span></div><div style="top:451px;height:19px;" class="view-line"><span><span></span></span></div><div style="top:470px;height:19px;" class="view-line"><span><span class="mtk4">#&nbsp;Eve&nbsp;asked&nbsp;her&nbsp;friend&nbsp;Evan&nbsp;to&nbsp;bring&nbsp;some&nbsp;cookies</span></span></div><div style="top:489px;height:19px;" class="view-line"><span><span class="mtk4">#&nbsp;That&nbsp;friend&nbsp;didn't&nbsp;participate&nbsp;in&nbsp;party&nbsp;at&nbsp;all</span></span></div><div style="top:508px;height:19px;" class="view-line"><span><span class="mtk4">#&nbsp;However,&nbsp;cookies&nbsp;were&nbsp;not&nbsp;very&nbsp;tasty</span></span></div><div style="top:527px;height:19px;" class="view-line"><span><span class="mtk4">#&nbsp;So&nbsp;by&nbsp;the&nbsp;end&nbsp;of&nbsp;the&nbsp;party&nbsp;there&nbsp;was&nbsp;still&nbsp;half&nbsp;</span><span class="mtk4">of&nbsp;them&nbsp;left</span></span></div><div style="top:546px;height:19px;" class="view-line"><span><span class="mtk4">#&nbsp;Eve&nbsp;took&nbsp;the&nbsp;remaining&nbsp;cookies&nbsp;home</span></span></div><div style="top:565px;height:19px;" class="view-line"><span><span class="mtk1">cookies;</span><span class="mtk5">30;</span><span class="mtk15">Evan;</span><span class="mtk4">;</span><span class="mtk11">;</span><span class="mtk9">Eve;</span><span class="mtk6">1/2</span></span></div><div style="top:584px;height:19px;" class="view-line"><span><span></span></span></div><div style="top:603px;height:19px;" class="view-line"><span><span class="mtk4">#&nbsp;Bob&nbsp;lost&nbsp;a&nbsp;bet&nbsp;to&nbsp;Jake</span></span></div><div style="top:622px;height:19px;" class="view-line"><span><span class="mtk4">#&nbsp;Usually&nbsp;person&nbsp;that&nbsp;receives&nbsp;pays&nbsp;to&nbsp;buyer</span></span></div><div style="top:641px;height:19px;" class="view-line"><span><span class="mtk4">#&nbsp;In&nbsp;our&nbsp;case&nbsp;this&nbsp;is&nbsp;reversed</span></span></div><div style="top:660px;height:19px;" class="view-line"><span><span class="mtk4">#&nbsp;So&nbsp;we&nbsp;can&nbsp;for&nbsp;demonstration&nbsp;purposes&nbsp;put&nbsp;minus&nbsp;s</span><span class="mtk4">ign</span></span></div><div style="top:679px;height:19px;" class="view-line"><span><span class="mtk1">bet;</span><span class="mtk5">-50;</span><span class="mtk15">Bob;</span><span class="mtk4">;</span><span class="mtk11">Jake</span></span></div></div>

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

[]()

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

