# Synthetic data and language bundles

**English** | [한국어](README.ko.md)

These are fictional Hanbit Technology workshop assets, not company policies.

| Asset | Korean source | English version |
|---|---|---|
| Six policies | `knowledge/policies.json` | `knowledge/en/policies.json` |
| Six dev cases | `evaluation/dev.jsonl` | `evaluation/en/dev.jsonl` |
| Four final holdout cases | `evaluation/holdout.jsonl` | `evaluation/en/holdout.jsonl` |
| Correct/incorrect judge fixtures | `evaluation/calibration.jsonl` | `evaluation/en/calibration.jsonl` |
| Offline answer fixtures | `fixtures/answers.json` | `fixtures/en/answers.json` |
| v1/v2 instructions | `../prompts/v1.txt`, `../prompts/v2.txt` | `../prompts/en/v1.txt`, `../prompts/en/v2.txt` |

Select the English bundle explicitly:

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
