# Host the same version-pinned Toolbox agent

**English** | [한국어](../../ko/labs/extensions/toolbox-hosted.md)

**B/C extension.** Complete the local [Toolbox](toolbox.md) request first.

**Evidence status:** the English local and remote Hosted Toolbox runs date from September 16, 2026 (earlier `gpt-5.6-luna` preset); not re-run with `gpt-6-sol`.

This module reuses the same MAF wrapper, tool/version validation and failure-preserving execution;
it does not copy an earlier workflow's quality score onto a new target.

**Need:** a working owned Toolbox version, the synthetic seed ledger, hosted SDKs, [prepared azd access](developer-toolkit.md#azd-check),
the actual existing project ARM ID, a new agent name and explicit deployment/model/tool permission.
**Stop when:** the exact new remote version returns real tool/model/evidence metadata.
**If blocked:** retain the stage, error and any created IDs as **failed/blocked**; unattempted stages are **not run**.
For package-only scope, stop after step 1 and return to [Lab 11](../11-capstone.md). Packaging is not a local or remote service test.

**First pass:** step 1 packages locally. Steps 2–3 prepare isolated azd state; step 2 also runs `azd ai project show`.
Treat that azd/project check separately from package-only preparation. Step 4 hosts locally but calls the real
Foundry model and Toolbox/Search: it is **live Azure, not an offline fixture**.
Obtain model/tool cost approval before step 4's request. Step 5's Hosted deployment and remote request need separate approval.
Always finish step 6 for assets you used. Keep both terminals at the **source repository root**
with the [Hosted SDK environment](developer-toolkit.md#hosted-sdk); `--cwd` selects the standalone azd project.

## 1. Package only the runtime and questions

Choose the branch **before packaging**:

- **Ordinary Toolbox:** enter the version verified in [Toolbox](toolbox.md); use the commands as shown.
- **Skill-bearing Toolbox:** enter the verified `SKILLED_VERSION` from [Tool Search/Skills](tool-search-skills.md).
  Add `--with-skill` to the package command below and step 4's server command **before running either**.

This choice is frozen in the package; do not package without the flag first and then try to overwrite it.
In the repository terminal, enter the verified version for your chosen branch:

```bash
printf 'Verified Toolbox version: '
read -r TOOLBOX_VERSION
python scripts/package_toolbox.py --language en --version "$TOOLBOX_VERSION"
```

The package is `.build/toolbox-en-<version>/`. It contains source, synthetic policies,
questions only, and a pinned `toolbox-profile.json`; no evaluator answer keys, holdout, `.env` or prior outputs.
Keep `package-manifest.json` and its file hashes; `cloud_deployed: false` records packaging only, not Hosted readiness.
Its profile freezes project, model, Toolbox name/version, Search connection and source configuration.
The application directory is read-only in Hosted execution. Request evidence is written under
the session's `$HOME/workshop-evidence/toolbox-runs`, not `/app/outputs`.
Use the recorded session's file commands to retrieve evidence before deleting that session.

Keep the printed **absolute package path** as `HOSTED_PACKAGE` for the preparation below.
Do not rebuild over an existing package or silently change runtime values after packaging.

## 2. Prepare an independent azd project

Use an empty standalone directory outside any existing azd project's parent tree.
This is execution-state isolation, not a separate curriculum repository.
The package can remain in the original repository folder.

In repository terminal A, enter the actual values. Use absolute paths without `~` shorthand.
Record the directory/name in `session-notes.txt` for a new terminal.
Continue only with prepared azd access: after the helper succeeds, the chained `azd ai project show` queries the existing project.
It is not model inference, but a successful package alone does not establish that access.

```bash
printf 'Absolute Toolbox package directory: '
read -r HOSTED_PACKAGE
printf 'Actual existing project ARM ID: '
read -r PROJECT_ARM_ID
printf 'New agent name (<your prefix>-toolbox-hosted-en): '
read -r HOSTED_AGENT_NAME
printf 'Absolute empty azd directory: '
read -r HOSTED_DIRECTORY
printf 'Actual existing project location (for example swedencentral): '
read -r PROJECT_LOCATION
python scripts/prepare_hosted_azd.py --language en --kind toolbox \
  --package "$HOSTED_PACKAGE" --directory "$HOSTED_DIRECTORY" \
  --agent-name "$HOSTED_AGENT_NAME" --initialize-env \
  --project-id "$PROJECT_ARM_ID" --location "$PROJECT_LOCATION" &&
azd ai project show --cwd "${HOSTED_DIRECTORY:?Use the prepared standalone directory}" --output json
```

The helper verifies every package file, copies that exact package, and writes a JSON-formatted
YAML manifest with one agent and the existing project endpoint. It initializes only this folder's
local azd environment using `azd env new/set/get-value`; it never provisions or deploys.
It verifies the ARM ID against the configured subscription/account/project and refuses
nonempty destinations, nested azd projects, changed packages or configuration drift.
An empty standalone directory can cause `init --src ... --no-prompt` to ask for a template
in the September 16 CLI. Adopting a template from inside itself can also fail with a source/destination overlap.
This route already provides the complete manifest, so it does not run either initialization path.
Do not select a sample that creates a new model or run `azd provision` for an unrelated project.
If preparation fails, stop and preserve the error/directory. Do not run the next azd command in the source project's context.

## 3. Match the remote environment to the package

The helper reads the workshop `.env` as data, checks it against the package profile, and writes
only the explicit project/model/Toolbox/Search settings into the agent service's `env`.
It sets `WORKSHOP_AUTH_MODE: managed-identity`, an output-token limit of 2048, and 1 CPU / 2 GiB.
No credential, answer key, alternate model or new model deployment is included.
The environment includes both `AZURE_AI_PROJECT_ENDPOINT` and the project extension's
`FOUNDRY_PROJECT_ENDPOINT`, read back against the same original endpoint.
Inspect these values before deployment; do not shell-`source` `.env`, overwrite the manifest, or copy IDs from a recording.
If the runtime bindings or environment schema change, stop before deployment.

The remote identity needs Foundry project access in addition to the upstream Search identity's permissions.
After deployment, the owner reads the **actual runtime principal ID** from the new agent version
and grants project-scoped Foundry User if required. Do not grant access to an assumed principal.
Local user permission does not transfer to the Hosted identity.

## 4. Verify local behavior with two terminals

In repository terminal A, use the same branch as step 1.
For a skill-bearing version, add `--with-skill` to the following command before running it:

```bash
OTEL_SDK_DISABLED=true python scripts/workshop.py --language en toolbox serve --version "$TOOLBOX_VERSION"
```

In terminal B, also at the source repository root, restore the directory from step 2.
Terminal A's shell variables are not inherited automatically:

```bash
printf 'Standalone Hosted directory from step 2: '
read -r HOSTED_DIRECTORY
curl --fail http://127.0.0.1:8088/readiness &&
azd ai agent invoke --cwd "${HOSTED_DIRECTORY:?Use the prepared standalone directory}" --local --new-session --new-conversation --timeout 210 "What are the advance-approval requirements for a KRW 170000 hotel on a domestic business trip in September 2026?"
```

Readiness alone is not completion. The JSON answer must include the selected Toolbox version/hash,
actual model calls, successful function/tool work and original policy evidence.
The local smoke command explicitly disables telemetry SDK export to avoid a large console-metric stream;
it does not verify App Insights export. Do not carry that local setting into the Hosted environment.
This training host accepts the bundled dev questions and the documented Toolbox question, not arbitrary company input.
Stop only terminal A's local server with Ctrl+C when finished.

## 5. Deploy and invoke the actual version

After deployment approval, return to terminal A after stopping its server.
It retains the exact package/directory/agent values from steps 1–2:

```bash
azd deploy "${HOSTED_AGENT_NAME:?Use the prepared agent service name}" --cwd "${HOSTED_DIRECTORY:?Use the prepared standalone directory}" &&
azd ai agent show --cwd "${HOSTED_DIRECTORY:?Use the prepared standalone directory}" --output json
```

Stop on a deployment error; an earlier active version is not the new deployment.
After `show` confirms the intended active agent, enter its actual new version:

```bash
printf 'Actual newly deployed agent version: '
read -r HOSTED_AGENT_VERSION
```

Make one request and verify the saved stream. The new evidence directory prevents overwriting an earlier attempt;
`pipefail` prevents a failed invocation from being hidden by `tee`.

```bash
(
  set -o pipefail
  : "${HOSTED_PACKAGE:?Use the verified package directory}" &&
  mkdir -p outputs &&
  mkdir outputs/toolbox-remote-en &&
  azd ai agent invoke "${HOSTED_AGENT_NAME:?Use the prepared agent service name}" \
    --cwd "${HOSTED_DIRECTORY:?Use the prepared standalone directory}" \
    --version "${HOSTED_AGENT_VERSION:?Use the version returned by show}" \
    --new-session --new-conversation --output raw --timeout 240 \
    "What are the advance-approval requirements for a KRW 170000 hotel on a domestic business trip in September 2026?" \
    | tee outputs/toolbox-remote-en/response.raw &&
  python scripts/verify_toolbox_response.py --file outputs/toolbox-remote-en/response.raw \
    --package "$HOSTED_PACKAGE" --agent-name "$HOSTED_AGENT_NAME" \
    --agent-version "$HOSTED_AGENT_VERSION" --output outputs/toolbox-remote-en/verified.json
)
```

If `outputs/toolbox-remote-en/` exists, read it first. A genuinely new request needs a new directory name
in **all three file paths and the `mkdir`**, not deletion of the earlier result.
Keep agent version, Session/Conversation/Trace IDs, actual returned Toolbox binding and tool/model results.
If the CLI exits 0 but displays no answer, that is **not** a passed smoke test.
Inspect the exact session logs/trace and response state before retrying or claiming completion.
The verifier above requires a completed service event, matching package hashes and successful model/tool/Skill evidence;
it does not repeat inference.
The package rejects different project/model/Toolbox/connection values instead of selecting an alternative at runtime.
A Toolbox upstream connection/index can still change; freeze those assets and inspect returned evidence separately.

## 6. Finish without breaking shared tools

Use [owned-session cleanup](../../reference/cleanup.md) for this new Hosted agent.
Using the recorded azd directory, agent and session, retrieve available evidence with `azd ai agent files list` and
`files download`. Paths are relative to the session's home: use the verifier's `remote_evidence_directory` on success,
or inspect that same session's `workshop-evidence/toolbox-runs/` if verification failed.
Keep the binding, request, model/function/tool results, summary or `failure.json`, package and response evidence.
If retrieval is blocked, record the reason and responsible owner. Stopping owned compute need not wait for retrieval;
verify its stopped/idle state, but preserve evidence before deleting the session or agent.
If deleting the new Hosted agent, check dependencies before removing its Toolbox, skill or Search source.
Do not delete shared project/model/Search resources or reuse old endpoint/version IDs.

**Next:** [C module selection](../../paths/c-advanced.md) or [Lab 11](../11-capstone.md).
