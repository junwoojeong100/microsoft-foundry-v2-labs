# Synthetic data and language bundles

**English** | [한국어](README.ko.md)

These are fictional Hanbit Technology workshop assets, not company policies.

| Asset | Korean original | English version |
|---|---|---|
| Six policies | `knowledge/policies.json` | `knowledge/en/policies.json` |
| Six dev cases | `evaluation/dev.jsonl` | `evaluation/en/dev.jsonl` |
| Four final holdout cases | `evaluation/holdout.jsonl` | `evaluation/en/holdout.jsonl` |
| Correct/incorrect judge fixtures | `evaluation/calibration.jsonl` | `evaluation/en/calibration.jsonl` |
| Offline answer fixtures | `fixtures/answers.json` | `fixtures/en/answers.json` |
| v1/v2 instructions | `../prompts/v1.txt`, `../prompts/v2.txt` | `../prompts/en/v1.txt`, `../prompts/en/v2.txt` |

From the repository root, select the English bundle explicitly:

```bash
python scripts/workshop.py --language en doctor
python scripts/workshop.py --language en demo --label english-offline --prompt v2
```

The default remains Korean for existing commands. No missing English file or failed request falls back to Korean.
Language selection is frozen in Hosted profiles and preserved in dataset/prompt/corpus hashes.
Do not compare different-language datasets as an isolated model or prompt experiment.

`localization.json` pins source and translation hashes. IDs, dates, amounts, decisions, and required citations remain equivalent,
but translated text has its own dataset hash. English development assets and effective workflow instructions were frozen
before the translated holdout was prepared. Holdout is final-acceptance material only.
Fixtures are prewritten examples, never Azure responses.

## Ready browser materials

[English learner ZIP](learner/en/learner-materials.zip) · [Korean learner ZIP](learner/ko/learner-materials.zip) · [Setup and file-by-file use](../docs/setup.md)

`data/learner/<language>/` is generated from that language's canonical v2 prompt, six policies and **dev only**.
It includes inline/browser instructions, six TXT sources, questions without reference-answer fields, and a blank six-row assessment.
Blank `session-notes.txt`, `workflow-review.txt` and `operations-checklist.txt` guide setup, observations,
pause/resume and final handoff. They contain no completed results; fill personal copies outside the repository
or B's Git-ignored `outputs/learner-notes-en/` directory, never the generated files under `data/learner/`.
The browser-only prose override is explicit; it does not change the frozen prompts or evaluation data.
`SOURCE.json` and the per-file manifest retain input/output hashes. The ZIP excludes holdout and answer keys.

Maintainers check the committed bytes with `python scripts/build_learner_materials.py`;
`--write` explicitly regenerates both bundles. Learners save their filled worksheets elsewhere, not in this generated directory.
