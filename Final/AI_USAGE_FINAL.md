# AI Usage — Final Report Stage

**Author:** Ali Efe Okudan (34314)
**Course:** DSA210 — Introduction to Data Science (Spring 2026)
**Stage:** Final report and code submission (18 May 2026)
**File this disclosure covers:** `Final/FINAL_REPORT.md` and the
overall `Final/` folder reorganisation.

This document discloses how AI assistance was used during the **final
report** stage. Two earlier disclosures cover the previous stages:

- EDA stage → "AI Usage Log" section in `34314_AliEfeOkudan_EDA.ipynb`
- ML stage  → `ML/AI_USAGE.md`

---

## Tool used

- **Claude (Anthropic)** — interactive coding/writing assistant, used
  through a chat interface with file-system access. No automation
  pipeline, model fine-tuning, or third-party AI service was used.

## What AI helped with

| Task | Done by me | AI assistance |
|---|---|---|
| Choice of "what counts as the final deliverable" | ✅ | — |
| Section list for `FINAL_REPORT.md` (Motivation → Future Work) | ✅ | Suggested outline aligned with the course guidelines |
| Recycling EDA / ML results into the report's tables | ✅ | Reformatted my existing tables into a single style |
| Wording of motivation, findings, limitations, future work | ✅ | First-draft prose that I rewrote in my own voice |
| Decision to create a self-contained `Final/` folder | ✅ | Suggested the `Final/figures` + `Final/data` layout |
| `.gitignore` content | ✅ | Suggested standard Python / macOS entries |
| Updating `requirements.txt` (adding `nbconvert`) | ✅ | Diagnosed missing dependency |
| Final numbers and verdicts (r, p, RMSE, R², coefficients) | ✅ | — (taken verbatim from my notebooks) |

## What AI did *not* do

- AI did **not** invent any number, figure, or table in the final report.
  Every quantitative claim is traceable to the EDA notebook
  (`34314_AliEfeOkudan_EDA.ipynb`), the ML notebook
  (`ML/34314_AliEfeOkudan_ML.ipynb`), or the companion notebook
  (`ML/ML_Project/ml_implementation.ipynb`).
- AI did **not** decide which hypotheses were supported.
- AI did **not** decide the final-folder structure on its own — the
  decision to bundle a self-contained submission folder was mine; AI
  proposed a concrete layout I then accepted.
- No AI-generated text was kept without me reading it line by line.

## How I verified AI output

1. Cross-checked every number in `FINAL_REPORT.md` against the
   corresponding cell output in the notebooks.
2. Re-opened each referenced figure (in `Final/figures/`) and confirmed
   it actually shows what the report describes.
3. Re-read the limitations and conclusions to make sure they match the
   limitations I already wrote in `ML/AI_USAGE.md` and
   `ML/ML_Project/REPORT.md`.
4. Confirmed reproducibility instructions in §10 of the final report
   match what I actually ran.

## Reproducibility

The final report does not introduce any new computation. Running

```bash
pip install -r requirements.txt
python data_collection.py
python data_processing.py
jupyter notebook 34314_AliEfeOkudan_EDA.ipynb
jupyter notebook ML/34314_AliEfeOkudan_ML.ipynb
```

reproduces every number, table, and figure referenced in `FINAL_REPORT.md`.

---

## Note on this document

For full transparency: the structure of this disclosure (headings, table
layout) follows the same template as `ML/AI_USAGE.md`. The text was
drafted with AI assistance and then edited so every claim about what AI
did or did not do is accurate for the **final-report stage specifically**.
The structure is AI's suggestion; the truth of each entry — who did
what — is mine, and I stand behind it.
