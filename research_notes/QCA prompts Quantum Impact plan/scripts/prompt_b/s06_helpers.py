"""Turney cost polynomial over all 2^13 states (shared-procedure discounts as OR terms)."""
import numpy as np
from common import FEATURES, EXPENSE, GROUPS, BITS


def cost_vector():
    B = BITS.astype(float)
    d = np.array([EXPENSE[f][1] for f in FEATURES])
    fi = {f: i for i, f in enumerate(FEATURES)}
    c = B @ d
    for g, mem in GROUPS.items():
        idx = [fi[f] for f in mem]
        shared = EXPENSE[mem[0]][0] - EXPENSE[mem[0]][1]
        c = c + shared * (1 - np.prod(1 - B[:, idx], axis=1))
    return c
