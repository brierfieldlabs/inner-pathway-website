# Inner Pathway isolated staging smoke test

11 October 2026

This staged-only commit tests the new deployment boundary.

Expected:
- CI validates the `staging` branch.
- The GitHub Pages **deploy job is skipped** on a staging push.
- The isolated Hamblett CT146 staging publisher automatically incorporates this commit.
- Neither the `main` commit nor the live website files are modified.
- This note is in `history/` and excluded from both public and staged static websites.

This document is a test record, not a production change.
