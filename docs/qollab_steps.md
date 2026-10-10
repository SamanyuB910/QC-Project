# Qollab steps for the team (you do these; paste the outputs back)

Use Chrome, Edge, Brave, Opera or Firefox 153+. **Safari cannot run Qollab projects.**

## Step 0: smoke test (now, about 20 min)

1. In Qollab, create a **new scratch project**, e.g. "ftp-smoke". Licence: MIT. It can stay private or unlisted.
2. Upload these four files from `tools/qollab_smoke/`, **keeping the `data/` folder**:
   - `main.py`
   - `ftp_smoke_helper.py`
   - `smoke_data.json`
   - `data/heart_cleveland_297.csv`
3. Press **Run** once per backend, with these Run settings (the form generated from `main()`):

   | # | Backend | `mode` | `shots` | `statevector_check` |
   |---|---|---|---|---|
   | 1 | Built-in simulator | `list` | `200` | `true` |
   | 2 | IonQ **Forte 1** (remote simulator) | `list` | `50` | `true` |
   | 3 | *Only if run 2 printed `JOB FAILED`:* IonQ Forte 1 | `single` | `50` | `false` |
   | 4 | Any IBM noise model (e.g. Fez) | `list` | `4` | `false` |
   | 5 | AWS Braket local simulator | `list` | `200` | `false` |

4. **Copy the entire output of each run** and paste it back in chat, labelled with the run number.
5. Also tell me:
   - Did a small plot appear in run 1?
   - Did the `press counter` ever show 2 or more? (That means state persists between presses.)
   - How did you add the files? (Upload button, drag-drop, one at a time, folders?)

What I'm checking:
- whether a **list of circuits counts as one IonQ job**;
- whether the sign convention holds in Qollab's Qiskit (`P(opt|HW5) ≈ 0.015`);
- whether multi-file imports and literal-path data reads work;
- which packages exist (scikit-learn, matplotlib);
- timings;
- whether IonQ returns properly sampled counts.

## Step 1: v0 safety entry (after I push Phase 1, target Sat 21:00)

Filled in when Phase 1 lands: upload the `five_tests_priced/` folder, run, **publish (MIT)**, and **submit from the Qollab registration page with theme = Quantum Impact**.
