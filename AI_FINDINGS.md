# AI Findings Log — AI-Assisted API Testing (Fintech)

| Date | AI output | Verdict | What was wrong / what I changed | Type |
|------|-----------|---------|----------------------------------|------|
| 2026-11-09 | TC_1 status-only test | ✏️ | Test passed against wrong URL (missing /latest). Status-only check can't catch wrong endpoint. | weak assertion |
| 2026-11-09 | Postman baseUrl setup | ✏️ | ENOTFOUND: variable not defined in active environment. Added baseUrl to Frankfurter Environment. | setup / config |
| 2026-11-09 | F1–F8 Frankfurter test ideas (Postman) | ✅ | Run 2026-11-13: 6 of 8 ideas passed as written (01, 02, 03, 05, 07, 08). | — |
| 2026-11-09 | F4 Invalid base currency | ✏️ | Passed, but accepts any 4xx — not one specific expected result. | weak assertion |
| 2026-11-09 | F6 Date equals today | ✏️ | Failed at 13:38: API returned the last published date, not today. ECB rates publish in the afternoon and not at weekends — AI assumed "always today". | wrong assumption |
| 2026-11-10 | Repo scaffold: .gitignore | ✅ | `.env` is ignored — verified with `git check-ignore -v .env` (.gitignore line 2). | — |
| 2026-11-10 | Repo scaffold: secret scan | ✅ | No hard-coded keys. grep returned 9 hits, all false positives (`.keys()`, Postman `key` field, comments, empty `# API_KEY=`). | false positive (tool) |
| 2026-11-10 | Repo scaffold: requirements.txt | ⏳ | Pinned pytest==8.3.4 — a newer version (8.4.2) exists on this machine. To decide whether to update. | outdated dependency? |
| 2026-11-11 | Create customer test (ReqRes POST /users) | ✏️ | Payload didn't match ReqRes user model; "customer" doesn't exist in ReqRes. Changed to first_name/last_name/email. | wrong assumption |
| 2026-11-11 | Create customer test: x-api-key header | ✏️ | Header not needed — classic ReqRes endpoints don't require a key (per current docs). Removed. | outdated info |
| 2026-11-11 | Create customer test assertions | ✏️ | AI test only checked status 201 — would pass even if name/email/id were wrong. Added echo checks + id and createdAt presence. | weak assertion |
| 2026-11-11 | Test environment | ✏️ | Tests ran with conda base pytest 8.4.2 (+ unrelated plugins), not .venv. Fixed with `python -m pytest` — confirmed 2026-11-13. | setup / config |
| 2026-11-12 | Stripe test ideas: "create returns 200" | ✏️ | Labelled as "docs" but came from a 3rd-party site. Verified later on Stripe's official errors page. | wrong source |
| 2026-11-12 | Stripe test ideas: C4 duplicate email | ✏️ | Expected result based on a 3rd-party blog, not Stripe docs. Must be verified by running. | wrong source |
| 2026-11-12 | Stripe test ideas: C5, P5 | ⏳ | AI marked them [ASSUMPTION] — expected results not in docs. To check when Stripe tests run. | assumption |
| 2026-11-12 | Stripe test ideas: C2 empty customer | ✅ | Correct per docs, but raised a requirement question: should our app allow empty customers? | requirement question |
| 2026-11-12 | Stripe test ideas: missing cases | ✏️ | AI missed: insufficient funds decline (P8), customer with tax/address (C6). Added by me. | missing case |
| 2026-11-13 | Test plan draft | ✏️ | Draft had a "Status" column claiming finished work that wasn't run. Rewrote as forward-looking plan + honest progress line. | overclaim |
| 2026-11-13 | Frankfurter pytest tests (3) | ✏️ | All 3 passed. But invalid-currency test accepts any 4xx — not one specific expected result. | weak assertion |

Verdict: ✅ accepted · ✏️ fixed · ❌ rejected · ⏳ open
Type: wrong fact · wrong assumption · missing case · missing context · weak assertion · wrong source · assumption · outdated info · outdated dependency · overclaim · setup / config · requirement question

## 📊 Weekly AI metrics (Fridays)

Counted per test idea / output (F1–F8 row = 6 outputs). Open (⏳) items are not counted.

| Week | Outputs reviewed | ✅ | ✏️ | ❌ | Acceptance rate |
|------|------------------|----|----|----|-----------------|
| 1    | 22 (+2 open)     | 9  | 13 | 0  | 41%             |

**Week 1 insight:** Most fixes were weak assertions and wrong/unverified sources. AI listed documented parameters well but missed real payment risks (insufficient funds, tax/address case) — those were added by the human reviewer. Running the tests raised the acceptance rate: several AI ideas turned out correct only once actually executed.
| 2026-11-16 | Stripe key setup | ✅ | Real test key in `.env` only. Verified: `git status` shows only `.env.example` changed; `git grep sk_test` finds only the placeholder. | — |
| 2026-11-16 | Stripe Customer CRUD tests (4) | ✅ | All 4 passed first time against Stripe test mode. Update uses POST — matches Stripe docs, not invented. | — |
| 2026-11-16 | CRUD: read-after-delete assertion | ✅ | AI marked it [ASSUMPTION]; confirmed by running, not by docs. | assumption |
| 2026-11-16 | CRUD: fixture cleanup | ⏳ | Teardown DELETE doesn't check the response (silent failure risk). Cleanup NOT yet verified: Dashboard showed 0 customers, but in a different sandbox — key in `.env` (…03zP) doesn't match that sandbox's key. | silent failure / wrong environment |
| 2026-11-16 | AI review of cleanup evidence | ✏️ | AI concluded "0 customers = cleanup works" without checking which sandbox the key belonged to. Caught by human reviewer. | wrong assumption |