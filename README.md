# 🏷️ Annotation Agreement Toolkit

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white) ![No dependencies](https://img.shields.io/badge/dependencies-none-2ea44f?style=flat-square) ![Tests](https://img.shields.io/badge/tests-unittest-2ea44f?style=flat-square) ![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

Measure how consistently annotators label the same data (Cohen's kappa, Fleiss' kappa, percent agreement) and get a list of items to adjudicate.

## Why this exists

On any labeling project, quality starts with consistency. If two trained annotators disagree on the same item, either the guideline is unclear or someone needs feedback. This tool turns a raw label export into an agreement report a QA lead can act on.

## Features

- **Percent agreement**: share of items where every annotator agreed
- **Cohen's kappa** for every pair of annotators (corrects for chance agreement)
- **Fleiss' kappa** across the whole team
- **Landis & Koch interpretation** (slight / fair / moderate / substantial / almost perfect)
- **Adjudication list**: every item with a disagreement, showing who chose what

## Quick start

No installs needed, just Python 3.9+.

```bash
git clone https://github.com/afra-ozi/annotation-agreement.git
cd annotation-agreement
python iaa.py sample_annotations.csv
```

## Input

A long-format CSV with one row per label: `item_id, annotator, label`.

## Sample output

Running `python iaa.py sample_annotations.csv` on the included sample data:

# Inter-annotator agreement report

Items: 8
Percent agreement: 62.5%
Fleiss' kappa: 0.617 (substantial)

## Cohen's kappa by annotator pair

- ann_a vs ann_b: 0.619 (substantial)
- ann_a vs ann_c: 0.619 (substantial)
- ann_b vs ann_c: 0.619 (substantial)

## Items to adjudicate

- t02: ann_a=negative, ann_b=negative, ann_c=neutral
- t04: ann_a=positive, ann_b=neutral, ann_c=positive
- t07: ann_a=neutral, ann_b=negative, ann_c=negative

## Tests

```bash
python -m unittest -v test_iaa
```

## License

MIT
