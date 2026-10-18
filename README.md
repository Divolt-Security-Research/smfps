# SMFPS — Silent-Mail-Forwarding Prevention Standard

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![IETF Draft](https://img.shields.io/badge/IETF-draft--divolt--smfps--00-blue.svg)](https://datatracker.ietf.org/doc/draft-divolt-smfps/)
[![Paper: arXiv](https://img.shields.io/badge/paper-arXiv-b31b1b.svg)](https://arxiv.org/)
[![Companion: ForwardGuard](https://img.shields.io/badge/companion-ForwardGuard-green.svg)](https://github.com/divolt-security-research/forwardguard)

**SMFPS** is a provider-side control baseline for the mail-forwarder configuration
surface exposed by domain registrars, shared-hosting control panels (cPanel/WHM,
Plesk, DirectAdmin), and other operators of RFC 5321 mail-forwarding features.
It specifies eight normative requirements, each with a conformance test, whose
adoption eliminates the **silent-forwarder primitive** — the capacity to redirect
a mailbox's traffic to an arbitrary external destination without notifying the
mailbox owner.

This repository holds:

- The IETF Internet-Draft source (`draft-divolt-smfps.xml`, XML2RFC v3 format).
- A frozen copy of each submitted revision under `drafts/`.
- A conformance test suite that providers can run against a staging environment
  to self-assess SMFPS compliance.
- The reference audit-event JSON Schema (`conformance/smfps-audit-event.schema.json`).

The companion research paper is at [arXiv](https://arxiv.org/), the open-source
defender-side detection tooling at [divolt-security-research/forwardguard](https://github.com/divolt-security-research/forwardguard).

## Who this is for

If you operate any of the following, SMFPS is a specification you can implement
to eliminate silent-forwarder findings against your service:

- A domain registrar that bundles email forwarding (Porkbun, Namecheap, Hover,
  GoDaddy, Dynadot, Gandi, Cloudflare Registrar, and their peers).
- A shared-hosting provider whose control panel includes forwarders
  (cPanel/WHM, Plesk, DirectAdmin, ISPConfig).
- A gateway appliance vendor whose product exposes a mail-forwarder
  configuration surface.

If you don't operate such a service but you want to detect silent forwarders
in your own domains, see
[`divolt-security-research/forwardguard`](https://github.com/divolt-security-research/forwardguard).

## Two conformance profiles

- **SMFPS Minimum Compliance** — requirements R1 + R2 + R3 + R4. Eliminates
  the silent-forwarder primitive. Appropriate for small operators.
- **SMFPS Full Compliance** — R1 through R8. Appropriate for top-ten
  registrars, multi-tenant hosting providers at scale, and any provider
  offering a reseller programme.

## Eight requirements at a glance

| ID | Requirement | What it defeats |
|---|---|---|
| R1 | Out-of-band notification on any forwarder lifecycle event | silent-forwarder primitive |
| R2 | Destination-ownership proof via time-limited URL | accidental and malicious exfiltration |
| R3 | Confirmation to the primary mailbox | victim awareness |
| R4 | Immutable, principal-attributed audit log | STRIDE Repudiation |
| R5 | Audit log exposed via standard HTTPS API (JSON Schema) | defender-side continuous audit |
| R6 | Per-domain forwarder count ceiling | bulk-add exfiltration mesh |
| R7 | Loop and chain-depth detection at apply time | STRIDE DoS |
| R8 | Reseller / sub-account attribution in audit chain | adversary class A3 |

See [`draft-divolt-smfps.xml`](./draft-divolt-smfps.xml) for the full
specification with rationale, conformance tests, and backwards-compatibility
notes for each requirement.

## Rendering the draft

The draft source is XML2RFC v3. To render:

```bash
pip install xml2rfc
# Text output:
xml2rfc --text draft-divolt-smfps.xml
# PDF output:
xml2rfc --pdf  draft-divolt-smfps.xml
# HTML output:
xml2rfc --html draft-divolt-smfps.xml
```

The IETF datatracker also renders submitted drafts automatically.

## Running the conformance test suite

The suite is a set of HTTP interactions a provider-side staging implementation
responds to. Each test corresponds to one SMFPS requirement.

```bash
pip install -r conformance/requirements.txt
python -m conformance.runner --target https://staging.your-provider.example \
    --credentials conformance/example-creds.yaml \
    --profile full       # or 'minimum'
```

Output is a per-requirement pass/fail summary. A passing run under `--profile
full` means the provider conforms to SMFPS Full.

The runner is intentionally minimal (<500 LOC); it reads one test per
requirement from `conformance/tests/`.

## Submitting feedback on the draft

- IETF: open a GitHub issue here and tag it `draft-feedback`, or reply on the
  mailmaint mailing list once the draft is announced.
- Editorial: PRs against `draft-divolt-smfps.xml` welcome.
- Specification: substantive changes go through issue discussion first.

## Divolt Security Research

SMFPS is maintained by Divolt Security Research. Reach the editors at
<research@divoltbtc.com>.

## Licence

Document and specification: CC BY 4.0 (see `LICENSE`).
Code in `conformance/`: Apache License 2.0 (see `conformance/LICENSE`).
