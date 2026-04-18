# Data Processing

## File To Process `output/[file-name].json`

## Classification Rules

- Classify every job using the combined `title` and `description`.
- Assign exactly one `delivery_type` and exactly one `solution_category` to each row.
- Use `Not specified` only when the post does not support a concrete category with confidence.
- Classify by the main client outcome, not by tool names alone.
- Ignore secondary features when one clear primary use case is described.

## Fixed Taxonomy

### `delivery_type`

- ???

### `solution_category`

- ???

## Checklist

- [ ] Confirm `output/[file-name].json` is the working source file and verify the dataset size.
- [ ] Read through the full dataset once to define a fixed taxonomy for `delivery_type` and `solution_category`.
- [ ] Write down the final taxonomy clearly in this file before classification starts so labels stay consistent across all rows.
- [ ] Perform classification
- [ ] Save the job-level output as `output/[file-name]-classified.json`.
- [ ] Read through `output/[file-name]-classified.json` in full to verify the classifications are consistent and correct.
- [ ] Correct any weak, over-specific, or inconsistent classifications in `output/[file-name]-classified.json`.
- [ ] Count classifications by `delivery_type`, `solution_category`, and their combinations.
- [ ] Save the aggregate output as `output/[file-name]-summary.json`.
- [ ] Verify that all summary totals match the classified dataset exactly.
