# Research tools

These scripts preserve the archive-discovery and recovery work. They are not imported by Eleventy and are not executed during build or deployment.

Run them explicitly from the repository root, for example `python tools/research/wayback_probe.py`. Most require network access. Read each script's arguments and output defaults before running it; several write research results under the sibling `private-research/` directory. `archive_originals.py` requires the separately retained recovery ZIP and can regenerate archive metadata and copies. Do not run it as an ordinary build step.

Published research notes live in `docs/research/`. The synced ChatGPT `sources/` directory outside this repository remains read-only.
