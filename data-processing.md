# Data Processing

## File To Process `output/[dataset-name].json`

Confirmed dataset size : X raw jobs
Deduplicated size: Y jobs

## Classification Rules

- Classify every job using the combined `title` and `description`.
- Assign exactly one `delivery_type` and exactly one `solution_category` to each row.
- Use `Not specified` only when the post does not support a concrete category with confidence.
- Classify by the main client problem or business outcome, not by tool names alone.
- Ignore secondary features when one clear primary use case is described.
- Build labels that are useful for strategic service decisions: each label should imply a type of problem worth learning to solve.
- A good label must be specific enough to suggest a sellable service, broad enough to cover multiple rows, and distinct enough not to overlap heavily with another label.
- Prefer problem-oriented labels over implementation-oriented labels unless the implementation itself is the primary thing being bought.
- Treat `Not specified` as a failure state to minimize, not a normal catch-all bucket.
- If many rows fall into a vague bucket, improve the taxonomy before finalizing the dataset.

## Taxonomy Design Standard

- Create a dataset-specific taxonomy file such as `[dataset-name]-taxonomy.md` and finalize it before classification begins.
- Do not assume the taxonomy from a previous dataset should carry over unchanged to a new field.
- For every label you create, ask:
  - Does this describe a real client problem?
  - Would I know what service to sell from this label alone?
  - Will this label recur across multiple rows?
  - Is it clearly different from the other labels?
  - Is this better than placing the row in `Not specified`?
- If two labels feel adjacent or easy to confuse, write a one-sentence tie-break rule for when to choose each one.
- Only keep a generic label if it is still strategically useful. If it does not point to a real type of demand, it is too vague.

## Quality Control

- Deduplicate exact duplicate postings before classification.
- At minimum, remove rows with identical `job_id` or identical `title` + `description`.
- Track raw count and deduplicated count separately.
- After the first classification pass, review every `Not specified` row again.
- Also review the largest categories and any categories that seem adjacent, weak, or overloaded.
- If a row can fit two labels equally well, the taxonomy likely needs a clearer boundary before summary generation.

## Checklist

- [ ] Confirm `output/[dataset-name].json` is the working source file and verify the dataset size.
- [ ] Deduplicate and record raw count vs deduplicated count.
- [ ] Read through the full dataset once to define a problem-oriented taxonomy for `delivery_type` and `solution_category`.
- [ ] Save the final taxonomy in `[dataset-name]-taxonomy.md` before classification starts so labels stay consistent across all rows.
- [ ] Write tie-break rules for any labels that are close enough to be confused during classification.
- [ ] Perform classification
- [ ] Save the job-level output as `output/[dataset-name]-classified.json`.
- [ ] Read through `output/[dataset-name]-classified.json` in full to verify the classifications are consistent and correct.
- [ ] Re-review all `Not specified` rows and any overloaded categories.
- [ ] Correct any weak, under-specific, or inconsistent classifications in `output/[dataset-name]-classified.json`.
- [ ] Count classifications by `delivery_type`, `solution_category`, and their combinations.
- [ ] Save the aggregate output as `output/[dataset-name]-summary.json`.
- [ ] Verify that all summary totals match the classified dataset exactly.
