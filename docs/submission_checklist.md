# Submission checklist: one project, two submissions

**Deadline for both: Sun Oct 11, 2026, 19:00 ET.** Aim to have everything in by **17:00**. Qollab entries can be edited until the deadline.

## A. Qollab × IonQ (global hackathon, Georgia Tech node)

- [ ] **Project created on the captain's own Qollab profile.** Only the creator can edit it, and only a public project owned by the captain or a joined teammate can be submitted.
- [ ] **Uploaded the latest `five_tests_priced/` folder** (New Project → Upload your own files, or an existing project → upload). It contains:
  - `main.py`, `ftp_core.py`, `ftp_classical.py`, `ftp_quantum.py`, `ftp_report.py`;
  - `README.md` (this becomes the write-up / project page);
  - `LICENSE`, `DATA_NOTICE.md`;
  - `data/heart_cleveland_297.csv`, `results/precomputed.json`, and `results/forte_cache.json` if present.
- [ ] **Runs on Built-in simulator** with default settings (seconds). The first line of the output shows the expected `build ...` id.
- [ ] **Runs on IonQ Forte 1 simulator** with default settings, in **one job**. This is required by the organizers for the IonQ track.
- [ ] Optional: runs on one IBM noise model (defaults to 8 shots) and AWS Braket local.
- [ ] **Published as public.** Public Qollab projects are MIT-licensed automatically; `LICENSE` is included too.
- [ ] **The write-up covers everything the rules ask for:**
  - what it does and the problem it explores;
  - how to run it, and how to replicate or extend it;
  - what existed before the window;
  - credits and AI use;
  - the attribution line **"This effort is supported by Qollab & IonQ"**.
- [ ] **Demo video, 2–3 minutes,** at a public link that opens **without signing in** (YouTube unlisted / Loom / Vimeo / Google Drive "anyone with the link"). Captions uploaded (`docs/video_script.md`).
- [ ] **Submitted from the Qollab registration page by the captain:**
  - pick the project;
  - **Theme = Impact**;
  - paste the video URL;
  - optional: "Dependencies and environment" = "Qiskit 2.5 + NumPy; scikit-learn and matplotlib only for optional output; no extra installs";
  - optional: "What didn't work?" = the honest caveats (no speedup; prices from 1992; IonQ simulator returns rounded counts);
  - tick the rules box → submit.
- [ ] **Re-submit / update after any later change** before 19:00 ET.

## B. Georgia Tech Qiskit Fall Fest (IBM track, judged by QCA)

- [ ] **The GitHub repo is public:** https://github.com/SamanyuB910/QC-Project. Check in a private window.
- [ ] **The repo README** links to the Qollab project and the video.
- [ ] **QCA's Fall Fest submission form**, posted on the GT Discord, submitted with the **GitHub link** and the **demo video link**.
- [ ] Optional: Demo Day, **Fri Oct 16, 16:00–18:00 ET**, is a presentation event, not a deadline.

## C. Final checks before submitting

- [ ] `pytest tools/tests` passes locally.
- [ ] The latest commit is pushed to `main`, and the uploaded Qollab files are the same version (compare the `BUILD` line).
- [ ] The video numbers match what the final Run prints.
- [ ] The video and GitHub links open while signed out.
- [ ] Keep the Qollab project available for 12 months (rules).
