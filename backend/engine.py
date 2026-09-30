"""Screening-only cached risk engine. It never represents a hydrodynamic model."""
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
import json

DATA = Path(__file__).parents[1] / "data" / "fani_demo.json"
SURGE = {"low": 1.2, "mid": 2.0, "high": 3.1}


def load_fixture():
    return json.loads(DATA.read_text(encoding="utf-8"))


def scenario(level: str):
    if level not in SURGE:
        level = "mid"
    payload = deepcopy(load_fixture())
    factor = {"low": 0.62, "mid": 0.82, "high": 1.0}[level]
    for asset in payload["assets"]:
        asset["risk"] = round(min(99, asset["base_risk"] * factor))
        asset["status"] = "flooded" if asset["risk"] >= 70 else "at risk" if asset["risk"] >= 40 else "watch"
    payload["assets"].sort(key=lambda item: item["risk"], reverse=True)
    payload["scenario"] = {"level": level, "surge_m": SURGE[level], "label": "Screening-level, not a hydrodynamic simulation"}
    payload["isolated_wards"] = [ward for ward in payload["wards"] if ward["threshold"] <= SURGE[level]]
    payload["flooded_shelters"] = [asset for asset in payload["assets"] if asset["type"] == "Shelter" and asset["risk"] >= 70]
    return payload


def metrics(level: str):
    result = scenario(level)
    assets = result["assets"]
    return {"surge_m": result["scenario"]["surge_m"], "assets_at_risk": len([a for a in assets if a["risk"] >= 40]), "critical_assets": len([a for a in assets if a["risk"] >= 70]), "isolated_wards": len(result["isolated_wards"]), "flooded_shelters": len(result["flooded_shelters"])}
