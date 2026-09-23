# Tool Search and Skills: discover a tool, load a reviewed procedure

**English** | [한국어](../../ko/labs/extensions/tool-search-skills.md)

**Path C, optional Preview — September 16, 2026.**

**Evidence status:** English discovery, pinning, Skill readback and load ran on September 16, 2026 with the earlier `gpt-5.6-luna` preset (no private catalog infrastructure); not re-run with `gpt-6-sol`.

Complete the ordinary [Toolbox lab](toolbox.md) first. Keep that Toolbox, its original version and ownership ledger.
This module still reads only the six bundled synthetic policies. It neither calls the public web nor executes skill scripts.

**Need:** the working synthetic Toolbox, the same `.env`, installed azd skill commands, and approval for new Toolbox/Skill versions and model calls.
**Stop when:** the actual tool list matches discovery/pinning configuration and a real MAF run loads the pinned skill before using policy evidence.
**If blocked:** do not change to the old `toolbox_search_preview` contract or load another skill after an error.

**First pass:** steps 1–5 verify a pinned Skill; step 6 records keep/cleanup ownership.
Changing the consumer default or creating a private catalog is not required.

## 1. Understand the three assets

| Asset | Purpose | Not equivalent to |
|---|---|---|
| Policy Search tool | Retrieves original policy evidence | A procedure or permission to approve |
| Tool Search | Finds relevant tool definitions through `tool_search` and invokes them through `call_tool` | Searching policy documents itself |
| Skill | A versioned Markdown procedure for reviewing evidence | A source of policy facts, a new model or automatic training |

One tool is deliberately enough to learn the protocol safely.
This tiny example does **not** demonstrate a measured token/cost saving at production scale.

## 2. Add discovery and pin the policy tool

Inspect the complete proposed definition first:

```bash
python scripts/workshop.py --language en toolbox plan --discovery --pin-policy
```

Inspect the plan's owned name and tool definition. Only after that check and write approval:

```bash
python scripts/workshop.py --language en toolbox add-version --discovery --pin-policy --confirm-create
```

Record the returned `selected_version` in the same terminal:

```bash
printf 'Discovery selected_version: '
read -r DISCOVERY_VERSION
python scripts/workshop.py --language en toolbox probe --version "$DISCOVERY_VERSION" --label discovery-list
```

The actual list must contain `tool_search`, `call_tool`, and the explicitly pinned `policy_search`.
Other unpinned tools are normally discovered on demand; do not mistake hidden tools for a broken connection.
No model or policy query has run in this probe.

## 3. Prepare the reviewed skill from canonical inputs

Run this **once**. If another C module already produced `outputs/extensions-en/`, inspect its manifest and reuse it rather than rerunning:

```bash
python scripts/workshop.py --language en prepare-extensions --label extensions-en
```

Open `outputs/extensions-en/policy-review/SKILL.md` and `manifest.json`.
The skill has the name `<your-prefix>-policy-review-en` and contains the existing v2 procedure plus an explicit no-script boundary.
It contains no holdout, answer fixture or approval credential. The manifest preserves the source prompt/corpus/dev hashes.

This preparation command also creates inputs for other extension modules.
`optimizer-dev.jsonl` contains evaluator reference fields: never paste those fields into an agent conversation.

## 4. Create the Skill asset, then verify its bytes

Check the commands before a write:

```bash
azd ai skill create --help
azd ai skill download --help
```

Enter the **actual project endpoint** from your setup card and the **skill_name** printed in the generated manifest:

```bash
printf 'Full project endpoint: '
read -r PROJECT_ENDPOINT
printf 'skill_name from outputs/extensions-en/manifest.json: '
read -r SKILL_NAME
azd ai skill create "${SKILL_NAME:?Use the generated skill name}" --file ./outputs/extensions-en/policy-review \
  --project-endpoint "${PROJECT_ENDPOINT:?Enter the full project endpoint}" &&
azd ai skill show "${SKILL_NAME:?Use the generated skill name}" \
  --project-endpoint "${PROJECT_ENDPOINT:?Enter the full project endpoint}" --output json
```

Directory upload preserves the supplied `SKILL.md` bytes as a package.
Do not use `--force`; creating over an existing skill can delete prior versions.
Read the actual `default_version`, then download that exact version:

```bash
printf 'Skill default_version returned by show: '
read -r SKILL_VERSION
mkdir outputs/skill-readback-en &&
azd ai skill download "${SKILL_NAME:?Use the generated skill name}" --version "${SKILL_VERSION:?Use the returned skill version}" \
  --output-dir ./outputs/skill-readback-en --project-endpoint "${PROJECT_ENDPOINT:?Enter the full project endpoint}" &&
cmp ./outputs/extensions-en/policy-review/SKILL.md ./outputs/skill-readback-en/SKILL.md
```

`cmp` prints nothing and exits 0 when the bytes match.
If they differ, stop and review the package/CLI behavior; do not edit the downloaded file to manufacture a match.
If the readback directory already exists, inspect that attempt first. For a new download, use a new directory in
`mkdir`, `--output-dir` and the second `cmp` path; never overwrite the earlier version's evidence.
The `${NAME:?...}` guards stop before azd if a required name, version or endpoint is empty.

## 5. Attach the exact skill version to a new owned Toolbox version

```bash
python scripts/workshop.py --language en toolbox plan --discovery --pin-policy --skill-version "$SKILL_VERSION"
```

Verify the exact Skill name/version in the plan before approving the new Toolbox version:

```bash
python scripts/workshop.py --language en toolbox add-version --discovery --pin-policy --skill-version "$SKILL_VERSION" --confirm-create
```

The helper references only `<your-prefix>-policy-review-en`, with the explicit version above.
Omitting a skill version would follow a mutable default and is not this lab's contract.
The default Toolbox version remains a separate pointer; inspect the returned values rather than assuming promotion.

```bash
printf 'Skill-bearing Toolbox selected_version: '
read -r SKILLED_VERSION
python scripts/workshop.py --language en toolbox probe --version "$SKILLED_VERSION" --label skilled-tool-list
```

After the probe succeeds, make the separately approved model request:

```bash
python scripts/workshop.py --language en toolbox ask --version "$SKILLED_VERSION" --label skilled-policy-answer --with-skill --confirm-cost
```

Check `skill_ref`, `skill_load_verified`, `function_calls`, `model_calls`, and original `tool-results.json`.
The reused v2 procedure requires a caller-supplied JSON schema. This helper supplies it and
validates `structured_answer`; it does not silently alter the stored Skill package.
An attached skill alone is not proof that the agent loaded it.
The MAF provider must actually call `load_skill`, then the policy tool, and preserve the resulting answer.
The code rejects skill-script execution and rejects a fluent final answer if a tool failed.

## 6. Keep publication and cleanup explicit

Keep the verified version/Skill IDs and `outputs/toolbox-runs/skilled-policy-answer/`.
If continuing to [Hosted Toolbox](toolbox-hosted.md), retain the assets and ledger.

<details>
<summary>Optional: promote the consumer default after review and approval</summary>

Only after reviewing that version should you change the consumer default:

```bash
python scripts/workshop.py --language en toolbox select --version "$SKILLED_VERSION" --confirm-update
```

Use the original saved version to roll back through the same explicit command.
The Toolbox endpoint can stay constant while its default changes, but pinned runs keep their recorded version.
Keep the skill version fixed too; Toolbox versioning does not freeze an unpinned skill reference.

</details>

When finishing, remove the owned Toolbox before deleting the skill it references.
Use the Toolbox lab's ownership-aware cleanup, then have the owner remove only this newly created Skill asset.
Never delete a shared skill or use force recreation as a version-update shortcut.

## Optional: private catalog is a separate infrastructure exercise

The [private skill catalog](https://learn.microsoft.com/azure/foundry/agents/how-to/private-skill-catalog)
uses Azure API Center and separate catalog permissions/allowed-tool governance.
It is not created by the commands above. Without that prepared infrastructure, record **catalog design only / not run**.

**Next:** [C module selection](../../paths/c-advanced.md) or [Lab 11 handoff](../11-capstone.md).
Conversation evaluation is an independent module, not the next required command.

[Tool Search contract](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/tool-search) ·
[Versioned Skills](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/skills).
