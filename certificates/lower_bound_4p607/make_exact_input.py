"""Compile rational JSON to exact integer input for the independent C++ kernel."""
from __future__ import annotations
import argparse
import json
import math
from fractions import Fraction as F
from pathlib import Path
from typing import Any


def compile_record(record: dict[str, Any], path: str | Path) -> tuple[int, int]:
    """Preserve coordinates and weights exactly; geometric validity is checked in C++."""
    if record.get("angle_limit") != "207107/500000":
        raise ValueError("This proof kernel uses angle_limit=207107/500000.")
    steps = record["direction_steps"]
    if isinstance(steps, bool) or not isinstance(steps, int):
        raise ValueError("direction_steps must be an integer.")
    L, B = F(record["outer_side"]), F(record["square_side"])
    atoms = [tuple(map(F, row)) for row in record["atoms"]]
    if not atoms or any(len(row) != 3 for row in atoms):
        raise ValueError("Expected a nonempty array of [x, y, weight] atoms.")
    G = math.lcm((L/2).denominator, (B/2).denominator,
                 *(value.denominator for x, y, _ in atoms for value in (x-L/2, y-L/2)))
    W = math.lcm(*(w.denominator for _, _, w in atoms))
    lines = [f"{len(atoms)} {steps} {G} {int(L*G/2)} {int(B*G/2)} {W}"]
    lines.extend(f"{int((x-L/2)*G)} {int((y-L/2)*G)} {int(w*W)}" for x, y, w in atoms)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return G, W


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    record = json.loads(args.certificate.read_text(encoding="utf-8"))
    G, W = compile_record(record, args.output)
    print(f"coordinate_scale={G} weight_denominator={W}")


if __name__ == "__main__":
    main()
