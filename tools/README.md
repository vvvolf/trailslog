# Tools

Small, self-contained tools that are part of the methodology's onboarding.

## Why tools may live here

The default rule is that executable tools live outside a knowledge repository.
This directory is a deliberate exception for a narrow class of helpers:

- one file or a tiny folder;
- no dependencies beyond shell and optional `git`;
- part of the methodology's own setup or onboarding;
- no independent release cycle, CI or product support;
- has a README contract and clear safety boundaries.

When a tool grows tests, dependencies, multiple consumers or its own release
rhythm, extract it into a separate repository and leave a link here.

## Tools

- [`new-project/`](new-project/README.md) — create a project from the
  canonical TrailsLog template.
