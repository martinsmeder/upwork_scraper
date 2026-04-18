# Data Processing

## Goal

Turn scraped Upwork jobs into a useful summary of what clients actually want built or improved, starting with `output/full-stack-jobs.json`.

The first version should ignore duplicate detection and focus on a stable taxonomy that is specific enough to reveal recurring demand patterns, but not so narrow that every fifth job needs its own category.

## Classification Rules

- Use a fixed taxonomy. Do not allow free-form category creation during classification.
- Assign exactly one `delivery_type` to each job.
- Assign exactly one `solution_category` to each job.
- Classify from the combined `title` and `description`.
- Classify by client outcome, not by framework names alone.
- Prefer the main use case over secondary features.
- Avoid vague catch-all labels unless they are explicitly defined and intentionally narrow.

## Taxonomy

Use the following fixed taxonomy for the `full-stack` dataset.

### `delivery_type`

- SaaS product
- Internal business tool
- Client or customer portal
- Mobile plus web product
- E-commerce system
- Marketplace or directory platform
- AI-enabled application
- Automation or integration system
- Dashboard or analytics application
- API or backend module

### `solution_category`

- CRM and lead pipeline
- Customer support inbox
- Scheduling and appointment booking
- Quoting and pricing tool
- Marketplace and listings platform
- Member portal
- Analytics dashboard
- Document and form processing
- AI chatbot or agent workspace
- E-commerce checkout and subscription flow
- Admin portal
- Case management system
- Operations back-office system
- Approval and review system
- Project and task management workspace
- Not specified
- Content publishing and automation workflow
- Field operations and dispatch system
- Billing and invoicing system
- Hiring and applicant portal
- Referral and loyalty system
- Online ordering and restaurant workflow
- Website builder or multi-tenant CMS

### Notes on ambiguous cases

- Do not use a generic fallback category. Pick the closest concrete product shape even if the post describes a broader SaaS platform.
- Prefer `Member portal` when the core experience is a logged-in area for clients, patients, members, researchers, or partners to access records, workflows, or service interactions.
- Prefer `Admin portal` for staff-facing hubs centered on user management, permissions, settings, navigation, and day-to-day internal operations.
- Prefer `Case management system` for software built around intake, processing, assignment, tracking, and resolution of individual records, requests, claims, matters, or service cases.
- Prefer `Operations back-office system` for internal staff tools centered on day-to-day processing, operational control, record management, and multi-step business workflows.
- Prefer `Approval and review system` when the core workflow is verification, QA, compliance, adjudication, moderation, or approval of records, documents, or decisions.
- Prefer `Project and task management workspace` for collaborative planning, task tracking, execution, and team coordination software.
- Use `Not specified` only when the posting does not reveal enough about the product shape to choose a concrete buildable category with confidence.
- Prefer `Analytics dashboard` only when reporting, KPI visibility, scorecards, monitoring, or decision support is the main client outcome.
- Prefer `Billing and invoicing system` when invoices, recurring charges, payments, subscriptions, or financial account workflows are central.
- Prefer `E-commerce checkout and subscription flow` for storefront, cart, checkout, subscription purchase, funnel, and merchant purchase experiences.
- Prefer `Marketplace and listings platform` for multi-seller, directory, classifieds, rental, or listing-based products.
- Prefer `AI chatbot or agent workspace` only when conversation, agent execution, copilots, or AI-driven workspaces are the product itself rather than a feature inside another system.
- Prefer `Content publishing and automation workflow` for systems centered on content generation, scheduling, approval, and distribution.
- Prefer `Document and form processing` when capture, upload, parsing, review, generation, or workflow around forms, PDFs, or documents is central.

## Output Files

Save both:

- `output/full-stack-classified.json`: original job rows plus classification fields
- `output/full-stack-category-summary.json`: counts and shares grouped by `delivery_type`, `solution_category`, and their combinations

Saving job-level classifications is required so the taxonomy can be revised later without re-scraping.

## Next Steps

- [x] Read through `output/full-stack-jobs.json` to decide on final taxonomy
- [x] Create file `output/full-stack-classified.json`, where each job has it's
      `delivery_type` and `solution_category` classification
- [ ] Count classifications to create the final output
      `output/full-stack-summary.json`, which shows the counts for each delivery type, solution category, and combination of both
