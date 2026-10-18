# Contributing to SMFPS

Three kinds of contribution are welcome:

1. **Specification feedback** on `draft-divolt-smfps.xml`. Open a GitHub issue
   first for substantive changes; small editorial fixes can go straight to PR.
   Each change should name the SMFPS requirement (R1..R8) it affects.
2. **Conformance test implementations** for additional providers. Fork
   `conformance/tests/adapters.py.template`, fill in the hooks for the
   provider you're testing against, and submit as a new adapter module.
3. **Interoperability reports.** If you've exercised the conformance suite
   against a provider staging environment and received PASS or FAIL, open an
   issue tagged `interop-report` with the output.

## Workflow

- Branch from `main`.
- CI must stay green (the IETF-draft render workflow lints the XML).
- Keep PRs focused on one requirement or one adapter.

## Discussion

Substantive IETF-process discussion happens on the IETF `mailmaint` mailing
list once the draft is announced. GitHub issues are for repository-local
questions.

## Divolt Security Research

SMFPS is maintained by Divolt Security Research. Reach the editors at
research@divoltbtc.com.
