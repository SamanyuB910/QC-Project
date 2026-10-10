"""Five Tests, Priced -- plain-text output and accessible figures.

Every result is a readable table (screen-reader friendly: words like yes/no, never colour or symbols alone).
Every figure is preceded by a text description and its numbers are printed as a table; figures use the
Okabe-Ito colour-blind-safe palette plus distinct markers, line styles and direct labels."""

OKABE_ITO = {"blue": "#0072B2", "orange": "#E69F00", "green": "#009E73", "vermillion": "#D55E00",
             "purple": "#CC79A7", "sky": "#56B4E9", "black": "#000000"}


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


def describe(text):
    print("  Figure description: " + text, flush=True)


def price_ladder_figure(front, optima):
    """front: [(price, auc, short label)] cheapest-first staircase; optima: [(price, auc, 'mu=..')]."""
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    xs = [p for p, _, _ in front] + [330]
    ys = [a for _, a, _ in front] + [front[-1][1]]
    ax.step(xs, ys, where="post", color=OKABE_ITO["blue"], linewidth=2, label="best AUC reachable at this price")
    ax.plot([p for p, _, _ in front], [a for _, a, _ in front], "o", color=OKABE_ITO["blue"], markersize=6)
    last = -1e9
    for p, a, lab in front:
        if p - last < 40:      # cheap panels sit close together; label the cluster once
            continue
        right = p > 60     # keep labels inside the axes and off the staircase: label to the left of the point
        ax.annotate(lab, (p, a), textcoords="offset points", xytext=(-6, 7) if right else (10, 10),
                    ha="right" if right else "left", fontsize=8)
        last = p
    ax.plot([p for p, _, _ in optima], [a for _, a, _ in optima], "D", color=OKABE_ITO["vermillion"],
            markersize=8, fillstyle="none", markeredgewidth=2, label="QUBO optimum at each price weight")
    ax.set_xlabel("price of the five-test panel (1992 CAD, Turney fee schedule)")
    ax.set_ylabel("cross-validated AUC")
    ax.set_title("What each extra dollar buys: five-test heart-disease panels")
    ax.set_xlim(0, 330)
    ax.set_ylim(min(ys) - 0.008, max(ys) + 0.012)
    ax.grid(alpha=0.3)
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    plt.show()
    plt.close("all")


def recovery_figure(shots_grid, curves, this_run=None):
    """curves: {label: [probability per shots value]}; drawn with distinct colour, marker and line style."""
    import matplotlib.pyplot as plt
    styles = [(OKABE_ITO["blue"], "o", "-"), (OKABE_ITO["orange"], "s", "--"), (OKABE_ITO["green"], "^", ":"),
              (OKABE_ITO["purple"], "D", "-.")]
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    for (lab, ys), (col, mk, ls) in zip(curves.items(), styles):
        ax.plot(shots_grid, [100 * y for y in ys], color=col, marker=mk, linestyle=ls, linewidth=2, label=lab)
    if this_run is not None:
        ax.axvline(this_run, color=OKABE_ITO["black"], linewidth=1, linestyle="--")
        ax.annotate("this run", (this_run, 2), textcoords="offset points", xytext=(4, 0), fontsize=8)
    ax.set_xscale("log")
    ax.set_xlabel("raw shots per circuit (log scale; about 22% of shots have exactly five tests)")
    ax.set_ylabel("chance one job finds every optimal panel (%)")
    ax.set_ylim(-2, 102)
    ax.set_title("Exact prediction: ideal circuit vs samplers without correlations")
    ax.grid(alpha=0.3)
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    plt.show()
    plt.close("all")
