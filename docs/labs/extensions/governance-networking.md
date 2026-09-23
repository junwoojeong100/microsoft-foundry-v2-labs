# Governance and networking: identify the actor before changing access

**English** | [한국어](../../ko/labs/extensions/governance-networking.md)

**Path C, owner-assisted.** This first pass inspects the existing training environment.

**Evidence status:** the scoped role checks date from September 16, 2026 (earlier `gpt-5.6-luna` preset); a private network was not tested, and nothing was re-run with `gpt-6-sol`.

It does not create API Management, a virtual network or a new Foundry project,
and it never disables a shared firewall to make a demonstration work.

**Need:** your setup card, an actual model/tool result or error, and read access to the relevant resource settings.
**Stop when:** every connection has an identified caller, target, permission scope and evidence.
**If blocked:** record the missing access and ask the owner; no blanket Owner role or alternate account.

**First pass:** steps 1–5 inspect only resources used in your selected modules.
Save `identity-review.txt` in your notes directory. Mark unused connections **not run** rather than creating them to complete the table.

## 1. Draw the actual identity chain

Use your own names and IDs, not those in historical recordings:

| Connection | Actor to identify | Evidence |
|---|---|---|
| Local code → Foundry | Configured CLI account/subscription/tenant | Read-only doctor and actual model response |
| Hosted agent → model | Actual runtime/agent identity | Deployed version, identity object ID and scoped model permission |
| Client → Toolbox | User or runtime identity calling the MCP endpoint | Version binding, authenticated tool list and actual tool result |
| Toolbox → Search | Identity used by the approved project connection | Keyless connection metadata and actual Search access |
| Search → IQ chat model | Search service's system-assigned identity | Model-account role and real planning/synthesis activity |
| Operator → App Insights | The log reader's own identity | Scoped query and exact trace IDs |

These identities are not interchangeable. A user's successful portal request does not establish a Hosted agent's access.

## 2. Inspect before changing anything

```bash
python scripts/workshop.py --language en doctor --cloud
python scripts/workshop.py --language en cleanup-plan
```

In the Azure portal, open only the resources on your setup card:

1. **Foundry account/project → Access control (IAM)**: distinguish project roles from account-level model access.
2. **Search → Identity and Access control (IAM)**: distinguish the Search identity from the caller that queries the index.
3. **Project connections**: confirm the actual Search endpoint and Entra authentication.
4. **Networking**: record public/private access and the approved client path without changing it.
5. **App Insights / Log Analytics**: record query permissions, retention and any protected-table restrictions.

Do not post complete IAM exports, tokens or private trace content publicly.

## 3. Explain one real permission result

Choose an actual earlier success or failure. Record:

```text
Operation:
Calling identity:
Target resource:
Required scoped permission:
Observed HTTP/result:
Evidence/run/trace ID:
Owner and proposed correction:
```

A deliberate denial test is optional and must use a new lab-owned identity and an approved synthetic target.
Never remove another user's working role to manufacture a 403.
If a role is added, record the exact assignment ID and resource scope so only that new assignment can be removed later.

Role propagation can take time. A missing role and a stale token are different causes;
repeated sign-in is not the default response to every 403.

## 4. Keep network isolation separate

For `PublicNetworkAccessDisabled`, private-endpoint 403 or a timeout, inspect the account's network settings.
A public-access-disabled resource requires the owner-approved private-network path.
Changing clients, disabling certificate checks or trying another MCP server does not grant network access.

If no private environment is prepared, complete a **network design worksheet** rather than claiming a live VNet test:
client location, DNS resolution, endpoint, outbound destination, firewall/private-link controls and recovery owner.

## 5. Control Plane and AI Gateway

Use the available Control Plane/fleet views to identify registered agents and their monitoring scope.
If the environment has no configured AI Gateway, record **AI Gateway not configured / design only**.
Explain where per-agent/team token limits, routing policies, access enforcement and monitoring would apply.
Do not create a gateway or register unrelated agents simply to populate a screenshot.

Model/content guardrails, network egress rules, Azure RBAC and business approval solve different problems.
A content filter does not grant access; a role does not make a model answer correct.

**Next:** [Agent safety](agent-safety.md) or [Lab 11](../11-capstone.md).
[Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) ·
[Network options](https://learn.microsoft.com/azure/foundry/agents/concepts/networking-options) ·
[Control Plane](https://learn.microsoft.com/azure/foundry/control-plane/overview).
