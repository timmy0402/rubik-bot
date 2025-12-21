import json
import os
import sys

# Add src to sys.path to import AlgorithmsView
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)

try:
    from algorithms import AlgorithmsView
except ImportError as e:
    print(f"FAIL: Could not import AlgorithmsView: {e}")
    sys.exit(1)


# Monkeypatch discord.ui.View to avoid event loop requirement
import discord.ui

discord.ui.View.__init__ = lambda self, timeout=180: None


class MockUser:
    id = 123
    name = "TestUser"


def test_mappings():
    print("Initializing AlgorithmsView (OLL)...")
    try:
        view = AlgorithmsView(mode="oll", user_id=123, userName="TestUser")
    except Exception as e:
        print(f"FAIL: Error initializing view: {e}")
        return

    # Check if alg_data is loaded
    if not hasattr(view, "alg_data") or not view.alg_data:
        print("FAIL: alg_data not loaded in AlgorithmsView")
        return

    print("Checking OLL Groups...")
    oll_data = view.alg_data.get("oll", {})
    missing_oll = []
    for group, ids in view.OLL_GROUPS.items():
        for oll_id in ids:
            if oll_id not in oll_data:
                print(f"  MISSING OLL: {oll_id} in group '{group}'")
                missing_oll.append(oll_id)

    if not missing_oll:
        print("SUCCESS: All OLL IDs found.")
    else:
        print(f"FAIL: Missing {len(missing_oll)} OLL algorithms.")

    print("\nChecking PLL Groups...")
    pll_data = view.alg_data.get("pll", {})
    missing_pll = []
    for group, ids in view.PLL.items():
        for pll_id in ids:
            if pll_id not in pll_data:
                print(f"  MISSING PLL: {pll_id} in group '{group}'")
                missing_pll.append(pll_id)

    if not missing_pll:
        print("SUCCESS: All PLL IDs found.")
    else:
        print(f"FAIL: Missing {len(missing_pll)} PLL algorithms.")


if __name__ == "__main__":
    test_mappings()
