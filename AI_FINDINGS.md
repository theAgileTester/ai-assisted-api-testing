# AI Findings Log — AI-Assisted API Testing (Fintech)

| Date | AI output | Verdict | What was wrong / what I changed | Type |
|------|-----------|---------|----------------------------------|------|
| 2026-11-09 | TC_1 status-only test | ✏️ | Test passed against wrong URL (missing /latest). Status-only check can't catch wrong endpoint. | weak assertion |
| 2026-11-09 | Postman baseUrl setup | ✏️ | ENOTFOUND: variable not defined in active environment. Added baseUrl to Frankfurter Environment. | setup / config |
| 2026-11-09 | 8 test ideas for GET /latest | ⏳ | Not run yet. | — |
| 2026-11-10 | Repo scaffold: .gitignore | ✅ | `.env` is ignored — verified with `git check-ignore -v .env` (.gitignore line 2). | — |
| 2026-11-10 | Repo scaffold: secret scan | ✅ | No hard-coded keys. grep returned 9 hits, all false positives (`.keys()`, Postman `key` field, comments, empty `# API_KEY=`). | false positive (tool) |
| 2026-11-10 | Repo scaffold: requirements.txt | ⏳ | Pinned pytest==8.3.4 — newer 9.x likely exists. To verify on PyPI and check all 3 packages are imported. | outdated dependency? |

Verdict: ✅ accepted · ✏️ fixed · ❌ rejected · ⏳ open
Type: wrong fact · wrong assumption · missing case · missing context · weak assertion · hallucinated API · outdated dependency · setup / config

## 📊 Weekly AI metrics (Fridays)

| Week | Outputs reviewed | ✅ | ✏️ | ❌ | Acceptance rate |
|------|------------------|----|----|----|-----------------|
| 1    |                  |    |    |    |                 |
| 2026-11-11 | Create customer test assertions | ✏️ | AI test only checked status 
| 2026-11-11 | Create customer test assertions | ✏️ | AI test only checked status 201 — would pass even if name/email/id were wrong. Added echo checks for first_name, last_name, email + id and createdAt presence. | weak assertion |
| 2026-11-11 | Test environment | ⏳ | Tests ran with conda base pytest 8.4.2 (+ unrelated plugins), not the project .venv (8.3.4). Risk: "works on my machine". Fix: run with `python -m pytest`. | setup / config |
| 2026-11-12 | Stripe test ideas: "create returns 200" | ✏️ | Labelled as "docs" but came from a 3rd-party site. Verified later on Stripe's official errors page. | wrong source |
| 2026-11-12 | Stripe test ideas: C4 duplicate email | ✏️ | Expected result based on a 3rd-party blog, not Stripe docs. Must be verified by running. | wrong source |
| 2026-11-12 | Stripe test ideas: C5, P5, P7 | ⏳ | AI marked them [ASSUMPTION] — expected results not in docs. P7 now confirmed as 401 from official docs. | assumption |
| 2026-11-12 | Stripe test ideas: C2 empty customer | ✅ | Correct per docs, but raised a requirement question: should our app allow empty customers? | requirement question |
| 2026-11-12 | Stripe test ideas: missing cases | ✏️ | AI missed: insufficient funds decline (P8), customer with tax/address (C6). Added by me. | missing case |