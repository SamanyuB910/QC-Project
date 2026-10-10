# Building an interactive, accessible quantum-education tool on Qollab (Pyodide + Qiskit): feasibility and stack

Current as of 2026-10-09, the day the build window opens at 19:00 ET.

**Labels.** "Confirmed" means a primary source says it, or I measured it myself. "Inferred" means it is my reasoning. Every bullet under Cited Findings is confirmed and carries its source. Every bullet under Inferences is inferred.

**Sources.** Qollab docs pages, read with WebFetch. Two official Qollab Team JS reference projects, whose source I read through Qollab's public file API in a browser:
- "QCFlows: Multi-file Example"
- "Quantum Hackathon Soundtrack"

Also: HTTP headers and the JS bundle of qollab.xyz, the GitHub API for the qollabxyz forks, PyPI JSON metadata, the Pyodide package list and changelog, and W3C/MDN/PhET/Desmos accessibility material.

**My own measurements.** I benchmarked stock **Pyodide 314.0.7** (Python 3.14.2, NumPy 2.4.6) in the pyodide.org console, running in Chromium 152 on Windows. This is the same Pyodide build Qollab loads, per Qollab's CSP header (see Q1). Qollab's own Qiskit wheel isn't publicly downloadable, so I benchmarked the NumPy `einsum` kernel that Qiskit's `BasicSimulator` uses, not Qiskit itself.

**Read-only.** I did not sign in, register, run, submit or publish anything on Qollab.

---

## Q1. What is the exact JS↔Python API on Qollab, how does the injected `backend` work, and are there working examples?

### Takeaway
A top-level `index.html` + `main.js` (+ optional `main.css`) makes a JS project.

**Calling Python from JS.** `main.js` imports your Python modules by dotted name, e.g. `import * as svc from 'pkg.module'`. It calls them with `fn.callPromising(...)` / `fn.callPromisingKwargs(...)` and converts results with `.toJs()`.

**The backend.** `backend` is a global holding the provider's real Qiskit backend object. Use `const job = await backend.run(circuit, {shots}); const result = await job.result();`.

**What the official reference projects do:**
- Pass only JSON strings across the boundary.
- Wait for the DOM to mount before touching it.
- Make one `backend.run` call from JS.
- End `main.js` with `await new Promise(() => {})` so remote IonQ backends stay reachable.

**Code that runs on every backend:**
- Use `job.result().get_counts()`, never IonQ's `job.get_counts()` shortcut.
- Use `BackendEstimatorV2`, not `BackendSamplerV2`, on IonQ.
- Transpile to a fixed basis without a backend.
- Pack everything into one job.

### Cited Findings

**Project structure and loading rules**
- A top-level `index.html` plus `main.js` makes a JS project, and output goes to the page and the console. A top-level `main.py` alone makes a Python project. Files in subfolders don't count. If both sets are present, the project runs as JS. — [Qollab docs: Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
- `index.html` is inserted into the body. `<html>`, `<head>` and `<body>` tags are stripped, `<script>` tags in `index.html` **do not run**, and `main.css` is the only stylesheet loaded. Other `.html`/`.css` files are ignored. — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
- JS imports of project files must start with `./` or `../`. The runtime tries the exact path, then `.js`/`.mjs`, then `index.js`/`index.mjs`. Other file types can't be imported, and **JS can't fetch project files**: read them in Python and pass the data to `main.js`. — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
- Python must open data files with plain string-literal paths relative to the root. Paths built with f-strings, `+` or `os.path.join` "aren't loaded and raise `OSError`". Binary files work. — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
  - The QCFlows README says the same: "Qollab preloads only files whose paths appear as plain strings in Python, so experiments.py lists each JSON file instead of scanning the folder." — [QCFlows: Multi-file Example](https://qollab.xyz/u/qollab/qcflows-multifile)

**Calling Python from JS**
- Import Python modules by dotted name, e.g. `import * as bell from 'quantum.bell'` for `quantum/bell.py`. Use named or `import * as` imports; a default import gives `undefined`. — [Qollab docs: JS / Qiskit projects](https://qollab.xyz/learn/docs/js-qiskit-projects)
- Call Python functions with `.callPromising(...)`, or `.callPromisingKwargs(...)` for keyword arguments, and convert results with `.toJs()`. Documented pattern: `(await bell.run_bell.callPromising(backend, 1000)).toJs()`. — [JS / Qiskit projects](https://qollab.xyz/learn/docs/js-qiskit-projects)
- On IonQ backends, a plain synchronous call such as `bell.run_bell(backend, 1000)` "fails with a `ConnectionError` that says XHR is not supported". — [JS / Qiskit projects](https://qollab.xyz/learn/docs/js-qiskit-projects)
- Qiskit can also be driven directly from JS:
  - Import from `qiskit`, e.g. `{ QuantumCircuit }`, or from submodules such as `qiskit.providers.jobstatus`.
  - Call constructors without `new`, e.g. `QuantumCircuit(2, 2)`.
  - Pass Python keyword arguments with `.callKwargs({...})`, e.g. `circuit.draw.callKwargs({ output: 'mpl' })`.
  - Return values are proxies; `.toJs()` converts them.
  - `run()` is async. Top-level `await` works, and the injected `setTimeout` returns an awaitable promise.
  - Poll `job.status()` against `JobStatus.DONE` / `JobStatus.ERROR`.

  — [JS / Qiskit projects](https://qollab.xyz/learn/docs/js-qiskit-projects)
- Circuit drawings in JS:
  1. Enable "Qiskit Visualizations" in the Libraries list.
  2. `circuit.draw.callKwargs({ output: 'mpl' })` returns a Matplotlib figure.
  3. `URL.createObjectURL(figure)` gives an `<img>` URL; the runtime converts the figure to SVG.

  — [JS / Qiskit projects](https://qollab.xyz/learn/docs/js-qiskit-projects)
- A Python dependency used only from JS must still be listed in `requirements.txt`. — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)

**Working example 1: QCFlows (Qollab Team, MIT, v1.1, Sep 29 2026)**

Structure: D3 front-end in `ui/*.js` modules, a Python package `qcflows/`, JSON examples in `data/experiments/`, and a `requirements.txt` that adds `qiskit_qasm3_import`. — [QCFlows project page](https://qollab.xyz/u/qollab/qcflows-multifile)

| What | Source |
|---|---|
| `ui/api.js` does `import * as service from 'qcflows.service'` and `await service.dispatch(method, path, JSON.stringify(payload))`, then `JSON.parse(String(raw))`. The README: "Only JSON strings cross the boundary, which avoids proxy conversion." | [QCFlows `ui/api.js`](https://api.qollab.xyz/api/project/id/01a0ebb2-b0ee-7799-9ad4-fe18e611ea44/versions/id/01a0ebd1-1556-7ced-a669-463a94094430/file?path=ui%2Fapi.js); [QCFlows README](https://qollab.xyz/u/qollab/qcflows-multifile) |
| D3 is loaded with `import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";` | [QCFlows `ui/graph.js`](https://api.qollab.xyz/api/project/id/01a0ebb2-b0ee-7799-9ad4-fe18e611ea44/versions/id/01a0ebd1-1556-7ced-a669-463a94094430/file?path=ui%2Fgraph.js) |
| `main.js` comments "Qollab may evaluate this module before index.html is mounted, so wait for it", and `boot()` re-polls `document.getElementById(...)` every 150 ms. | [QCFlows `main.js`](https://api.qollab.xyz/api/project/id/01a0ebb2-b0ee-7799-9ad4-fe18e611ea44/versions/id/01a0ebd1-1556-7ced-a669-463a94094430/file?path=main.js) |
| Sampling runs from JS: `const circuit = hardware.prepare_circuit(n, opsJson); const job = await backend.run(circuit, { shots: 1024 }); const result = await job.result(); JSON.parse(String(hardware.summarize(result, ...)))`. Comment: "Qollab's backend.run/result are async here, which remote backends (IonQ) need. Python only prepares the circuit and scores it." | [QCFlows `main.js`](https://api.qollab.xyz/api/project/id/01a0ebb2-b0ee-7799-9ad4-fe18e611ea44/versions/id/01a0ebd1-1556-7ced-a669-463a94094430/file?path=main.js) |
| `main.js` ends with `await new Promise(() => {});`. Comment: "Qollab routes remote backend requests (IonQ simulators and hardware) only while main.js is still running; once it returns, the run is 'Done'… Press Stop… to end the session." | [QCFlows `main.js`](https://api.qollab.xyz/api/project/id/01a0ebb2-b0ee-7799-9ad4-fe18e611ea44/versions/id/01a0ebd1-1556-7ced-a669-463a94094430/file?path=main.js) |
| `qcflows/hardware.py` transpiles with no backend and no network: `transpile(circuit, basis_gates=["h","x","y","z","s","sdg","t","tdg","sx","rx","ry","rz","cx","cz","swap","ccx"], optimization_level=0)`. It computes TVD versus `Statevector.from_instruction(circuit).probabilities_dict()`, and handles `result.get_counts()` returning a list. Its docstring: synchronous `backend.run(...).result()` from Python "works on the built-in simulator but fails on remote backends (IonQ)". | [QCFlows `hardware.py`](https://api.qollab.xyz/api/project/id/01a0ebb2-b0ee-7799-9ad4-fe18e611ea44/versions/id/01a0ebd1-1556-7ced-a669-463a94094430/file?path=qcflows%2Fhardware.py) |

**Working example 2: Quantum Hackathon Soundtrack (Qollab Team; fork of Superposition Sequencer)**

Files (sizes in bytes):

| File | Size |
|---|---|
| `index.html` | 2910 |
| `main.css` | 5564 |
| `main.js` | 11567 |
| `audio.js` | 6857 |
| `data/forte_takes.json` | 17865 |
| `soundtrack/circuits.py`, `harmony.py`, `midi.py`, `score.py`, `service.py` | — |

`requirements.txt` holds only a comment. — [Soundtrack project via Qollab API](https://qollab.xyz/u/qollab/quantum-hackathon-soundtrack)

| What | Source |
|---|---|
| Every bridge call uses `callPromising` with JSON strings: `await svc.render.callPromising(JSON.stringify(opts))`, `await svc.run_circuit.callPromising()`, `await svc.ingest.callPromising(JSON.stringify(counts), SHOTS)`. The service module docstring: "Everything crosses the JS boundary as JSON strings." | [Soundtrack `main.js`/`service.py`](https://qollab.xyz/u/qollab/quantum-hackathon-soundtrack) |
| Counts conversion: `const c = result.get_counts(); const m = c && c.toJs ? c.toJs() : c; return m instanceof Map ? Object.fromEntries(m) : m;`. A Python dict arrives in JS as a `Map` after `.toJs()`. | [Soundtrack `main.js`](https://qollab.xyz/u/qollab/quantum-hackathon-soundtrack) |
| Backend name in JS: `try { return String(backend.name ?? backend.backend_name ?? 'selected backend'); } catch { return 'selected backend'; }` | [Soundtrack `main.js`](https://qollab.xyz/u/qollab/quantum-hackathon-soundtrack) |
| Python exports a file download with `from js import sendFile; sendFile(name, "audio/midi", "data:audio/midi;base64,...")` inside try/except, returning base64 as a fallback. | [Soundtrack `service.py`](https://qollab.xyz/u/qollab/quantum-hackathon-soundtrack) |
| It also waits for the DOM (`whenMounted()` polls every 150 ms) and ends with `await new Promise(() => {})`. | [Soundtrack `main.js`](https://qollab.xyz/u/qollab/quantum-hackathon-soundtrack) |

**The injected `backend`**

What the docs say:
- `backend` is "a real Qiskit provider backend, not a Qollab wrapper":
  - Built-in runs give Qiskit's `BasicSimulator`.
  - An IBM noise model gives that device's Fake backend.
  - An IonQ choice gives `IonQProvider`'s backend.
- "Nothing intercepts `run()`." Omitting `shots` gives 1024.

— [Qollab docs: Python / Qiskit projects](https://qollab.xyz/learn/docs/python-qiskit-projects)

Engines and qubit limits:

| Backend | Engine | Qubits |
|---|---|---|
| Built-in | Qiskit `BasicSimulator` | 24 |
| AWS Braket local | Braket `StateVectorSimulator` | 25 |
| IBM | Fake backend on Qiskit Aer | 120–156 |
| IonQ remote | IonQ cloud noise-model simulator | Aria 25, Forte 29 |
| IonQ hardware | Forte 1 / Forte Enterprise 1 | 36 |

— [Qollab docs: Ideal vs. noise-model simulators](https://qollab.xyz/learn/docs/ideal-vs-noise-model-simulators); [Compute backends](https://qollab.xyz/learn/docs/compute-backends)

Qollab's patched `BasicSimulator` (qollabxyz/qiskit fork) sets:
- `MAX_QUBITS_STATEVECTOR = 24` and `MAX_QUBITS_CLIFFORD = 2048`
- `name="basic_simulator"`, with no explicit "simulator" flag
- Evolution via `np.einsum`
- `memory=True` by default
- A `seed_simulator` run option, default random
- `from js import reportCounts, reportNumQubits`, called on every run to report counts to the JS layer

— [qollabxyz/qiskit `basic_simulator.py`](https://raw.githubusercontent.com/qollabxyz/qiskit/main/qiskit/providers/basic_provider/basic_simulator.py); [commit 236e397](https://api.github.com/repos/qollabxyz/qiskit/commits/236e397711)

Other Qollab Qiskit fork patches:

| Commit | Change |
|---|---|
| d743652 | `getenv_use_multiple_threads()` in `crates/util/src/lib.rs` now always returns `false` ("Our environment won't allow spawning extra threads"), so Rust code runs single-threaded. |
| 03e9bb8 | `BasicProviderJob.get_counts()` now **raises** "Job.get_counts() is IonQ-only shortcut… use Job.result().get_counts() instead." |
| 1881654 | Dropped the fork's MPLShim because "the runtime now installs a `qollab_mpl` matplotlib backend that intercepts show()/savefig()". The body cites 21/21 Pyodide test cases passing and the private repo qollabxyz/web#269. |
| 56eba21 | Added an `update-qiskit` script that rebases the patches onto a Qiskit tag. |

— [qollabxyz/qiskit commits](https://api.github.com/repos/qollabxyz/qiskit/commits?per_page=15); [commit d743652](https://api.github.com/repos/qollabxyz/qiskit/commits/d743652fb6); [commit 03e9bb8](https://api.github.com/repos/qollabxyz/qiskit/commits/03e9bb8909)

Qollab's patched qiskit-ionq (forked from upstream at 1.0.2; PyPI upstream is now 1.1.1 from June 2026):
- **Commit c0d2657:** `submit_job` timeout changed from 30 to `None`, so Python "suspends response delivery" while the user is asked to consent to spending credits. Otherwise Emscripten would kill the request after 30 s.
- **Commit 8fdc4ac:** IonQ `Job.get_counts()` / `get_probabilities()` now emit a `UserWarning` telling you to use `Job.result().get_counts()` "for this code to run properly on non-IonQ backends."

— [qiskit-ionq commit c0d2657](https://api.github.com/repos/qollabxyz/qiskit-ionq/commits/c0d26573e9); [commit 8fdc4ac](https://api.github.com/repos/qollabxyz/qiskit-ionq/commits/8fdc4ac472); [PyPI qiskit-ionq JSON](https://pypi.org/pypi/qiskit-ionq/json)

The Qollab front-end bundle also scans code for `job.get_counts(` / `job.get_probabilities(` (regex `/\bjob\.get_(?:counts|probabilities)\s*\(/`). It uses backend IDs such as `:simulator:sim` and `ionq:forte-enterprise-1:sim`. — [qollab.xyz `_nuxt/BWPMdZ7B.js` bundle](https://qollab.xyz/u/qollab/qcflows-multifile)

**Primitives**
- `BackendSamplerV2` works only on local and IBM simulators. On IonQ, "the `qiskit-ionq` 1.0.2 provider doesn't return per-shot memory, so the wrapper fills every shot with 0 and a Bell pair comes back as all `00` with no error."
- `BackendEstimatorV2` works on every backend. On IonQ, put all (circuit, observable) pairs in **one** Estimator call at one precision; a second call fails.

— [Qollab docs: Primitives](https://qollab.xyz/learn/docs/primitives)

**One job per run on IonQ**
- IonQ remote simulators and hardware accept one job per run. A second job stops the run with "only one job is allowed per code run".
- Fix: pass all circuits to one `backend.run`, or press Stop and then Run.

— [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment); [Qollab docs: Error reference](https://qollab.xyz/learn/docs/error-reference)

**Python-side rules**
- `main()` with typed parameters (int/float/str/bool, full signature on one line starting at column 1) gets a form under Run settings, and the runtime calls it.
  - An invalid signature, e.g. `Optional[int]`, "silently" produces no form and no call.
  - Don't also call `main()` yourself, or it runs twice.
- `input()` doesn't work.
- `plt.show()` shows an SVG; `plt.savefig("x.png")` shows the image plus a PNG download.
- `sendFile(name, contentType, data)` exposes other files.

— [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)

**Network, persistence and limits**
- Network: only GET and OPTIONS. No XHR, WebSocket or web workers. JS requests go out with origin `null`, so the target must send `Access-Control-Allow-Origin: *`. — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
- Persistence: nothing survives between runs. `localStorage`, `sessionStorage`, IndexedDB and cookies are unavailable in the sandboxed frame. — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
- Limits: 100 files × 2 MB, 200 MB per account, no run-time limit. Stop gives Python 5 s. — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)

**Browser, Pyodide and Python versions**
- Requires WebAssembly JSPI: "recent Chrome, Edge, or Opera, or Firefox 153 or later". Otherwise Run is disabled. — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment); [FAQ](https://qollab.xyz/learn/docs/faq)
- Safari: one secondary source lists JSPI only in "Safari 27 beta" as of mid-2026 (unverified). — [OpenReplay JSPI article](https://blog.openreplay.com/jspi-javascript-wasm-bridge/); [WebKit bug 283054](https://bugs.webkit.org/show_bug.cgi?id=283054)
- Pyodide version: qollab.xyz's own CSP whitelists `cdn.jsdelivr.net/pyodide/v314.0.7/full/` (HTTP headers fetched 2026-10-09). The docs say "Python 3.14, Qiskit 2.x, and NumPy 2.x". Pyodide 314.0.0 (June 9 2026) moved to Python 3.14.2, and 314.0.7 shipped Sept 14 2026. — [qollab.xyz response headers](https://qollab.xyz/u/qollab/qcflows-multifile); [Python / Qiskit projects](https://qollab.xyz/learn/docs/python-qiskit-projects); [Pyodide changelog](https://pyodide.org/en/stable/project/changelog.html)
- Sign-in: one error is "Can't run quantum jobs as an anonymous user at the moment… Sign in again, then rerun." — [Error reference](https://qollab.xyz/learn/docs/error-reference)

### Inferences
- **Recommended bridge (copy of the official pattern):**
  - Python modules expose small functions that take and return **JSON strings**.
  - JS calls them with `await mod.fn.callPromising(jsonString)` and parses the result with `JSON.parse(String(x))`.
  - This avoids PyProxy lifetime/leak issues and the Map-vs-Object surprise.
  - Keep any Python object you hand to `backend.run` (the circuit) as a proxy; don't JSON it.
- **Use `callPromising` everywhere**, not plain sync calls. It is the only mode the docs guarantee to work when a remote backend is involved, and it costs nothing on local simulators.
- **Backend detection is best-effort.** Wrap it in try/catch: `backend.name`, then `backend.backend_name`, then a fallback. Expected values: `"basic_simulator"` on the built-in, `fake_*` names on IBM (the usual Qiskit Fake backend naming), and IonQ names containing "ionq" or "qpu"/"simulator". Only the first is source-confirmed. Branch on substrings, never exact strings. Treat the backend as remote/limited if the name contains "ionq".
- **`num_qubits`** is probably readable as `backend.num_qubits` (BackendV2 attribute; standard for Fake backends and IonQ). Upstream `BasicSimulator`'s target may report `None`. Guard with a fallback of 24. Not verified at runtime.
- **The keep-alive trick matters only if the tool lets users press a button that hits the backend after initial load.** If all backend work happens during boot, the run can finish normally. For an interactive page, end `main.js` with `await new Promise(() => {})` as both official examples do, so the page stays live.
- **Python-only fallback:** a pure `main.py` project can't render rich interactive UI (only console, SVG and PNG). For a teaching tool, JS + Python is the right shape.

### Gaps
- The Qollab runtime source (qollabxyz/web) is private, so I couldn't confirm the full JS global surface: `reportCounts`, `reportNumQubits`, `sendFile`, and whether `sendFile` can be called directly from JS. I also couldn't confirm the PyProxy-to-JS conversion defaults (e.g. `dict_converter`).
- I couldn't confirm whether `backend.num_qubits`, `backend.target` or `backend.options` behave identically across all providers inside Qollab.
- I didn't run anything on Qollab: first-run load time of Qiskit in Qollab, and the exact error surfaces on IonQ, are unverified.

---

## Q2. Which Qiskit pieces and which useful Python packages (stim, pymatching, pyzx, qutip, networkx, sympy, scipy.sparse, qiskit_aer) actually load in Pyodide in Oct 2026?

### Takeaway
Qiskit does **not** publish a WASM wheel. Qollab builds its own patched Qiskit 2.5.x, with Rust compiled single-threaded, and Qiskit Aer 0.17.2 (via the PQCA preset).

**Package availability in Pyodide 314.0.7 (my tests and the package list):**

| Status | Packages |
|---|---|
| Built in | networkx 3.6.1, sympy 1.14.0, scipy 1.18.0 (with `scipy.sparse`), matplotlib 3.10.8, pandas, scikit-learn |
| Installs from PyPI | rustworkx 0.18.1 (official `pyemscripten_2026_0` wheel); pyzx 0.10.7 (pure Python), works |
| Fails | **stim, pymatching, qutip**: no pure or Emscripten wheel |

For QEC teaching, use networkx `max_weight_matching` as the decoder, or a JS-side stabilizer simulator.

### Cited Findings
**Pyodide 314.0.7 built-in package list**
- **Present:**

  | Package | Version |
  |---|---|
  | numpy | 2.4.6 |
  | scipy | 1.18.0 |
  | sympy | 1.14.0 |
  | networkx | 3.6.1 |
  | matplotlib | 3.10.8 |
  | pandas | 3.0.2 |
  | scikit-learn | 1.8.0 |
  | Pillow | 12.2.0 |
  | cvxpy-base | 1.8.2 |
  | igraph | 1.0.0 |
  | highspy | 1.13.1 |
  | python-sat | 1.8.dev26 |

- **Not present:** qiskit, qiskit-aer, rustworkx, stim, pymatching, pyzx, qutip, galois, ldpc, symengine, pyscf, jax, numba, cirq, pennylane, pytket.

— [Pyodide 314.0.7 packages list](https://pyodide.org/en/stable/usage/packages-in-pyodide.html)

**Pyodide history and the new wheel tag**
- rustworkx (0.17.0a3) was added as a Pyodide package in 0.29.0. In 314.0.2, packages that now ship PyEmscripten wheels on PyPI were removed from the lockfile. — [Pyodide changelog](https://pyodide.org/en/stable/project/changelog.html); [Pyodide 0.29.0 changelog](https://pyodide.org/en/0.29.0/project/changelog.html)
- PEP 783 defines the PyPI-accepted platform tag `pyemscripten_<year>_<patch>_wasm32`, which installers read from `sysconfig.get_config_var("PYEMSCRIPTEN_PLATFORM_VERSION")`. — [PEP 783](https://peps.python.org/pep-0783/)
- **My test:** in Pyodide 314.0.7 that value is `"2026_0"`, and micropip is 0.11.1. — [own test, Pyodide console](https://pyodide.org/en/stable/console.html)

**PyPI wheel survey, 2026-10-09** (latest release of each package)
- **Emscripten wheel published:** only rustworkx 0.18.1 (`rustworkx-0.18.1-cp310-abi3-pyemscripten_2026_0_wasm32.whl`).
- **No Emscripten wheel:** qiskit 2.5.2, qiskit-aer 0.17.2, stim 1.16.0, pymatching 2.4.0, qutip 5.3.1, ldpc 2.4.1, symengine 0.14.1, pytket 2.18.5.
- **Pure-Python (`py3-none-any`):**

  | Package | Version |
  |---|---|
  | pyzx | 0.10.7 |
  | galois | 0.4.11 |
  | quimb | 1.15.0 |
  | cirq-core | 1.7.0 |
  | pennylane | 0.45.1 |
  | qiskit-ionq | 1.1.1 |
  | qiskit-qasm3-import | 0.6.0 |
  | pylatexenc | 2.11 |
  | lark | 1.3.1 |
  | networkx | 3.7 |

— [PyPI JSON API](https://pypi.org/pypi/stim/json), queried for each package

**Qiskit's dependencies**
- Qiskit 2.5.2 needs `numpy>=2.0,<3`, `scipy>=1.14`, `rustworkx>=0.15.0`, `dill`, `stevedore` and `typing-extensions`.
- The `visualization` extra adds matplotlib, pydot, Pillow, pylatexenc, seaborn and sympy. — [PyPI qiskit JSON](https://pypi.org/pypi/qiskit/json)

**My micropip tests in stock Pyodide 314.0.7 / Chromium 152** (all from the [Pyodide console](https://pyodide.org/en/stable/console.html))
- `micropip.install('rustworkx')` succeeded: version 0.18.1, 2.2 s.
- `micropip.install('stim')`, `'pymatching'` and `'qutip'` each failed with `ValueError: Can't find a pure Python 3 wheel for '<pkg>'`.
- `micropip.install('pyzx')` succeeded in 2.7 s. `zx.full_reduce` on an 8-qubit, depth-200 `CNOT_HAD_PHASE_circuit` went from 345 to 58 vertices in 5.27 s, including first import.
- `networkx.max_weight_matching(maxcardinality=True)` on complete graphs (a minimum-weight perfect matching (MWPM) decoder stand-in), timed by defect count:

  | Defects | Time |
  |---|---|
  | 10 | 3.2 ms |
  | 20 | 12.7 ms |
  | 40 | 85.8 ms |

**pyzx's dependencies**
- pyzx 0.10.7 requires typing_extensions, numpy, pyperclip, tqdm, ipywidgets and lark. All are pure Python or in Pyodide. — [PyPI pyzx JSON](https://pypi.org/pypi/pyzx/json)

**What Qollab installs**
- Pure-Python wheels and Pyodide-built packages install from `requirements.txt`. Packages "that need compiled code with no Pyodide build stop the run with 'Could not install every package listed in requirements.txt.'"
- Pip options, environment markers and URL requirements are refused. — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
- Library presets:

  | Preset | Version |
  |---|---|
  | Qiskit Visualizations | 2.x |
  | Qiskit Algorithms | 0.4.0 |
  | Qiskit Optimization | 0.7.0 |
  | Qiskit Nature + PySCF | 0.8.0 |
  | Qiskit Finance | 0.4.1 |
  | Qiskit Machine Learning | 0.9.1 |
  | QAVE | 0.1.0 |

  — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment); [qollab.xyz JS bundle library table](https://qollab.xyz/u/qollab/qcflows-multifile)
- PQCA is "Partitioned Quantum Cellular Automata" (github.com/hmillerbakewell/partitioned-quantum-cellular-automata, "2.x.x with Qiskit 2.x compat"). It brings `qiskit_aer 0.17.2` and `qiskit_ibm_runtime 0.50.0`. — [qollab.xyz JS bundle](https://qollab.xyz/u/qollab/qcflows-multifile); [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)
- IBM noise-model backends run "Qiskit Aer with its calibrated noise model" in the browser. Aer switches to the density-matrix method only when shots > 2^n and all measurements are at the end. — [Ideal vs. noise-model simulators](https://qollab.xyz/learn/docs/ideal-vs-noise-model-simulators)

**Qiskit modules confirmed working inside Qollab** (from the official example projects)

| Module | Where it's used |
|---|---|
| `qiskit.quantum_info.Statevector` (`from_instruction`, `probabilities_dict`) | QCFlows `hardware.py` |
| `partial_trace` and `entropy` | Soundtrack `circuits.py` |
| `transpile(..., basis_gates=..., optimization_level=0/1)` with no backend | Both projects |
| OpenQASM 2/3 import via `qiskit_qasm3_import` | QCFlows |
| `circuit.draw("mpl")` | Needs the Qiskit Visualizations preset; `print(circuit)` gives a text drawing without it |

— [QCFlows](https://qollab.xyz/u/qollab/qcflows-multifile); [Soundtrack](https://qollab.xyz/u/qollab/quantum-hackathon-soundtrack); [Python / Qiskit projects](https://qollab.xyz/learn/docs/python-qiskit-projects)

**Building Rust extensions for Pyodide**
- Rust-extension packages (PyO3/maturin) are cross-compiled with pyodide-build to `wasm32-unknown-emscripten`; the Rust toolchain must be set up manually. — [pyodide-build Rust tutorial](https://pyodide-build.readthedocs.io/en/stable/tutorials/rust.html)
- Searching Qiskit's issue tracker for "pyodide" found only CI/cibuildwheel bumps, with no official Emscripten target. — [GitHub search Qiskit/qiskit pyodide](https://api.github.com/search/issues?q=repo:Qiskit/qiskit+pyodide&per_page=20)

**QAVE (the Qollab-maintained visualization library)**
- QAVE emits a versioned `trace.json` and renders GIF/MP4 through a **Processing (Java, P3D) + PeasyCam + ffmpeg** viewer.
- Main API: `generate_animation_from_qiskit(circuit, options=SimulationOptions(algorithm_id=..., mode="validation", seed=24, shot_count=100), artifacts=ArtifactOptions(out_dir=...))`. MIT licensed.
- The README documents no keyboard, reduced-motion or alt-text features. — [qollabxyz/qave README](https://raw.githubusercontent.com/qollabxyz/qave/main/README.md)

### Inferences
- **Qiskit in the browser is a custom build.** It is effectively Qiskit 2.5.x compiled by Qollab with single-threaded Rust, so quantum_info, the transpiler, the primitives and the circuit library should all work, just slower than native. Anything that spawns threads or processes (`parallel_map`, multiprocessing) is disabled or would fail.
- **For QEC / fault-tolerance teaching:**
  - Use Qiskit's `quantum_info.Clifford` / `StabilizerState` for stabilizer simulation. They are part of Qiskit, so they are available.
  - `BasicSimulator`'s Clifford path supports up to 2048 qubits.
  - Use `networkx.max_weight_matching` for an MWPM decoder. 40 defects in under 0.1 s is plenty for distance-3 to distance-7 demos.
  - Don't plan on stim or pymatching.
  - The Stim/Crumble JS tools are Apache-2.0 (see Q3), which may conflict with the hackathon's "outside repos must be MIT" rule.
- **pyzx works** and is a strong candidate for a "ZX-calculus / circuit optimization" teaching tool. Budget about 3 s for install and import on first run.
- **galois and quimb install as wheels but probably fail at import.** Both depend on numba, which isn't in Pyodide. Avoid them.
- **cirq-core and pennylane are pure wheels** and might install, but they add load time. They are irrelevant to a Qiskit-required hackathon.
- **QAVE's renderer** (Processing/ffmpeg) can't run in Pyodide. In Qollab, QAVE is at best a trace generator, and you'd need your own JS player for `trace.json`. Verify by opening a Qollab QAVE example project before relying on it.
- **qiskit_aer via PQCA** gives Aer's `NoiseModel` and `AerSimulator(method="density_matrix")` for custom-noise teaching. Turning it on adds a heavy first-run download; budget for it or precompute.

### Gaps
- I couldn't download Qollab's actual Qiskit/Aer WASM wheels, so I measured no Qiskit-specific timings (import time, `transpile` time, `Statevector.evolve` overhead versus raw einsum).
- I couldn't confirm how the "Qiskit Visualizations" preset is spelled in `requirements.txt` (e.g. `pylatexenc`/`seaborn` presence), or whether `plot_bloch_multivector` (matplotlib 3D) renders correctly through Qollab's `qollab_mpl` backend.
- I didn't test whether Qollab's installer honours `pyemscripten` wheels from PyPI (e.g. a newer rustworkx); it ships its own build anyway.

---

## Q3. Can index.html pages load external JS/CSS from CDNs on Qollab, or must they be vendored? What visualization libraries are practical and license-compatible?

### Takeaway
Yes, CDNs work, but **only jsDelivr for scripts**. The JS frame's CSP allows `script-src cdn.jsdelivr.net` and blocks unpkg, cdnjs and esm.sh. The official QCFlows project imports D3 that way: `https://cdn.jsdelivr.net/npm/d3@7/+esm`.

| Resource | What's allowed |
|---|---|
| Bare imports | `three` 0.186.1, `three/addons/`, `postprocessing` 6.39.5 (import map); docs also list tween.js and meshline |
| Stylesheets | Any origin (`style-src *`) |
| Fonts | Any origin (`font-src *`) |
| Images and media | Any origin (`img-src *`) |
| Web workers | Blocked |
| Vendored code | Small ES modules as project `.js` files (≤ 2 MB each) |

For the hackathon's MIT-only rule, prefer MIT libraries: three.js, KaTeX, Plotly.js, quantum-circuit, Chart2Music. D3 is ISC, which is functionally MIT-like.

### Cited Findings
**What the docs say**
- "`three`, `three/addons/…` (three.js 0.186.1), `postprocessing` (6.39.5), `@tweenjs/tween.js`, and `meshline` are available. Other packages can be loaded from a full URL, such as a jsDelivr `/+esm` link." — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)

**The JS sandbox frame (`qollab.xyz/jsworker.html`)**
- It contains an import map: `"three": "https://cdn.jsdelivr.net/npm/three@0.186.1/build/three.module.js"`, `"three/addons/": ".../three@0.186.1/examples/jsm/"`, `"postprocessing": "https://cdn.jsdelivr.net/npm/postprocessing@6.39.5/+esm"`.
- It loads the project module from `location.hash` as `<script type="module">`, and shows a 🚀 "Loading..." overlay while loading.
- Its `Content-Security-Policy` header (fetched 2026-10-09):

  | Directive | Value |
  |---|---|
  | `default-src` | 'self' blob: data: api.cms.qollab.xyz api.qollab.xyz pub.qollab.xyz … github.com raw.githubusercontent.com … cdn.jsdelivr.net pypi.org files.pythonhosted.org |
  | `script-src` | 'self' 'unsafe-eval' 'unsafe-inline' www.googletagmanager.com e.qollab.xyz cdn.jsdelivr.net connect.facebook.net |
  | `style-src` | 'unsafe-inline' * |
  | `font-src` | * |
  | `img-src` | blob: data: * |
  | `media-src` | blob: data: * |
  | `connect-src` | * |
  | `worker-src` | 'none' |
  | `object-src` | 'none' |

— [qollab.xyz/jsworker.html (headers and body)](https://qollab.xyz/jsworker.html)

**Working CDN import and vendoring rules**
- QCFlows: "No script tags. index.html holds body markup only, and D3 comes in with `import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm"`." — [QCFlows](https://qollab.xyz/u/qollab/qcflows-multifile)
- Vendoring: project JS files import via `./` paths (`.js`/`.mjs`). Each file is ≤ 2 MB, with 100 files per project. JS can't fetch non-JS project files. — [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment)

**Hackathon license rule**
- Projects must be published "on an MIT license", and "Any outside repo the project relies on must also use an MIT license." — [Qollab Rules & Terms](https://qollab.xyz/programs/hackathon/terms)

**Library licenses (GitHub API, 2026-10-09)**

| Library | License | Notes | Source |
|---|---|---|---|
| KaTeX | MIT | — | [GitHub API KaTeX](https://api.github.com/repos/KaTeX/KaTeX) |
| Plotly.js | MIT | — | [GitHub API plotly.js](https://api.github.com/repos/plotly/plotly.js) |
| p5.js | **LGPL-2.1** | — | [GitHub API p5.js](https://api.github.com/repos/processing/p5.js) |
| quantastica/quantum-circuit ("Quantum Circuit Simulator implemented in JavaScript") | MIT | 274 stars; last push 2026-09-19 | [GitHub API quantum-circuit](https://api.github.com/repos/quantastica/quantum-circuit) |
| Strilanc/Quirk | **Apache-2.0** | Last push 2024-07-16 | [GitHub API Quirk](https://api.github.com/repos/Strilanc/Quirk) |
| quantumlib/Stim (which contains Crumble) | **Apache-2.0** | — | [GitHub API Stim](https://api.github.com/repos/quantumlib/Stim) |
| Quantum-Flytrap/quantum-tensors | No license declared (`null`) | Last push 2023 | [GitHub API quantum-tensors](https://api.github.com/repos/Quantum-Flytrap/quantum-tensors) |
| Chart2Music (chart sonification) | MIT | — | [Chart2Music README on jsDelivr](https://cdn.jsdelivr.net/npm/chart2music@1.20.0/README.md); [npm chart2music](https://www.npmjs.com/package/chart2music) |

**What past Qollab winners and showcases use**
- "Entangled Body" used a Next.js/Three.js front-end with a server back-end, outside Qollab's runtime. — [GitHub: Entangled-Body](https://github.com/IonQ-Qollab-Quantum-Challenge/Entangled-Body) (from the earlier notes file)
- QCFlows uses a D3 force graph, heatmap and timeline in the browser. — [QCFlows](https://qollab.xyz/u/qollab/qcflows-multifile)

### Inferences
- **The CSP is good evidence about the JS project frame**, because its import map exactly matches the documented three.js and postprocessing versions. Under that CSP, `<script>`/ESM from **unpkg.com, cdnjs.cloudflare.com, esm.sh or skypack would be blocked**. Use `https://cdn.jsdelivr.net/npm/<pkg>@<exact-version>/+esm`, and pin exact versions (QCFlows' `d3@7` floats).
- **CSS from CDNs** (e.g. KaTeX's `katex.min.css` plus fonts) is allowed by `style-src *` / `font-src *`. Only `main.css` is auto-loaded, though, so inject it from JS: `const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = '...'; document.head.append(l);`. The alternative is to copy the needed CSS into `main.css` and let fonts load from jsDelivr. This is untested in Qollab.
- **Recommended stack for a teaching tool:**

  | Need | Choice |
  |---|---|
  | 3D Bloch spheres | three.js (pre-wired, MIT) |
  | Circuit diagrams, amplitude bars, lattices, decoding graphs | D3 or hand-written SVG |
  | Equations | KaTeX (`+esm`, MIT); MathJax is Apache-2.0 |
  | Charts | Plotly.js only if needed (large bundle) |
  | Sonification | Chart2Music (MIT) or the native Web Audio API |
  | Client-side gate-by-gate simulation | quantum-circuit (MIT) |

  For client-side simulation, a hand-written ~100-line JS statevector for ≤ 10 qubits is simpler still: it makes "drag a slider, see the state" instant without a Python round trip.
- **Avoid as dependencies, given the MIT-only clause:** p5.js (LGPL), Quirk/Crumble (Apache-2.0), and quantum-tensors (unlicensed). Linking out to Quirk or Crumble as "further exploration" is fine.
  - Qiskit itself is Apache-2.0 and required, so organizers clearly don't apply the clause to platform libraries. Ask in the global Slack before relying on any non-MIT runtime dependency.
- **Bundle-size budget:** every CDN library adds first-load latency on the judge's machine. Pyodide + Qiskit is already the dominant cost.
- **No workers** means heavy JS (large three.js scenes, big D3 force simulations) competes with Python on the main thread. Keep scenes light and pause animations while Python runs.

### Gaps
- I didn't confirm empirically that the JS project iframe is exactly `jsworker.html` with this CSP, or that unpkg/cdnjs are actually blocked. Both are inferred from the headers plus the matching import map.
- I didn't confirm whether `<link>`, `<style>` or `<template>` tags inside `index.html` survive insertion.
- D3's license (ISC) and Crumble's exact licensing were not re-verified via API in this session.
- I found no MIT-licensed, maintained npm "Bloch sphere" package worth recommending over a ~150-line three.js implementation.

---

## Q4. What are realistic performance ceilings for Qiskit statevector / density-matrix simulation in the browser?

### Takeaway
Single-threaded WASM with a ~4 GiB heap, where **no single array can reach 2 GiB** (wasm32 `sys.maxsize = 2^31−1`):
- **Statevectors:**
  - ≤ 16 qubits: interactive, a few ms per gate.
  - 18–20 qubits: tens of ms per gate.
  - 22 qubits: ~0.15–0.25 s per gate.
  - 24 qubits: ~0.8 s per gate.
  - 27 qubits (complex128): impossible.
- **Density matrices:** ~8 qubits is comfortable, 10 is sluggish, 11+ is not interactive.
- **Mid-circuit measurement and noise models** multiply cost by the number of shots.

Design for ≤ 12 qubits for anything live and precompute the rest.

### Cited Findings
**My einsum benchmark** (Pyodide 314.0.7, Python 3.14.2, NumPy 2.4.6, Chromium 152, Windows 11; complex128)

This uses the same `np.einsum(..., dtype=complex, casting="no")` kernel as `BasicSimulator`. One gate application:

| Qubits | 1-qubit gate | 2-qubit gate (CX) |
|---|---|---|
| 10 | 0.9 ms | 0.4 ms |
| 14 | 0.9 ms | 1.3 ms |
| 16 | 2.4 ms | 4.2 ms |
| 18 | 15 ms | 17 ms |
| 20 | 36 ms | 71 ms |
| 22 | 155 ms | 230 ms |
| 23 | 464 ms | 615 ms |
| 24 | 782 ms | 874 ms |

— [own measurement, Pyodide console](https://pyodide.org/en/stable/console.html)

**My memory-ceiling test** (same setup)
- The Wasm heap grew to 4,165,533,696 bytes (~3.9 GiB). `MemoryError` hit after holding 3,840 MiB in 256-MiB arrays.
- Single allocations of 2^25 and 2^26 complex128 (512 MiB and 1 GiB) succeeded.
- `np.empty(2**27, dtype=complex)` (2 GiB) raised `ValueError: array is too big`; `sys.maxsize` is 2147483647.

— [own measurement](https://pyodide.org/en/stable/console.html)

**My naive density-matrix benchmark**
- Method: 1-qubit `U ρ U†` with a single 3-operand `einsum`, unoptimized, so treat it as an upper bound.

  | Qubits | Time per gate | ρ size |
  |---|---|---|
  | 8 | 19 ms | 1 MiB |
  | 10 | 191 ms | 16 MiB |
  | 11 | 865 ms | 64 MiB |

- A 13-qubit ρ is 1 GiB (2 copies would exceed the heap).

— [own measurement](https://pyodide.org/en/stable/console.html)

**Background on the 4 GiB ceiling**
- 4 GB is the most wasm32 can address, up from a previous practical limit of 2 GB. — [V8 blog: Up to 4GB of memory in WebAssembly](https://v8.dev/blog/4gb-wasm-memory)

**Qollab's published timings and scaling** — all from [Ideal vs. noise-model simulators](https://qollab.xyz/learn/docs/ideal-vs-noise-model-simulators)
- Ideal simulators "apply the gates once, then sample all shots", so shots barely matter.
- With a mid-circuit measurement or reset, the built-in simulator reruns the circuit every shot. On a 10-qubit circuit, 1,000 shots took 13 s versus 0.07 s without.
- Noise-model simulators resample errors per shot.
  - IBM models cost about 13 ms per shot after a ~10 s fixed setup for a 156-qubit device model.
  - The page notes the browser "runs the same libraries as WebAssembly on one thread and is several times slower" than its native numbers.
- Native single-core timings for a 10-qubit, 20-layer circuit:

  | Shots | Built-in | Braket local | IBM Fez noise model |
  |---|---|---|---|
  | 1 | 0.02 s | 0.2 s | 9.8 s |
  | 1,000 | 0.02 s | 0.2 s | 22.6 s |
  | 2,000 | 0.02 s | 0.4 s | 14.4 s |

  The IBM time drops at 2,000 shots because the run switches to density-matrix mode once shots exceed 2^n.

**Load times and remote simulators**
- "The built-in simulator starts immediately." AWS Braket and IBM simulators "load their libraries the first time you pick one in a session," and IBM simulators "build a device model on every run." — [Compute backends](https://qollab.xyz/learn/docs/compute-backends); [FAQ](https://qollab.xyz/learn/docs/faq)
- IonQ remote noise simulation is one simulation per shot, so run time grows with shots. Runs near the ceiling (29 qubits on Forte simulators) "may still fail". Possible errors include `SimulationTimeout` and `TooLongPredictedExecutionTime`. — [Compute backends](https://qollab.xyz/learn/docs/compute-backends); [Error reference](https://qollab.xyz/learn/docs/error-reference)

**Threads**
- No web workers are allowed (CSP `worker-src 'none'`; docs: "web workers are unavailable"). Qollab's Qiskit fork forces Rust to a single thread. — [jsworker.html CSP](https://qollab.xyz/jsworker.html); [Runtime environment](https://qollab.xyz/learn/docs/runtime-environment); [qollabxyz/qiskit commit d743652](https://api.github.com/repos/qollabxyz/qiskit/commits/d743652fb6)

### Inferences
- **Practical budgets on a mid-range laptop**, from the per-gate times above:

  | Use | Qubits | Cost |
  |---|---|---|
  | Live, every-slider-move | ≤ 12 statevector, ≤ 6–8 density matrix | ~1 ms per gate |
  | On demand, "press to compute" | Up to ~20 statevector | 100 gates ≈ 4–7 s |
  | Avoid live | 24 qubits | 100 gates ≈ 80 s, peak memory ≈ 2 × 256 MiB plus overhead |

  Because Pyodide runs on the page's main thread, a 5 s computation freezes the UI. Show a busy state and yield first (`await new Promise(r => setTimeout(r))`).
- **The built-in judge backend caps at 24 qubits**; Braket is 25. Choose a run-on-backend circuit of ≤ 20 qubits (the Soundtrack uses 20 and calls it something "which fits every Qollab backend") and ≤ ~1,000 shots.
- **Avoid mid-circuit measurement and reset in the circuit you send to `backend.run`** on the built-in simulator. It turns a 0.07 s run into ~13 s natively (more in WASM) at 1,000 shots. For teleportation or QEC syndrome-extraction demos:
  - Use deferred measurement, or a small qubit count with few shots.
  - Or simulate the measurement logic yourself with `Statevector` / `Clifford` in Python.
- **Use Clifford/stabilizer methods for QEC demos.** They scale to hundreds or thousands of qubits cheaply. Use statevectors only for small, non-Clifford illustrations.
- **Density-matrix teaching** (decoherence, channels, noise) should use 1–3 qubits live, which is effectively free. Precompute larger noisy-sim curves offline and ship them as JSON.
- Real Qiskit `Statevector.evolve` and `transpile` add Python and Rust overhead on top of these raw kernels, so treat the table as optimistic for very small circuits. The large-n figures are kernel-dominated.

### Gaps
- No Qiskit-in-WASM measurements were possible: the Qollab wheel isn't downloadable and I didn't sign in to Qollab. Unknown:
  - Qiskit import time (likely several seconds on first run)
  - `transpile` latency
  - `StatevectorSampler` / `StatevectorEstimator` timings
  - Aer-in-WASM timings
- Browser and hardware variation: measured on one Chromium build on one machine. Firefox 153+ JSPI performance is untested.

---

## Q5. What accessibility practices should an interactive quantum visualization follow (WCAG 2.2 AA, keyboard, ARIA for SVG/canvas, text alternatives, sonification, color, motion)?

### Takeaway
The rule is "Follow industry best practices on UI accessibility", which means WCAG 2.2 AA. Build every visual as **real DOM** (native controls, SVG with roles and names) rather than an opaque canvas. Pair each visualization with:
- A text/table alternative
- Live-region "responses", the PhET Interactive Description pattern
- Full keyboard operation, with no drag-only interactions
- 24 × 24 px targets
- Okabe–Ito colors plus redundant encodings
- `prefers-reduced-motion` support
- Optional sonification, as in Desmos audio trace and Chart2Music

### Cited Findings
**Hackathon wording**
- "Follow industry best practices on UI accessibility." — [Qollab Rules & Terms](https://qollab.xyz/programs/hackathon/terms)

**WCAG 2.2** (W3C Recommendation, 5 Oct 2023) adds these criteria:

| Criterion | Level | Requirement |
|---|---|---|
| 2.4.11 Focus Not Obscured (Minimum) | AA | A focused component must not be entirely hidden by author content |
| 2.4.13 Focus Appearance | AAA | Focus indicator ≥ 2 CSS px perimeter, 3:1 contrast |
| 2.5.7 Dragging Movements | AA | A single-pointer, non-drag alternative unless dragging is essential |
| 2.5.8 Target Size (Minimum) | AA | ≥ 24 × 24 CSS px or sufficient spacing |
| 3.2.6 Consistent Help | A | Repeated help mechanisms appear in the same relative order |
| 3.3.7 Redundant Entry | A | Don't re-ask for information the user already gave |
| 3.3.8 Accessible Authentication (Minimum) | AA | No cognitive-function test at login without an alternative |

4.1.1 Parsing was removed. — [W3C WAI: What's new in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)

**Complex images (charts, diagrams)**
- They need a short text alternative plus a long description, ideally visible to everyone.
- Approaches:
  - Wrap image and description in `<figure role="group">` + `<figcaption>`.
  - Use an adjacent link to the description.
  - Use `aria-describedby` for text-only descriptions. Screen readers read the referenced element as one paragraph, without headings or tables.

— [W3C WAI Images Tutorial: Complex images](https://www.w3.org/WAI/tutorials/images/complex/)

**SVG accessibility**
- For a static graphic, put `role="img"` on the `<svg>`, add `<title>` (and `<desc>`) with ids, and reference them via `aria-labelledby`. TPGI found SVG was otherwise ignored by many browser and screen-reader combinations (testing dated ~2013–14). — [TPGI: Using ARIA to enhance SVG accessibility](https://tpgi.com/using-aria-enhance-svg-accessibility); [Orange accessibility guidelines: Accessible SVG](https://a11y-guidelines.orange.com/en/articles/accessible-svg/)
- For interactive SVG, every focusable element needs `tabindex`, a `role` and an accessible name (`aria-label` or a child `<title>`).
  - Avoid positive tabindex.
  - Never remove the focus outline.
  - `tabindex="-1"` allows programmatic `focus()`.

  — [Fizz Studio on interactive SVG](https://fizz.studio/?p=246); [MDN SVGElement.tabIndex](https://developer.mozilla.org/docs/Web/API/SVGElement/tabIndex); [SVG2 WG note on focus](https://lists.w3.org/Archives/Public/public-svg-wg/2013AprJun/0162.html)

**PhET Interactive Description framework**

*State descriptions*
- **Static:** names of interactive objects, a scene summary, navigation order, and hints.
- **Dynamic:** updated to stay accurate, using "qualitative scales".

*Responsive descriptions*
- **Object responses** describe changes to the object the user manipulated. For sliders they use `aria-valuetext`.
- **Context responses** describe changes in the surrounding scene.
- Both are delivered through ARIA live regions, which PhET shows as an activity log.

*Tools and background*
- PhET's "A11y View" displays the descriptions visually for testing without a screen reader. Example: [Resistance in a Wire a11y view](https://phet.colorado.edu/sims/html/resistance-in-a-wire/latest/resistance-in-a-wire_a11y_view.html).
- Earlier research used a "parallel DOM" to give HTML equivalents of every interactive element.

— [CU Boulder / Coursera: Description Design for Interactive Learning Resources](https://www.coursera.org/learn/description-design-for-interactive-learning-resources) (search snippets); [Smith et al. 2017 (OCAD)](https://openresearch.ocadu.ca/id/eprint/1576/); [Springer: PhET parallel DOM work](https://link.springer.com/chapter/10.1007/978-3-319-92049-8_28)

**Desmos audio trace (sonification precedent)**
- Alt/Option+T enters audio trace, and H plays the graph. Keyboard and keypad control volume, speed and point-to-point navigation, and the mode speaks point and axis descriptions.
- Sound carries meaning: an overtone marks x crossing from negative to positive, static marks negative y, and "pops" mark intersections. — [Desmos Help: Audio Trace](https://help.desmos.com/hc/en-us/articles/37064105800333-Audio-Trace); [Perkins: Desmos sonification](https://www.perkins.org/resource/understanding-desmos-sonification-lessons/)
- Known pitfalls: embedded graphs are reachable only via tab order, and the default orange fails WCAG contrast. — [Illinois CITL Desmos guide](https://citl.illinois.edu/node/623)

**Chart2Music**
- "Turns charts into sound so blind users can hear the data." MIT licensed. — [Chart2Music README](https://cdn.jsdelivr.net/npm/chart2music@1.20.0/README.md)

**Reduced motion**
- `@media (prefers-reduced-motion: reduce)` takes the values `no-preference` and `reduce`. It is Baseline widely available since January 2020. — [MDN prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)

**Okabe–Ito color-blind-safe palette**

| Color | Hex |
|---|---|
| Orange | #E69F00 |
| Sky blue | #56B4E9 |
| Bluish green | #009E73 |
| Yellow | #F0E442 |
| Blue | #0072B2 |
| Vermillion | #D55E00 |
| Reddish purple | #CC79A7 |
| Black | #000000 |

— [NYU Siegal lab palette page](https://siegal.bio.nyu.edu/color-palette/); [ConceptViz Okabe–Ito reference](https://conceptviz.app/blog/okabe-ito-palette-hex-codes-complete-reference)

**What Qollab's own reference app does**
- QCFlows sets `aria-pressed` on toggle buttons, `aria-expanded`/`aria-controls`/`aria-label` on collapsible sections, and `aria-hidden` on icons.
- It supports arrow keys on its timeline, and its README says "Drag the timeline slider or use the arrow keys".
- Gates are placed by "click a gate, then click qubits", which is a non-drag interaction.

— [QCFlows `main.js`](https://api.qollab.xyz/api/project/id/01a0ebb2-b0ee-7799-9ad4-fe18e611ea44/versions/id/01a0ebd1-1556-7ced-a669-463a94094430/file?path=main.js); [QCFlows README](https://qollab.xyz/u/qollab/qcflows-multifile)

### Inferences
**A concrete checklist for a quantum teaching tool:**

1. **Use native controls** for parameters, so keyboard, screen-reader and touch support come free:
   - `<input type="range">` for θ/φ and noise strength
   - `<button>` for gates
   - `<fieldset>`/radio groups for basis choice
2. **Write quantum-meaningful `aria-valuetext`**, e.g. "θ = 90°, qubit on the equator, 50% chance of 1".
3. **Give the Bloch sphere a text twin.** A three.js canvas gets `role="img"` plus an `aria-label`. Next to it, a visible or toggleable readout gives Bloch (x, y, z), θ, φ, and P(0)/P(1), updated on change. Announce changes through a polite `aria-live` region; this is a PhET-style "object response".
4. **Pair each amplitude or probability chart with a real `<table>`** (basis state | amplitude | phase | probability), toggleable as a "data view".
5. **Encode phase redundantly**, e.g. colour wheel plus arrow angle plus numeric value, so meaning never relies on colour alone.
6. **Don't depend on drag** (WCAG 2.5.7):
   - Circuit editors use click-to-select, then click-to-place, plus keyboard (arrow keys move a cursor across the qubit × time grid; Enter places; Delete removes).
   - Rotating the Bloch sphere by drag needs buttons or keys as an alternative.
7. **Use 24 × 24 px minimum targets** and a visible `:focus-visible` outline with ≥ 3:1 contrast. Make sure sticky headers don't cover focused items (2.4.11).
8. **Respect reduced motion** with `matchMedia('(prefers-reduced-motion: reduce)')`:
   - Skip interpolation and jump to the end state.
   - Disable auto-rotating spheres.
   - Provide a "step" button for gate-by-gate animation.
9. **Use the Okabe–Ito palette** and check text contrast ≥ 4.5:1 and non-text ≥ 3:1. Those AA thresholds come from WCAG 2.1 (1.4.3/1.4.11) and were not re-verified in this session. Support light and dark modes.
10. **Optional sonification**, as a differentiator: map measurement probabilities to pitch or loudness, and syndrome flips or decoder corrections to distinct earcons, using Web Audio. Chart2Music handles line and bar charts.
11. **Write descriptions in PhET style:**
    - A scene summary at the top ("You are exploring a 3-qubit repetition code…").
    - Hints.
    - Context responses after each action ("Bit flip on qubit 2. Syndrome now reads 1 1. The decoder flips qubit 2 back.").
12. **Use the PhET "A11y View" idea:** a visible "Description log" panel that mirrors the live-region text helps sighted judges see the accessibility work, and helps the demo video show it.
13. **Test** with keyboard only, then NVDA + Chrome. Run axe DevTools or Lighthouse on the rendered page locally before publishing.

### Gaps
- PhET's current official Interactive Description design patterns (patterns 1–7) and templates weren't retrievable. The phet.colorado.edu feature pages render client-side and came back empty.
- I don't know how Qollab's host page (toolbar, console, 🚀 loading overlay) affects screen-reader flow around the embedded project frame. That's outside the team's control, but worth checking.

---

## Q6. Which hackathon-grade engineering patterns make the project reliable for judges (precomputed data, seeds, fallbacks, single-batch IonQ jobs, fast first run, progressive disclosure, self-checking quizzes, concept-inventory pre/post)?

### Takeaway
Follow the official Soundtrack and QCFlows playbook:
- Exact `Statevector`/`Clifford` math in Python for all teaching visuals, with no backend.
- **One** composite circuit sent through **one** `backend.run` from JS, inside try/catch with a visible fallback.
- **Precomputed noisy/IonQ results shipped as JSON** and read in Python by literal path.
- Deterministic seeds.
- JSON-string bridge, DOM-mount wait, keep-alive promise.
- Never `job.get_counts()` and never `BackendSamplerV2` on IonQ.

Add a short JS pre/post concept check modeled on validated QIS inventories (QISCIT, QCCS), with results kept in memory only.

### Cited Findings
**Soundtrack pattern**
- **Ships precomputed IonQ data.** It bundles `data/forte_takes.json` (17.9 KB) of real IonQ Forte measurements, loaded with `open("data/forte_takes.json")` inside `try … except OSError`.
- **Packs one circuit:** "Remote backends on Qollab take ONE circuit per run, so everything this run measures is packed side by side on separate qubits of a single circuit… 8 + 12 = 20 qubits, which fits every Qollab backend". It composes sub-circuits onto disjoint qubit ranges and calls `measure_all()`.
- **Decodes per register** with bit-shifts: `(v >> offset) & ((1 << w) - 1)`.
- **Uses a fixed basis transpile:** `transpile(qc, basis_gates=BASIS, optimization_level=1)`, "so no backend (and no network) is needed".
- **Shows its data source.** The UI has three source buttons, "IonQ Forte take" / "Ideal simulation" / "This run". On failure: "The job did not complete on ${backendName()}, so chords use ideal sampling."
- **Keeps runs small and deterministic:** 128 shots and render seed 7.

— [Soundtrack `service.py`/`main.js`/`circuits.py`](https://qollab.xyz/u/qollab/quantum-hackathon-soundtrack)

**QCFlows pattern**
- Metrics come from the exact Statevector. The backend is used only for an optional "Sample on QPU" button, which reports measured versus ideal with total variation distance.
- The app "itself never spends credits".
- The README tells the user which backend to pick ("Press Run… and pick the Built-in simulator").

— [QCFlows](https://qollab.xyz/u/qollab/qcflows-multifile)

**Determinism and noise on hardware**
- `BasicSimulator` accepts a `seed_simulator` run option; otherwise it draws a random seed. — [qollabxyz/qiskit basic_simulator.py](https://raw.githubusercontent.com/qollabxyz/qiskit/main/qiskit/providers/basic_provider/basic_simulator.py)
- IonQ hardware: debiasing is on by default at ≥ 500 shots, and `DebiasingError` needs at least 500 shots. IonQ cost depends on post-compilation 1Q/2Q gate counts plus shots, with an N-qubit gate counted as 6(N−2) 2Q gates. — [How credits work](https://qollab.xyz/learn/docs/how-credits-work); [Error reference](https://qollab.xyz/learn/docs/error-reference)

**Judging and outages**
- Judges "press Run on a free simulator". Hardware versus simulator "is not scored". — [Qollab How it works (FAQ)](https://qollab.xyz/programs/hackathon/how-it-works)
- Rules: projects must "Run on Qollab's free simulators, including IonQ's quantum simulator." — [Rules & Terms](https://qollab.xyz/programs/hackathon/terms)
- Outages of more than 12 hours may extend the deadline. — [Rules & Terms](https://qollab.xyz/programs/hackathon/terms) (via earlier notes)

**Error handling**
- The Quantum Garden project catches a qiskit-ionq parsing `AttributeError` and prints "qiskit-ionq SDK parsing bug — check API key and backend target". The general fix is to "Wrap the submit call in `try`/`except`". — [Error reference](https://qollab.xyz/learn/docs/error-reference)

**Validated concept inventories for a pre/post check**
- **QISCIT (Quantum Information Science Concept Introductory Test):** 31 items, content-validated with 11 QIS experts, openly shared. It covers states, measurement, qubits, entanglement, decoherence, gates and communication, and needs no college-level math. — [arXiv 2506.17122](https://www.arxiv.org/pdf/2506.17122)
- **QCCS (Quantum Computing Conceptual Survey):** validity and reliability evidence via Classical Test Theory and Rasch modeling. — [arXiv 2608.14459](https://arxiv.org/pdf/2608.14459); [APS 2025 abstract](https://meetings-archive.aps.org/smt/2025/apr-s22/6/)
- **Discussion of a QC concept inventory:** "The Benefits and Challenges of a Quantum Computing Concept Inventory". — [arXiv 2512.20836](https://arxiv.org/pdf/2512.20836)
- **The FCI/FMCE precedent:** giving the same test at start and end measures teaching effectiveness. — [search summary of concept-inventory literature](https://arxiv.org/pdf/2512.20836)

### Inferences
**Recommended architecture for a Quantum Unlocked tool**

1. **Python layer (`edu/*.py`)** holds pure functions that take JSON and return JSON:
   - `explain_state(circuit_json)` returns amplitudes, Bloch vectors, reduced density matrices and entropies via `Statevector` / `partial_trace`.
   - `qec_round(params_json)` runs a Clifford-based syndrome extraction plus a networkx MWPM decoder.
   - `build_backend_circuit()` returns the **single** composite circuit (≤ 20 qubits, fixed-basis transpile).
   - `score_counts(counts_json)` returns per-register results with TVD versus ideal.
2. **JS layer:**
   - `main.js` waits for the DOM, calls `explain_*` for instant visuals, and renders with three.js, SVG or KaTeX.
   - Then it does exactly one `await backend.run(circuit, {shots: 256..1000})` inside try/catch and labels the result source.
   - It ends with `await new Promise(() => {})` only if later buttons need the backend.
3. **Shipped data:** `data/ionq_forte_sim.json` (counts recorded from the IonQ Forte noise-model simulator during development, with date, backend, shots and seed), plus `data/ideal.json`. The page always has meaningful content even if the judge's backend fails or is slow.
   - Capture from the free IonQ remote simulator by running once and copying the console output.
   - Optionally add an IBM noise-model run.
   - Label everything honestly ("recorded on IonQ Forte 1 noise-model simulator, 2026-10-10").
4. **Seeds:** `seed_simulator` on BasicSimulator/Aer runs, `seed_transpiler` on transpiles, and a fixed NumPy `default_rng(seed)`. The demo video and the judge's run then show the same numbers on ideal backends.
5. **Fast first run:**
   - Avoid heavy presets (Nature/PySCF, ML, PQCA/Aer) unless essential.
   - Keep `requirements.txt` empty or tiny; pyzx adds about 3 s.
   - Render a static explanatory first screen from HTML/CSS immediately, before Python finishes loading.
   - Show progress text in an `aria-live` status element.
6. **Progressive disclosure:**
   - Level 1 is an intuition (one qubit, Bloch sphere, sliders).
   - Level 2 is the mechanism (multi-qubit, entanglement, syndrome).
   - Level 3 is "real hardware" (the IonQ comparison).
   - Use `<details>`/`<summary>` or `aria-expanded` sections, as QCFlows does, plus "Next step" guidance.
7. **Self-checking quiz:**
   - Write a small JS module with multiple-choice and "predict the outcome" items.
   - Before a gate is applied, ask the learner to predict the probabilities, then reveal the simulation. This is a "predict–observe–explain" loop.
   - Give immediate feedback in an `aria-live="polite"` region, with explanations tied to the visualization.
   - Use native radio inputs inside a `<fieldset>`/`<legend>`.
8. **Pre/post concept check:**
   - Write 5–6 original items covering the same constructs as QISCIT/QCCS (superposition vs. mixture, measurement collapse, entanglement and local measurement, decoherence, error-syndrome meaning).
   - Don't copy inventory items verbatim; check each instrument's license first.
   - Show the pre score, the post score and the normalized gain g = (post − pre)/(100 − pre), Hake's metric (not re-verified this session).
   - Storage is unavailable, so results live only in memory. Offer "Download my results (JSON)" via Python `sendFile`, which is the documented path.
9. **Portability checklist:**
   - Use `job.result().get_counts()`, and handle the list-of-dicts case.
   - Use no `BackendSamplerV2` on IonQ, and one `BackendEstimatorV2` call if using Estimator.
   - Keep circuits to ≤ 20 qubits.
   - Send no mid-circuit measurements to the built-in simulator.
   - Avoid gates outside the common basis (transpile first).
   - Wrap backend calls in try/catch with fallback data.
   - Test on the Built-in, AWS Braket local, one IBM noise model, and the IonQ Forte remote simulator before publishing.
10. **Browser note for the README and project page:** "Requires Chrome/Edge/Opera (recent) or Firefox 153+; Safari is not supported by the Qollab runtime (JSPI)". Also mention keyboard shortcuts and the accessibility features. This helps the Documentation Quality score.

### Gaps
- I couldn't verify whether `sendFile` is callable directly from JS. The Soundtrack only calls it from Python.
- I don't know whether judges are signed in when pressing Run. Anonymous runs of quantum jobs may be refused per the error reference, which suggests judges must be signed in.
- No public data shows how long Qollab's first-run Pyodide + Qiskit load takes on a typical judge machine, so measure it during the build.
- The QISCIT and QCCS licenses for item reuse weren't checked.
