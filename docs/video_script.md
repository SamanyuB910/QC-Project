# Demo video script: "Five Tests, Priced" (target 2:40, hard limit 3:00)

**Format.** Screen recording with voiceover. Showing your face is not required.

**Record in:** Chrome, Edge, Brave, Opera or Firefox 153+ (not Safari).

**Host on** YouTube (unlisted), Loom, Vimeo or Google Drive with "anyone with the link". Check that the link opens while signed out.

**Captions.** Upload this transcript as captions (YouTube: *Subtitles → Upload file → "Without timing"*). This also covers accessibility.

**Before recording:**
- Open the Qollab project page.
- Run it once on **Built-in simulator** so the output is ready to scroll.
- Have the GitHub repo open in a second tab.

---

| Time | Screen | Voiceover (say this) |
|---|---|---|
| 0:00–0:15 | Project title on the Qollab page; press **Run** | "A chest-pain clinic can afford five heart tests per patient. Which five, and what does each extra dollar buy? This is QCA's Prompt B, with one change: the tests now have real prices." |
| 0:15–0:35 | Section 1: shared-procedure table | "We use the UCI Cleveland heart-disease data, 297 patients and 13 measurements, plus published test costs from the Ontario fee schedule. Some tests share a procedure: one treadmill ECG gives three readings, so you pay for the treadmill once. That makes cost non-additive, and it becomes a three-qubit term in the circuit." |
| 0:35–1:00 | Section 2: classical table; point at "greedy" | "Classical first. Exhaustive search over all 1,287 five-test panels takes milliseconds, so we always know the true answer. The obvious shortcut, greedy selection, misses it at three of five price points, once picking only the 26th-best panel. The prompt's formula as written is easy; with real prices it is not." |
| 1:00–1:30 | Section 3: circuit build line, prediction table, "submitting ONE job" | "The quantum step: 13 qubits, one per test, one circuit per price point, all five in a single job; on IonQ, which takes one circuit per job, we send the most price-sensitive circuit. The circuit can only swap a test in for a test out, so every sample has exactly five tests. We dropped the prompt's penalty term, because any penalty you can choose without knowing the answer made QAOA no better than random. The circuit matches an exact model to ten to the minus fifteen." |
| 1:30–2:00 | Prediction table, then section 4 results | "Before the job runs, the program prints its prediction: one 1,000-shot job should find every optimal panel 98 percent of the time. A sampler with the same per-test odds but no correlations manages 63 percent, and random panels 11. Simulated annealing and local search, given the same number of evaluations, reach 55 and 63 percent. Under IonQ's older noise rates: 92 percent. On IonQ's current noise model it missed; a probe job shows the gates run correctly, so that is noise, and we report it as registered." |
| 2:00–2:25 | Section 5 evidence; price-ladder figure | "Here is the clinic's answer: three history questions alone reach AUC 0.84; one treadmill ECG at 91 dollars reaches 0.875; adding fluoroscopy, 0.90. Two checks we registered before running both passed, and the numbers re-selected on held-out patients are printed honestly next to the optimistic ones." |
| 2:25–2:40 | Section 6 "does not claim"; GitHub tab | "What we don't claim: no speedup. Exhaustive search is exact and instant at 13 tests. What we show is sample quality, and that on all-to-all trapped ions the circuit needs about a third of the two-qubit gates it needs on a heavy-hex lattice: 238 versus about 775. Code, tests and data notice are on GitHub. This effort is supported by Qollab and IonQ." |

---

**After recording:**
1. Paste the link into the Qollab registration page ("Demo video URL") and into QCA's Fall Fest form.
2. Open the link in a private window to confirm it plays without signing in.

> **Check before recording.** Replace the numbers above with whatever your final Run prints: the "Precomputed evidence" table, the check results, and the gate ledger. Say only what the screen shows.
