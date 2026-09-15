# Language, execution, and media contract

**English** | [한국어](../ko/reference/languages.md)

**English is the default documentation language; Korean remains a complete path. Each language has separate recordings.**

## Documentation

English lives in `README.md` and `docs/`; Korean lives in `README.ko.md` and `docs/ko/`.
Every page links to its counterpart.
Temporary Korean-first deferrals are bounded by hashes and visible warnings in `docs/localization.json`.
After English expansion, remove those deferrals and recheck command parity.

## Runtime data and answers

English has its own v1/v2 prompts, six policies, dev/holdout/calibration datasets, and offline fixtures.
Use `--language en` for English execution; existing commands keep Korean by default.
The [data bundle](../../data/README.md) preserves original Korean files and pins separate translation hashes.
IDs, limits, effective dates, decisions, and required citations are checked for equivalence.
Translated text is a different dataset and is never an error-triggered substitute.
English development instructions were frozen before preparing the translated final holdout.

Do not translate model/API identifiers, filenames, CLI flags, or schema field names.
Never substitute another language's fixture or model response after an error.

## Independent capture

Korean/English use separate prompts/data, browser locales, action labels, CLI/portal source recordings,
screenshot directories, edited videos, and native evaluation runs.
Renaming one movie does not make it two independent language editions.
Chapter cards, actual app views, offline fixtures, live Azure calls, diagnostics, and controlled comparisons are labeled.

Replace older media only after both new language sets pass playback and link validation.
Preserve original evaluation/failure and prompt/dataset/corpus/response/evaluator lineage.

## Validation

```bash
python scripts/check_docs.py
```

Commands and local links are checked in both languages.
Unrecorded deferrals or command drift fail; English execution results are not copied into Korean scores.
