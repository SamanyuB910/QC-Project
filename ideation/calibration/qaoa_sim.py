import numpy as np
def lr_qaoa(E, n, p, dg, db):
    En = (E - E.mean()) / (np.abs(E - E.mean()).max())
    psi = np.full(2**n, 2**(-n/2), dtype=complex)
    for k in range(p):
        g = (k+1)/p * dg; b = (1 - k/p) * db
        psi *= np.exp(-1j * g * En)
        # mixer exp(-i b X) on each qubit
        c, s = np.cos(b), 1j*np.sin(b)  # exp(+i b X): |+> is ground state of -X, anneal to MIN of E
        psi = psi.reshape([2]*n)
        for q in range(n):
            psi = np.moveaxis(psi, q, 0)
            a0, a1 = psi[0].copy(), psi[1].copy()
            psi[0] = c*a0 + s*a1; psi[1] = s*a0 + c*a1
            psi = np.moveaxis(psi, 0, q)
        psi = psi.reshape(-1)
    return np.abs(psi)**2

