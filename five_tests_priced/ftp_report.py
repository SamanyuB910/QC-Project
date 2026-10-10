"""Five Tests, Priced -- printing helpers: section titles, plain-text tables, number formats, and the two figures.

Accessibility rules followed by every output:
  * results are plain-text tables a screen reader can read, using words such as yes/no, never colour alone;
  * every figure is preceded by a text description, and its numbers are also printed as a table;
  * figures use the Okabe-Ito colour-blind-safe palette plus distinct markers, line styles and direct labels.
"""

# Okabe-Ito colour-blind-safe palette.
OKABE_ITO = {"blue": "#0072B2", "orange": "#E69F00", "green": "#009E73", "vermillion": "#D55E00",
             "purple": "#CC79A7", "sky": "#56B4E9", "black": "#000000"}


# -----------------------------------------------------------------------------------------------------------------
# Text output
# -----------------------------------------------------------------------------------------------------------------
def section(title):
    """Print a section title, underlined."""
    print("\n" + title)
    print("-" * len(title), flush=True)


def table(headers, rows, note=None):
    """Print rows as a plain-text table with aligned columns, then an optional note line."""
    cells = [[str(h) for h in headers]] + [[str(c) for c in row] for row in rows]
    widths = [max(len(row[i]) for row in cells) for i in range(len(headers))]

    def format_row(row):
        return "  " + " | ".join(cell.ljust(width) for cell, width in zip(row, widths))

    print(format_row(cells[0]))
    print("  " + "-+-".join("-" * width for width in widths))
    for row in cells[1:]:
        print(format_row(row))
    if note:
        print("  " + note)
    print(flush=True)


def panel(names, maxlen=60):
    """Test names joined by commas, shortened with '...' if longer than maxlen characters."""
    text = ", ".join(names)
    return text if len(text) <= maxlen else text[: maxlen - 3] + "..."


def money(x):
    """Dollar amount, e.g. 9.2 -> '$9.20'."""
    return f"${x:,.2f}"


def pct(x, nd=0):
    """Probability as a percentage, e.g. 0.985 -> '98%' (nd = number of decimals)."""
    return f"{100 * x:.{nd}f}%"


def yesno(b):
    return "yes" if b else "no"


def describe(text):
    """Text description printed before a figure, for readers who cannot see it."""
    print("  Figure description: " + text, flush=True)


# -----------------------------------------------------------------------------------------------------------------
# Figures (matplotlib is imported only when a figure is drawn)
# -----------------------------------------------------------------------------------------------------------------
def price_ladder_figure(front, optima):
    """Staircase of the best cross-validated AUC reachable at each panel price.

    front:  [(price, AUC, short label)], cheapest first
    optima: [(price, AUC, 'mu=..')], the exact optimum at each price weight, drawn as diamonds
    """
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    xs = [price for price, _, _ in front] + [330]          # extend the last step to the right edge
    ys = [auc for _, auc, _ in front] + [front[-1][1]]
    ax.step(xs, ys, where="post", color=OKABE_ITO["blue"], linewidth=2, label="best AUC reachable at this price")
    ax.plot([price for price, _, _ in front], [auc for _, auc, _ in front], "o", color=OKABE_ITO["blue"],
            markersize=6)
    last_labelled_price = -1e9
    for price, auc, label in front:
        if price - last_labelled_price < 40:     # cheap panels sit close together; label the cluster once
            continue
        right_side = price > 60      # keep labels inside the axes and off the staircase: label left of the point
        ax.annotate(label, (price, auc), textcoords="offset points", xytext=(-6, 7) if right_side else (10, 10),
                    ha="right" if right_side else "left", fontsize=8)
        last_labelled_price = price
    ax.plot([price for price, _, _ in optima], [auc for _, auc, _ in optima], "D", color=OKABE_ITO["vermillion"],
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
    """Chance that one job finds every optimal panel, against shots per circuit (log scale).

    curves: {label: [probability for each value in shots_grid]}; each curve gets its own colour, marker and
    line style. this_run: shots used in this Run, marked with a dashed vertical line.
    """
    import matplotlib.pyplot as plt
    styles = [(OKABE_ITO["blue"], "o", "-"), (OKABE_ITO["orange"], "s", "--"), (OKABE_ITO["green"], "^", ":"),
              (OKABE_ITO["purple"], "D", "-.")]
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    for (label, probabilities), (colour, marker, line_style) in zip(curves.items(), styles):
        ax.plot(shots_grid, [100 * p for p in probabilities], color=colour, marker=marker, linestyle=line_style,
                linewidth=2, label=label)
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
