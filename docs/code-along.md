# Code-along: predict, break and repair the SDK contracts

**English** | [한국어](ko/code-along.md)

**Finish with your own code copies, a failed check that you can explain, and a repaired result.**
This optional practice follows B's core handoff or [Lab 00's local setup](labs/00-start.md#path-b).
It is not another required A/B lab.

**Mode:** installed SDKs with fixed, synthetic test responses. **No Azure sign-in, model calls, deployment or `.env` is needed.**
Both guide languages use the same **English test fixtures**, not a new English/Korean model comparison.
The checker tests API wiring; it does not measure answer quality.

## 1. Prepare the local practice environment

Use the source repository root, Bash/zsh (WSL on Windows), and an active Python **3.13** virtual environment.
Keep your existing `.venv`; do not replace it or reinstall a working environment.
For a new environment, use [Lab 00 step 3](labs/00-start.md#3-install-a-virtual-environment-and-sdks),
then return here **before** its `.env` and Azure sign-in steps.

This optional practice covers the Hosted adapter as well, so it needs the full SDK set.
If it is not already installed in this environment:

```bash
python -m pip install -r requirements.lock.txt -e ".[cloud,agents,hosted,dev]" &&
python -m pip check
```

Package downloads need internet access; running the exercises below does not need Azure.
Do not add credentials to make a mock test pass.

## 2. Make a personal copy once

The six small recipes are complete starting points, not production replacements for the workshop CLI.
Do not edit `examples/recipes/`, `src/`, `prompts/`, `data/` or the tests for these exercises.
Do not interrupt a Lab 07 comparison to change its inputs.

```bash
mkdir -p outputs &&
mkdir outputs/code-along-en &&
cp examples/recipes/{02_responses.py,03_prompt_agent.py,04_maf_tool.py,05_maf_sequential.py,06_iq_retrieve.py,08_hosted_agent.py} outputs/code-along-en/
```

The chain stops if the destination already exists. For this pass, reopen your existing copies instead of copying over them.
For another pass, choose a new directory and change every command below consistently.

| Open in your copy | Find this code | Explain before running |
|---|---|---|
| `02_responses.py` | `client.responses.create`, `store=False` | Which model is called, and which service IDs return? |
| `03_prompt_agent.py` | `create_version`, `agent_reference` | Why invoke the returned version instead of `latest`? |
| `04_maf_tool.py` | `@tool`, `lookup_policy`, `tools=[...]` | Who executes the function? What does no matching evidence mean? |
| `05_maf_sequential.py` | `SequentialBuilder(participants=[analyst, writer])` | Which role runs first, and which output is returned? |
| `06_iq_retrieve.py` | `/knowledgebases(`, `api-version`, `raise_for_status` | Why must a failed IQ request remain an error? |
| `08_hosted_agent.py` | `ResponsesHostServer`, `build_server` | Why does serving a protocol locally not prove a deployment? |

Read the functions named in the table, not just the `main()` entry points.
**Do not run these copied `.py` files directly**: their `main()` functions are real Azure examples.
Use only `scripts/check_recipes.py` for this offline exercise. Its fixed transports and policy fixtures are selected before testing,
never substituted after a live failure. The socket guard is an extra safeguard, **not a security sandbox**; run only your trusted copies.

## 3. Check the unchanged copies

```bash
(
  set -C
  python scripts/check_recipes.py --directory outputs/code-along-en > outputs/code-along-en/check-baseline.json
)
```

The checks print to the terminal; the JSON summary is saved in `check-baseline.json`.
The parentheses limit `set -C` to this block. It refuses an existing output file **before** running Python.
Use a new report name for a new attempt; do not erase an earlier result to make room.

**Check:** open the JSON. Require `mode: offline-sdk-practice`, `status: passed`, `tests_run` equal to `tests_expected`,
zero `failures`, `errors`, `skipped` and `expected_failures`, and `source_unchanged: true`.
Keep `azure_tested: false` and `model_quality_measured: false`.
The test, recipe and fixture hashes identify what this check used.
If the unchanged copy fails, resolve that failure before deliberately breaking anything.

## 4. Break one contract, then repair it

In **your copy** of `02_responses.py`, find `store=False` inside `ask` and change only that value to `store=True`.
Predict which assertion should fail: the request must not silently change its storage behavior.

```bash
(
  set -C
  python scripts/check_recipes.py --directory outputs/code-along-en > outputs/code-along-en/check-store-broken.json
)
```

**Expected failure:** exit code `1`, `status: failed`, and a failure in
`test_responses_recipe_returns_service_ids_without_storing`.
This is a mock request, not an actual stored Azure response. A missing package or syntax error is a different failure;
read the terminal message instead of counting every red result as the intended lesson.

Restore `store=False` in that same copy, then run:

```bash
(
  set -C
  python scripts/check_recipes.py --directory outputs/code-along-en > outputs/code-along-en/check-store-repaired.json
)
```

**Check:** the repaired run passes all selected checks. Compare its recipe hash with the baseline; an exact byte-for-byte repair has the same hash.
Keep all three summaries, including the failed one. Explain the change and its consequence in your own notes.
Do not edit the test, its expected value or the saved JSON to obtain a pass.

## 5. Optional: practise two more mistakes

Try one row at a time, restoring it before the other. These are changes to your copies only.

| File | Deliberate mistake | Check that should reject it | Repair |
|---|---|---|---|
| `03_prompt_agent.py` | In `invoke`, change `"version": version` to `"version": "latest"` | `test_prompt_agent_recipe_creates_a_prompt_version_and_pins_it` | Restore the returned `version` |
| `05_maf_sequential.py` | Change `participants=[analyst, writer]` to `participants=[writer]` | `test_sequential_recipe_runs_both_agents_and_returns_outputs` | Restore both participants in order |

Use the same checker with a fresh report name for each broken/repaired state:

```bash
(
  set -C
  python scripts/check_recipes.py --directory outputs/code-along-en > outputs/code-along-en/check-extra-01.json
)
```

Change `check-extra-01.json` to `check-extra-02.json`, and so on, **before** another attempt.
Record which row and state each file represents. A changed recipe can trigger a test failure or an SDK error;
both must stay visible, and neither is an Azure service result.

## 6. Finish or recover

| Situation | Next action |
|---|---|
| `No module named ...` | Check Python 3.13 and the active `.venv`, then install the pinned optional SDK set from step 1 |
| `Missing or redirected recipe` | Check all six filenames in the copied directory; do not point at a ZIP or a symlink |
| Output file already exists | Read that result, or choose a new report name; keep the earlier file |
| `blocked a network connection` | Stop. The copy tried to leave the declared mock path; inspect your changes instead of signing in or disabling the guard |
| Repaired code still fails | Read the first actual failure, compare with the original recipe, and change only your copy |

**Done:** your baseline and repaired summaries pass, the intentional failed summary remains, and you can explain the API contract you broke.
This is **SDK practice completed**, not B's Azure completion, a model score, or deployment approval.
Keep the copied code and reports locally; no cloud cleanup is needed for this exercise.

Return to [B's implementation extensions](paths/b-practitioner.md) or [choose a C module](paths/c-advanced.md).
