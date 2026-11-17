# AI Findings Log

Every AI output in this project is reviewed by a human tester before it is trusted.
This log records what the AI got right, what had to be fixed, and why.

**Result:** Kept = correct as written · Fixed = needed a change · Rejected = thrown away · Open = not decided yet

## Week 1 (9–13 Nov 2026)

| Date | AI output | Result | What happened | Mistake type |
|------|-----------|--------|---------------|--------------|
| 9 Nov | Frankfurter: status-only test | Fixed | Passed against the wrong URL. Checking only the status code can't catch a wrong endpoint. | Weak assertion |
| 9 Nov | Postman `baseUrl` setup | Fixed | Variable wasn't defined in the active environment. Added it. | Setup |
| 9 Nov | Frankfurter: 8 Postman test ideas | Kept (6 of 8) | 6 ideas passed as written. | — |
| 9 Nov | Frankfurter: invalid currency test | Fixed | Accepted any 4xx code instead of one exact code. | Weak assertion |
| 9 Nov | Frankfurter: "date equals today" | Fixed | Failed: rates are published in the afternoon and not at weekends. AI assumed "always today". | Wrong assumption |
| 10 Nov | Repo setup: `.gitignore` | Kept | `.env` is ignored. Proved with `git check-ignore`. | — |
| 10 Nov | Repo setup: secret scan | Kept | No hard-coded keys. All 9 search hits were false alarms. | — |
| 10 Nov | Repo setup: `requirements.txt` | Open | pytest version pinned to 8.3.4; a newer version exists. | Outdated dependency? |
| 11 Nov | ReqRes: create customer payload | Fixed | Payload didn't match the ReqRes user model. | Wrong assumption |
| 11 Nov | ReqRes: API key header | Fixed | Not needed for this endpoint. Removed. | Outdated info |
| 11 Nov | ReqRes: create customer assertions | Fixed | Only checked status 201. Added checks for name, email, id and created date. | Weak assertion |
| 11 Nov | Test environment | Fixed | Tests ran with the wrong Python environment. Fixed with `python -m pytest`. | Setup |
| 12 Nov | Stripe: "create returns 200" | Fixed | Source was a third-party site, labelled as official docs. Verified on Stripe's docs. | Wrong source |
| 12 Nov | Stripe: duplicate email idea | Fixed | Expected result came from a blog, not Stripe docs. Needs a real run. | Wrong source |
| 12 Nov | Stripe: invalid email, uppercase currency | Open | Expected results not in the docs. To check when the tests run. | Assumption |
| 12 Nov | Stripe: customer with no fields | Kept | Correct per docs. Raised a question: should our app allow empty customers? | — |
| 12 Nov | Stripe: test ideas list | Fixed | Missed insufficient-funds decline and customer with tax address. I added both. | Missing case |
| 13 Nov | Test plan draft | Fixed | Claimed work that hadn't been run. Rewritten as a plan. | Overclaim |
| 13 Nov | Frankfurter: 3 pytest tests | Fixed | All passed, but the invalid-currency test accepts any 4xx code. | Weak assertion |

## Week 2 (16–20 Nov 2026)

| Date | AI output | Result | What happened | Mistake type |
|------|-----------|--------|---------------|--------------|
| 16 Nov | Stripe test key setup | Kept | Key is in `.env` only. Proved with `git status` and `git grep`. | — |
| 16 Nov | Stripe: customer create / read / update / delete tests | Kept | All 4 passed first time. Update uses POST, as in Stripe docs. | — |
| 16 Nov | Stripe: read after delete | Kept | AI marked it as an assumption. Running the test confirmed it. | — |
| 16 Nov | Stripe: test data cleanup | Open | Cleanup doesn't check if the delete worked. Not yet verified: the Dashboard I checked was a different sandbox from the test key. | Silent failure |
| 16 Nov | AI check of cleanup | Fixed | AI said "0 customers, cleanup works" without checking which sandbox the key belonged to. I caught it. | Wrong assumption |

## Weekly metrics

Counted per AI output. Open items are not counted.

| Week | Reviewed | Kept | Fixed | Rejected | Kept as written |
|------|----------|------|-------|----------|-----------------|
| 1 | 22 | 9 | 13 | 0 | 41% |

**Week 1 takeaway:** Most fixes were weak assertions and unverified sources. AI listed the documented parameters well but missed real payment risks, which I added. Running the tests raised the score: some AI ideas turned out to be correct only once they were run.
