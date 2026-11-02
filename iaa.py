"""Inter-annotator agreement (IAA) toolkit.

Reads a long-format CSV (item_id, annotator, label) and reports:
- percent agreement
- Cohen's kappa for every pair of annotators
- Fleiss' kappa across all annotators
- the items annotators disagreed on, for review/adjudication

Usage:
    python iaa.py sample_annotations.csv
"""
import csv
import sys
from collections import Counter, defaultdict
from itertools import combinations


def load(path):
    """Return {item_id: {annotator: label}} from a CSV file."""
    data = defaultdict(dict)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            data[row["item_id"].strip()][row["annotator"].strip()] = row["label"].strip()
    return dict(data)


def percent_agreement(data):
    """Share of items where every annotator chose the same label."""
    items = [labels for labels in data.values() if len(labels) > 1]
    if not items:
        return 0.0
    agreed = sum(1 for labels in items if len(set(labels.values())) == 1)
    return agreed / len(items)


def cohen_kappa(a, b):
    """Cohen's kappa for two equal-length label lists."""
    if len(a) != len(b) or not a:
        raise ValueError("label lists must be non-empty and the same length")
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    expected = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    if expected == 1:
        return 1.0
    return (observed - expected) / (1 - expected)


def pairwise_kappa(data):
    """Cohen's kappa for every annotator pair, using items both labeled."""
    annotators = sorted({a for labels in data.values() for a in labels})
    results = {}
    for x, y in combinations(annotators, 2):
        shared = [i for i, labels in data.items() if x in labels and y in labels]
        if shared:
            results[(x, y)] = cohen_kappa([data[i][x] for i in shared], [data[i][y] for i in shared])
    return results


def fleiss_kappa(data):
    """Fleiss' kappa over items that have the same number of ratings."""
    counts = Counter(len(labels) for labels in data.values())
    if not counts:
        raise ValueError("no data")
    n_raters = counts.most_common(1)[0][0]
    items = [list(l.values()) for l in data.values() if len(l) == n_raters]
    if n_raters < 2:
        raise ValueError("need at least two ratings per item")
    categories = sorted({lab for labels in items for lab in labels})
    N = len(items)
    p_j = {c: 0 for c in categories}
    P_i = []
    for labels in items:
        c = Counter(labels)
        for k in categories:
            p_j[k] += c[k]
        P_i.append((sum(v * v for v in c.values()) - n_raters) / (n_raters * (n_raters - 1)))
    total = N * n_raters
    P_bar = sum(P_i) / N
    P_e = sum((v / total) ** 2 for v in p_j.values())
    if P_e == 1:
        return 1.0
    return (P_bar - P_e) / (1 - P_e)


def disagreements(data):
    """Items where annotators did not all choose the same label."""
    return {i: labels for i, labels in data.items() if len(set(labels.values())) > 1}


def interpret(k):
    """Landis & Koch (1977) interpretation of a kappa value."""
    if k < 0:
        return "poor"
    for limit, word in [(0.2, "slight"), (0.4, "fair"), (0.6, "moderate"), (0.8, "substantial")]:
        if k <= limit:
            return word
    return "almost perfect"


def report(data):
    lines = ["# Inter-annotator agreement report", ""]
    lines.append(f"Items: {len(data)}")
    lines.append(f"Percent agreement: {percent_agreement(data):.1%}")
    fk = fleiss_kappa(data)
    lines.append(f"Fleiss' kappa: {fk:.3f} ({interpret(fk)})")
    lines += ["", "## Cohen's kappa by annotator pair", ""]
    for (x, y), k in pairwise_kappa(data).items():
        lines.append(f"- {x} vs {y}: {k:.3f} ({interpret(k)})")
    lines += ["", "## Items to adjudicate", ""]
    for item, labels in disagreements(data).items():
        lines.append(f"- {item}: " + ", ".join(f"{a}={l}" for a, l in sorted(labels.items())))
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python iaa.py annotations.csv")
    print(report(load(sys.argv[1])))
