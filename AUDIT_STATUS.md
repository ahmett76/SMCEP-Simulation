# SMCEP simulation audit (2026-11-08)

- v0.5: Original Turkish code restored from supplied Word document; wrapped title repaired; syntax and execution passed; all numerical CSV columns match the archived historical results.
- v0.6: Full default rerun did not complete within the audit time budget; not verified.
- v0.7: See verification table below; default output paths were overridden with `--out`.
- v0.8: See verification table below; default output paths were overridden with `--out`.
- v0.9: See verification table below; default output paths were overridden with `--out`.
- v1.0: See verification table below; default output paths were overridden with `--out`.

| Version | CSV byte-identical | JSON semantic equality |
|---|---|---|
| v0.7 | Yes | No (requires investigation) |
| v0.8 | Yes | No (requires investigation) |
| v0.9 | Not completed | Not completed |
| v1.0 | Yes | No (requires investigation) |

Note: Different JSON output paths may cause a mismatch even if experimental statistics are identical. This report does not claim full reproducibility of all five pilots.
