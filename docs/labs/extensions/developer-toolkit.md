# Developer tools: one environment, optional editor integration

**English** | [한국어](../../ko/labs/extensions/developer-toolkit.md)

**Path B preparation.** The canonical route uses the repository's Python CLI.

**Evidence status:** the tooling checks date from September 16, 2026 (earlier `gpt-5.6-luna` preset); not re-run with `gpt-6-sol`.

Foundry Toolkit is an optional editor interface, not a second implementation or a reason to install every new SDK.

**First pass:** core B uses section 1 and returns to its route. Hosted SDKs, azd and the editor extension below are needed only by separately selected modules.

**Need:** Lab 00 B's source folder, `.venv`, `.env` and your own `az login`. `doctor --cloud` is a read-only preflight; it creates nothing.

## 1. Confirm the actual Python and project

Complete [Lab 00 B](../00-start.md#b-code-one-folder-one-environment).
In VS Code, open the repository folder and choose its `.venv` with **Python: Select Interpreter**.
Open a new terminal at the same root and activate that environment.

```bash
source .venv/bin/activate
python --version
python -m pip check
python scripts/workshop.py --language en doctor
python scripts/workshop.py --language en doctor --cloud
```

An offline PASS does not prove cloud authentication.
A successful cloud preflight does not prove model feature support; complete Lab 02's actual request.

**Core B done:** return to [B's next unfinished step](../../paths/b-practitioner.md).
Do not install Hosted packages or azd just to pass a check that the core route does not require.

<a id="hosted-sdk"></a>

### Selected modules only: Hosted and Toolbox SDKs

<details>
<summary>Prepare once before Toolbox, local Hosted serving, the matrix or local recovery; not for package-only B</summary>

From this repository root with `.venv` active, install the declared extra only if it is missing:

```bash
python -m pip install -e ".[hosted]"
python -m pip check &&
python scripts/check_sdk.py
```

`check_sdk.py` checks **cloud + agents + hosted**, including `ResponsesHostServer`.
It is not a core-B check. Require `passed: true` and `azure_requests_sent: false`.
Keep a working prepared environment instead of reinstalling it for each module.
The [local recovery module](approval-recovery.md) additionally checks its exact agentserver versions;
the owner uses the [locked rehearsal environment](../../instructor.md#4-the-day-before-rehearse-the-same-edition) if needed.
An SDK mismatch remains a preparation error, not a reason to upgrade arbitrary packages or call Azure.

</details>

<a id="azd-check"></a>

## 2. Inspect azd without modifying shared settings

Only modules that use azd need this check. Install/sign in through the
[official setup](https://learn.microsoft.com/azure/foundry/agents/how-to/install-cli-foundry-extensions)
if it is missing; installation and sign-in are not agent deployment.

```bash
azd version
azd ext list
azd auth login --check-status
azd ai agent init --help
```

The account, project and model values must match the setup card.
Do not change the default subscription or globally upgrade every extension during a class.
An incompatible CLI/extension combination is a preparation blocker, not a reason to skip error output.

## 3. Optional Foundry Toolkit

Use the [official installation and project setup guide](https://learn.microsoft.com/azure/foundry/how-to/develop/install-foundry-toolkit-visual-studio-code).
Install only after the owner approves the extension on that computer.

After installation:

1. Open **Foundry Toolkit** in VS Code's Activity Bar.
2. Sign in with the same intended Entra account; this is separate from assuming that a terminal login was inherited.
3. Under **My Resources**, select the exact training project.
4. Inspect its model and agent inventory; compare the IDs/endpoints with your setup card.
5. Open a source file and terminal in the same workspace; do not create a duplicate project from an unrelated template.

For Toolbox creation, use the [workshop's executable Toolbox path](toolbox.md) first.
Toolkit's tools view can then inspect that same resource rather than create another unnamed copy.

If Toolkit is not installed or cannot access the project, keep the CLI route and label editor integration **not run**.
Do not present a screenshot of the Marketplace as a successful Toolkit integration.

## 4. Record the compatibility snapshot

The committed dependency pins are the tested workshop combination, not a promise to use every package's newest release.
MAF Python 1.18 introduces vector-store abstractions, tool-loop bounds and breaking dependency/serialization changes.
Before adopting it, test the **whole** provider/Projects/OpenAI/hosting combination in a separate environment.
Do not upgrade only one library and infer compatibility from a successful import.

SDK help and generated `azure.yaml` are executable contracts.
If current help differs from a historical screenshot or source sample, keep the discrepancy and verify the intended operation before changing the guide.

## 5. Optional Foundry Dev Pack

Foundry Dev Pack bundles current Foundry developer tools such as `az`, `azd` with the Foundry extension,
the Foundry skill for coding agents, Foundry Toolkit for VS Code when applicable, and canvas integration when applicable
(checked 2026-09-24).

Choose the one installer for your operating system from the official announcement:

| Operating system | Installer command |
|---|---|
| Windows | `winget install Microsoft.FoundryDevPack` |
| macOS | `brew install --cask microsoft/foundry/devpack && foundry-devpack install` |
| Linux | `curl -fsSL https://aka.ms/foundry-devpack-install.sh \| bash` |

This installs current/latest tooling, not necessarily this workshop's pinned SDK combination.
Record the actual versions afterward and keep the workshop pins for exercises.
Do not install it on shared machines without owner approval.

## 6. Coding agents with the Microsoft Foundry skill

GitHub Copilot and Claude Code can use the Microsoft Foundry skill to help scaffold, evaluate and troubleshoot Foundry work
(checked 2026-09-24). Treat generated changes as code that must be reviewed.

Guardrails for this workshop:

- Coding agents must not provision, deploy, assign roles, publish or change the default Azure subscription without explicit approval.
- Keep all examples on bundled synthetic data.
- Review generated code, dependency changes and Azure commands before use.
- Preserve prompt, dataset, response, evaluator and trace lineage.

**Next:** return to the module that sent you here, or to [B's next unfinished step](../../paths/b-practitioner.md).
[MAF Python 1.18 release](https://github.com/microsoft/agent-framework/releases/tag/python-1.18.0) ·
[Workshop compatibility record](../../reference/versions.md).
