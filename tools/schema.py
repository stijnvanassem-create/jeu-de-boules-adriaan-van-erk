#!/usr/bin/env python3
"""Genereert per baan een vast speelschema van 4 rondes triplette (3 tegen 3).

Regels:
  - elke ronde een andere teamsamenstelling (geen enkel trio komt twee keer voor);
  - bij 7 spelers rust er elke ronde een ander (niemand rust twee keer voordat
    iedereen een keer gerust heeft; bij 4 rondes zijn dat dus 4 verschillende rusters);
  - minimaliseer herhaalde teamgenoten, daarna spreid tegenstanders zo gelijk mogelijk.

Zoekt exhaustief (6 spelers: alle 10 indelingen; 7 spelers: alle indelingen per
rustvolgorde) en kiest bij gelijke score deterministisch de eerste.

Gebruik:  python3 tools/schema.py          -> print schema's
          python3 tools/schema.py --js     -> print het JS-blok voor index.html
"""
import itertools
import json
import random
import sys

BANEN = {
    1: ["Stefen", "Hanna G", "Juliëtte", "Joost", "Gordon", "Ardin"],
    2: ["Bert", "Renata", "Niels", "Gert", "Emil", "Pieter Jan"],
    3: ["Myrna", "Roxanne", "Bartjan", "Louis", "Ronnie", "Annika"],
    4: ["Johan", "Hanna K", "Marcel", "Bart", "Abby", "Roos"],
}
RONDES = 4


def splits(players):
    """Alle manieren om 6 spelers in twee teams van 3 te verdelen (10 stuks)."""
    first = players[0]
    rest = players[1:]
    out = []
    for mates in itertools.combinations(rest, 2):
        a = (first,) + mates
        b = tuple(p for p in players if p not in a)
        out.append((a, b))
    return out


def score(rounds, n):
    """Lager is beter. Tuple: (max teamgenoot-herhaling, som kwadraten teamgenoten,
    spreiding tegenstanders, max tegenstander-telling)."""
    mate = {}
    opp = {}
    for a, b, _rest in rounds:
        for team in (a, b):
            for x, y in itertools.combinations(sorted(team), 2):
                mate[(x, y)] = mate.get((x, y), 0) + 1
        for x in a:
            for y in b:
                k = (min(x, y), max(x, y))
                opp[k] = opp.get(k, 0) + 1
    pairs = list(itertools.combinations(range(n), 2))
    m = [mate.get(p, 0) for p in pairs]
    o = [opp.get(p, 0) for p in pairs]
    mean_o = sum(o) / len(o)
    var_o = sum((v - mean_o) ** 2 for v in o)
    return (max(m), sum(v * v for v in m), round(var_o, 6), max(o))


def solve(n, seed):
    idx = list(range(n))
    best = None
    if n == 6:
        rest_orders = [[None] * RONDES]
    else:
        # Rust is per definitie eerlijk (4 verschillende rusters). Welke 4 en in welke
        # volgorde maakt voor de kwaliteit niet uit (symmetrie), dus vaste geseede loting.
        rng = random.Random(seed)
        order = idx[:]
        rng.shuffle(order)
        rest_orders = [order[:RONDES]]
    for rests in rest_orders:
        options = []
        for r in rests:
            playing = [p for p in idx if p != r]
            options.append([(a, b, r) for a, b in splits(playing)])
        for combo in itertools.product(*options):
            trios = [frozenset(t) for a, b, _ in combo for t in (a, b)]
            if len(set(trios)) != len(trios):
                continue  # elke ronde andere samenstelling, geen trio dubbel
            s = score(combo, n)
            if best is None or s < best[0]:
                best = (s, combo)
    return best


def main():
    result = {}
    report = []
    for baan, names in BANEN.items():
        n = len(names)
        s, combo = solve(n, seed=baan)
        rounds = []
        for a, b, r in combo:
            rounds.append({
                "a": [names[i] for i in a],
                "b": [names[i] for i in b],
                "rest": names[r] if r is not None else None,
            })
        result[baan] = rounds
        report.append((baan, names, rounds, s))

    if "--js" in sys.argv:
        print("const SCHEDULE = " + json.dumps(result, ensure_ascii=False) + ";")
        return

    for baan, names, rounds, s in report:
        print(f"BAAN {baan}  ({len(names)} spelers: {', '.join(names)})")
        for i, r in enumerate(rounds, 1):
            line = f"  Partij {i}:  {' + '.join(r['a'])}  vs  {' + '.join(r['b'])}"
            if r["rest"]:
                line += f"   | rust: {r['rest']}"
            print(line)
        # controle-tellingen
        mate, opp, played = {}, {}, {p: 0 for p in names}
        for r in rounds:
            for t in (r["a"], r["b"]):
                for p in t:
                    played[p] += 1
                for x, y in itertools.combinations(sorted(t), 2):
                    mate[(x, y)] = mate.get((x, y), 0) + 1
        hist = {}
        for p in itertools.combinations(sorted(names), 2):
            c = mate.get(p, 0)
            hist[c] = hist.get(c, 0) + 1
        print(f"  Controle: max {s[0]}x samen in een team; paren per aantal keer teamgenoot: "
              + ", ".join(f"{k}x: {v}" for k, v in sorted(hist.items())))
        print("  Partijen gespeeld: " + ", ".join(f"{p} {c}" for p, c in played.items()))
        print()


if __name__ == "__main__":
    main()
