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

## Step 1: v0 safety entry (target Sat 21:00)

1. **Upload.** Qollab → New Project → **Upload your own files**. Drag in the whole `five_tests_priced/` folder, or a zip of it (one wrapping folder is stripped automatically). The folder's `README.md` becomes the project write-up.
   - Files: `main.py`, `ftp_core.py`, `ftp_classical.py`, `ftp_quantum.py`, `ftp_report.py`, `README.md`, `LICENSE`, `DATA_NOTICE.md`, `data/heart_cleveland_297.csv`, `results/precomputed.json`.
   - **The captain should create it on their own profile.** Only the creator can edit it, and only the captain or a joined teammate's public project can be submitted.
2. **Run on Built-in simulator** with default settings. It should finish in seconds. Paste the output back to me.
3. **Run on IonQ Forte 1 (remote simulator)** with defaults (`circuits = auto`, `shots = 0`, which means 500 per circuit). Accept the consent dialog if one appears; the simulator is free. Paste the output back.
   - If it prints `JOB FAILED`, press Run again with `circuits = single` and paste that too.
4. **Publish** → choose a version name → visibility **public**. Public Qollab projects are automatically MIT-licensed.
5. **Record a quick placeholder video.** The registration form *requires* a video URL. A 2–3 min screen recording of the Run plus the write-up is fine for now (Loom/YouTube/Drive, viewable without sign-in). Replace it with the real video on Sunday.
6. **Submit from the Qollab registration page** (captain):
   - pick the project;
   - **Theme = Impact**;
   - paste the video URL;
   - optionally fill "Dependencies and environment": "Qiskit 2.5 + NumPy; no extra packages";
   - tick the rules box;
   - submit.

   You can edit and re-submit until Sun Oct 11, 19:00 ET.
7. **Optional, so its queue time overlaps sleep:** run IonQ Forte 1 again with `dump_counts = true` and paste the `COUNTS_JSON ...` line. I'll store it as the cached IonQ result.
