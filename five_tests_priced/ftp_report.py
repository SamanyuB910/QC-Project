"""Five Tests, Priced -- plain-text output. Every result is a readable table (screen-reader friendly: words like
yes/no instead of colour or symbols); figures, when shown, are preceded by a text description and followed by
the same numbers as a table."""


def section(title):
    print("\n" + title)
    print("-" * len(title), flush=True)


def table(headers, rows, note=None):
    cells = [[str(h) for h in headers]] + [[str(c) for c in r] for r in rows]
    widths = [max(len(r[i]) for r in cells) for i in range(len(headers))]
    line = lambda r: "  " + " | ".join(c.ljust(w) for c, w in zip(r, widths))  # noqa: E731
    print(line(cells[0]))
    print("  " + "-+-".join("-" * w for w in widths))
    for r in cells[1:]:
        print(line(r))
    if note:
        print("  " + note)
    print(flush=True)


def panel(names, maxlen=60):
    s = ", ".join(names)
    return s if len(s) <= maxlen else s[: maxlen - 3] + "..."


def money(x):
    return f"${x:,.2f}"


def pct(x, nd=0):
    return f"{100 * x:.{nd}f}%"


def yesno(b):
    return "yes" if b else "no"
