# RangeWitness

A reusable GenLayer primitive for comparing **numeric claims in natural-language evidence**. Comparative consensus extracts closed integer intervals for a committed metric and unit. Deterministic code then computes an intersection, or supplies two source IDs witnessing a contradiction. It never averages incompatible statements into a misleading answer.

This is not a factual price feed, a reliability score, or a measurement of real delivery performance. The included parcel excerpts are deliberately constructed test inputs, not independent external observations. No production adoption or rewards are claimed.

## State machine and guarantees

`commit(metric, unit, excerpts_json)` freezes 2–12 unique excerpts, creator address and SHA-256 snapshot. `resolve(id)` is creator-only and final. `get_case(id)` and `list_cases(offset, limit)` expose reproducible evidence and results.

A custom `run_nondet_unsafe` validator independently runs the extraction function and compares the exact ID/status/lower/upper tuples in deterministic code. Validators compare the complete mapping of excerpt IDs, bounded/uncertain/irrelevant statuses and exact numeric bounds. All excerpts must occur exactly once. Reasons can differ in wording. Bounded quotations must be contiguous substrings of committed evidence. Approximate, decimal, missing-unit, open-ended, ambiguous and mismatched-scope statements are excluded rather than guessed. There is no unit conversion.

After consensus, ordinary deterministic Python computes `max(lower)` and `min(upper)` over all bounded readings. At least two are required. For a nonempty intersection the result is `overlap`. For an empty intersection it is `conflict`; the IDs attaining those two extremes are a minimal pairwise conflict witness for closed intervals on a line. Ties choose the lowest ID. With fewer than two readings the result is `insufficient`. The full set of excluded IDs is retained. Source excerpts and hashes remain available for inspection.

The model's semantic extraction can be wrong despite consensus. Structural validation proves coverage, integer bounds, quote membership and deterministic aggregation, **not** source authenticity, independence, completeness or semantic correctness. An attacker can commit misleading text. Results apply only to the committed material and exact metric/unit. `overlap` means numerical compatibility, not truth; `conflict` means incompatible extracted intervals, not dishonesty. Do not use this test primitive for financial, medical, legal or safety decisions.

## Reproduce

Python 3 runs the deterministic business-rule tests without installing a fake blockchain SDK:

```sh
python tests.py
npm ci --ignore-scripts
# Set GENLAYER_PRIVATE_KEY_FILE to your own ignored testnet key file.
# Fund only with Bradbury test GEN. Never commit that file.
npm run deploy
npm run demo
```

The Node scripts pin GenLayer SDK and viem versions, check the Bradbury chain ID/genesis/manager, whitelist only deploy/commit/resolve, track signed and pending transactions, reconcile rather than resend, cap each signed transaction at 0.3 test GEN, protocol prepayment at 0.2 and session balance loss at 1. Logs and keys are ignored. Demo refuses to run again after any initial commit. An interruption must be reconciled with `node scripts/run.mjs` before further action; do not blindly rerun demo.

22 tests cover intersection, disjoint conflict witnesses, touching endpoints, canonical ties, insufficient evidence, fabricated quotations, incomplete/duplicate/boolean IDs, invalid bounds, excluded readings, creator authorization, immutable finalization, snapshot preservation, duplicate inputs, atomic failure, prose-insensitive decision comparison and independent validator execution. The stub isolates deterministic business rules; it does not simulate validator consensus. The separate on-chain demo validates actual deployment and consensus execution.

## On-chain evidence

Deployment and finalized demo receipts are published in `deployment.json` and `demo-result.json` after successful testnet execution. The demo uses two explicitly disjoint hour ranges, an unrelated weight and an approximate time. Expected outcome: bounded IDs 1/2, irrelevant ID 3, uncertain ID 4, conflict witnesses 2/1 at lower=30 and upper=24 hours.

## Reuse

Adapt the metric/unit and excerpts for builders checking incompatible published integer estimates, documentation constraints or service specifications. Preserve original quotations and expose uncertainty to downstream users. The primitive deliberately separates probabilistic extraction from deterministic interval algebra; a different extraction backend can reuse the same validation and witness computation.

License: MIT; see LICENSE.

