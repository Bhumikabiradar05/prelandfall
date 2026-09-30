"""Honest fixture backtest; production adapter should fetch pre/post Sentinel-1 from EE."""
import json
from pathlib import Path

assets = json.loads((Path(__file__).parents[1] / "data" / "fani_demo.json").read_text())["assets"]
# Cached Sentinel-1 interpretation deliberately incomplete: likely peak inundation may be missed.
observed_flooded = {"Puri 33/11 kV Substation", "Marine Drive feeder", "Puri-Konark Road segment", "Town Hall Cyclone Shelter"}
predicted = {asset["name"] for asset in assets if asset["base_risk"] >= 70}
true_positive = len(predicted & observed_flooded)
precision = true_positive / len(predicted) if predicted else 0
recall = true_positive / len(observed_flooded) if observed_flooded else 0
print(f"Fani cached backtest — precision: {precision:.2f}; recall: {recall:.2f}")
print("Limit: Sentinel-1 may miss the flood peak because of acquisition timing, radar shadow, vegetation and wind effects.")
