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

Example `delivery_type` values:

- SaaS product
- Internal tool
- Client-facing web app
- Mobile plus web product
- E-commerce system
- Marketplace platform
- API or backend platform
- AI-enabled application
- Automation system
- Dashboard or analytics app

Example `solution_category` values:

- CRM and lead pipeline
- Customer support inbox
- Scheduling and appointment booking
- Quoting and pricing tools
- Marketplace and listings
- Member portal
- Analytics dashboard
- Document and form processing
- AI chatbot or agent workspace
- E-commerce operations
- Internal admin tooling
- Content publishing workflow
- Field operations and dispatch
- Finance and billing workflow
- Hiring and applicant workflow

## Output Files

Save both:

- `output/full-stack-classified.json`: original job rows plus classification fields
- `output/full-stack-category-summary.json`: counts and shares grouped by `delivery_type`, `solution_category`, and their combinations

Saving job-level classifications is required so the taxonomy can be revised later without re-scraping.

## Next Steps

- [ ] Read through `output/full-stack.json` to decide on final taxonomy
- [ ] Process the the dataset
