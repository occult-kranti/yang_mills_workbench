# Exact-tree release procedure

1. Admit all ten source-bound loop gates after separate producer and skeptical review. Keep limited outcomes and inventory repairs visible.
2. Build Round26 network/data and Pages. Check the current graph, summaries, roadmap and method updates against the admitted claims.
3. Commit the complete candidate. Create a clean detached worktree at that commit. Run `verify.py` there with its exact commit, tree and a fresh external output directory:

```bash
python3 -B research/round26/release/verify.py \
  --expected-commit FULL_COMMIT \
  --expected-tree FULL_TREE \
  --output /absolute/new/release-verification
```

4. The verifier preserves historical research, checks Round24 gates, replays all twenty current producers in normal and optimized Python, replays both inherited AA producers in both modes, exercises admission mutations, removes and rebuilds current generated assets byte-for-byte, and runs seven interface suites. The final worktree must remain clean.
5. Push the tested candidate, open a pull request and record the external receipt hash and exact tested commit/tree in its body. Fetch the actual remote head. Merge only when its resulting tree is the tested tree; otherwise review and verify the changed candidate. Never force-push over unrelated work.
6. Verify GitHub main and Pages independently. Record the merged commit, matching tree, deployment status and live asset bytes. A successful source push is not a successful website deployment.

The supported cloud browser could not access the local loopback preview (`ERR_BLOCKED_BY_CLIENT`). This is not a successful visual audit. Test the public deployment after publication and record the observed interactions and limitations separately from the exact-tree receipt. Do not claim responsive-device testing from a DOM stand-in.

The PR is the publication receipt location because adding its own commit/tree receipt to the candidate would change that tree. Scientific gates and written proofs are durable within the candidate; the execution receipt is attached as exact text/hash to the PR.
