# AI Usage — ML Stage

**Author:** Ali Efe Okudan (34314)
**Course:** DSA210 — Introduction to Data Science (Spring 2026)
**Stage:** Machine-Learning Methods Application
**Date:** 2026-05-05

This document discloses how AI assistance was used during the ML stage of the
project, in line with the DSA210 academic-integrity guidelines on AI use.

---

## Tool used

- **Claude (Anthropic)** — interactive coding assistant. Used through a chat
  interface with file-system access for editing notebooks and running scripts.
  No model fine-tuning, automation pipeline, or third-party AI service was used.

## Scope of AI assistance

AI was used as a *support* tool, in clearly bounded ways. The research
question, hypotheses, dataset choices, modelling decisions, interpretation of
results, and conclusions are my own — based on the EDA stage of this project
and on material covered in DSA210 lectures.

The table below lists each task and who did it.

| Task | Done by me | AI assistance |
|---|---|---|
| Project topic & research question | ✅ | — |
| Hypothesis formulation (H1, H2, H3) | ✅ | — |
| Choice of data sources (yfinance, pytrends, SteamDB) | ✅ | — |
| Choice of target (`steam_trends_z` as TR-specific gaming proxy) | ✅ | — |
| Choice of train/test split strategy (chronological, 6-month holdout) | ✅ | — |
| Decision to compare regularised linear models against tree models | ✅ | — |
| Interpretation of holdout results in light of EDA findings | ✅ | — |
| Final report writing (this folder's `REPORT.md`) | ✅ | — |
| Boilerplate Python imports / cell scaffolding | ✅ | Suggested cell structure |
| `sklearn` API usage (`Pipeline`, `TimeSeriesSplit`, `GridSearchCV`) | ✅ | Reference reminders |
| Plot styling (axes, legends, savefig) | ✅ | Snippet templates |
| Markdown formatting of result tables | ✅ | Formatting suggestions |
| Debugging shape/index mismatches | ✅ | Error-message diagnosis |

## What AI did *not* do

- AI did **not** decide the research question, hypotheses, or dataset.
- AI did **not** select features or evaluate which model "should win".
- AI did **not** write the report's discussion or conclusions; those are my
  interpretation of the numbers produced by my code.
- AI outputs were **not** copied verbatim without inspection. Every numeric
  result in the report was reproduced by running the notebooks on
  `merged_dataset.csv` myself.
- AI did **not** fabricate any data. All values come from the CSV produced
  by `data_processing.py` in the data stage.

## How I verified AI suggestions

1. Ran every cell suggested by AI in the notebook and inspected the output
   before keeping it.
2. Cross-checked sklearn snippets against the
   official scikit-learn documentation (e.g. `TimeSeriesSplit`,
   `Pipeline`, `permutation_importance`).
3. Compared model results against a hand-coded persistence baseline
   (`ŷ_t = y_{t-1}`) to make sure the reported RMSE values are sensible.
4. Re-ran the notebooks end-to-end after the final folder reorganisation to
   confirm reproducibility.

## Examples of how AI was used (representative, not exhaustive)

- *"What is the right way to keep StandardScaler from leaking test data into
  training when using TimeSeriesSplit?"* — produced a `Pipeline` snippet that I
  adapted to my variable names.
- *"My RMSE looks suspiciously low; could it be label leakage?"* — checked my
  feature list together; concluded the issue was that `steam_players_z` was
  globally z-scored before the split (acceptable for this assignment, noted in
  Limitations).
- *"How do I display feature importance for both linear and tree models in one
  bar chart?"* — produced a matplotlib template I then re-styled.
- Spotting typos in markdown tables and inconsistent column ordering.

## Reproducibility

Anyone can reproduce all numbers in the ML stage by running:

```bash
pip install -r requirements.txt
python data_collection.py
python data_processing.py
jupyter notebook ML/34314_AliEfeOkudan_ML.ipynb
jupyter notebook ML/ML_Project/ml_implementation.ipynb
```

The notebooks contain fixed random seeds (`random_state=42`) where
applicable, so results are deterministic.

---

## Note on this document

For full transparency: the first draft of this `AI_USAGE.md` itself was
produced with the same AI assistant (Claude). I read it line by line, edited
the wording where it did not match what actually happened, removed claims I
could not personally verify, and kept only the parts that I would stand
behind in person. The structure (headings, table layout) is the AI's
suggestion; the content of every entry — who did what, what AI did *not*
do, the verification steps — is mine.

---

*This disclosure is provided in good faith and follows the spirit of the
DSA210 AI-use policy. Any further questions about how a specific cell or
result was produced can be answered by reference to the corresponding
commit history and the notebooks themselves.*
