# AI-Assisted API Testing (Fintech)

API test suite built with an AI-assisted workflow: AI drafts, a human tester
reviews, and every AI mistake is logged in `AI_FINDINGS.md`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
python -m pytest
```

## Structure

| Path | Purpose |
|------|---------|
| `tests/` | pytest + requests API tests |
| `postman/` | Postman collection for exploratory runs |
| `.env.example` | Config template (real `.env` is git-ignored) |
| `AI_FINDINGS.md` | Log of AI output reviewed, fixed or rejected |

## Test Plan

### Objective
Evaluate how reliable AI-generated API tests are for fintech APIs, and show
how a human tester reviews, fixes or rejects AI output before it is trusted.

### APIs in scope
| API | Why | What will be tested |
|-----|-----|---------------------|
| Frankfurter (`/latest`) | Simple read-only API to set up the workflow | Response structure, query parameters, negative cases |
| ReqRes (`/api/users`) | Public demo API that accepts writes | Create a customer (POST): status + response body |
| Stripe (test mode) | Real fintech API | Customers + PaymentIntents: creation, validation, card declines |

### Approach
1. AI generates the artefact (test ideas, code, data) from official docs.
2. A human tester reviews it: runs it, checks the expected result against a named source, then keeps, fixes or rejects it.
3. Every AI mistake is logged in `AI_FINDINGS.md` with a type.
4. Weekly metrics track how often AI output is accepted as-is.

### Test types
- Functional: happy path, parameters, required fields
- Negative: invalid input, missing parameters, missing auth
- Payment-specific (Stripe): declined cards, insufficient funds, amount format rules
- Security hygiene: `.env` git-ignored, no hard-coded secrets

### Tools
pytest · requests · python-dotenv · Postman

### Exit criteria
Every test has one specific expected result from a named source, and every
AI_FINDINGS item is either closed or marked open.

### Out of scope
Performance and load testing, UI testing, live (non-test-mode) payments.

### Known risks
- Demo APIs accept any payload, so a passing test proves little without body assertions.
- AI may present third-party sources as official docs.
- Tests currently run from the conda environment, not the project `.venv`.

### Progress
Week 1: workflow set up, first tests drafted and reviewed, Stripe test ideas reviewed. See `AI_FINDINGS.md`.

## Test Cases

Status: **Automated** = test code exists · **Designed** = idea reviewed, not yet coded · **Not run** = code exists but results not yet reviewed

### AI-generated (reviewed by human)

| ID | API | Test case | Expected result | Source | Verdict | Status |
|----|-----|-----------|-----------------|--------|---------|--------|
| F1–F8 | Frankfurter | 8 ideas for `GET /latest` (structure, base, symbols, amount, date, rates) | See Postman collection | AI, no docs given | ⏳ | Not run |
| R1 | ReqRes | Create a customer (POST `/users`) | 201 | ReqRes docs | ✏️ assertion only checked status | Automated |
| C1 | Stripe | Create customer with name + email | 200, `id` starts with `cus_`, email echoed | Stripe docs | ✅ | Designed |
| C2 | Stripe | Create customer with no fields | 200 — no required fields | Stripe docs | ✏️ raises requirement question | Designed |
| C3 | Stripe | Customer created with test key | `livemode` = false | Stripe docs | ✅ | Designed |
| C4 | Stripe | Same email twice | Two different customer IDs | 3rd-party blog | ✏️ source to verify; duplicate-data risk | Designed |
| C5 | Stripe | Invalid email format | Error — to be confirmed | Assumption | ✏️ expected result unknown | Designed |
| P1 | Stripe | `amount=2000`, `currency=gbp` | 200, `status` = `requires_payment_method` | Stripe docs | ✅ | Designed |
| P2 | Stripe | Missing `amount` | 400 | Stripe docs | ✅ | Designed |
| P3 | Stripe | Decimal amount (`20.00`) | Error — integer in smallest unit | Stripe docs | ✅ | Designed |
| P4 | Stripe | 9-digit amount | Error — max 8 digits | Stripe docs | ✅ | Designed |
| P5 | Stripe | Uppercase currency (`GBP`) | To be confirmed | Assumption | ✏️ check real response | Designed |
| P6 | Stripe | PaymentIntent linked to customer | `customer` = the `cus_` ID | Stripe docs | ✅ | Designed |
| P7 | Stripe | No API key | 401 | Stripe errors docs | ✏️ AI had no source; confirmed | Designed |

### Added by human tester

| ID | API | Test case | Expected result | Why it was added |
|----|-----|-----------|-----------------|------------------|
| R1+ | ReqRes | Create a customer — body checks | `first_name`, `last_name`, `email` echoed; `id` not empty; `createdAt` present | AI test would pass even if the data was wrong |
| C6a | Stripe | Customer with address + tax info | 200, address saved | Docs: address required when calculating tax — AI didn't test it |
| C6b | Stripe | Tax calculation without address | Error — to be confirmed | Negative side of C6a |
| P8 | Stripe | £30.00 with an insufficient-funds test card | 402, `decline_code` = `insufficient_funds`, `amount_received` = 0 | Real payment risk AI missed |

**Summary:** 14 AI test ideas reviewed (7 ✅, 6 ✏️, 1 ⏳) · 4 cases added by the human tester, all for payment risks or weak assertions the AI missed.
