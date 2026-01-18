
import os

from engine.kingdom import Kingdom
from engine.events import check_events
from engine.chronicle import Chronicle

SEASONS = ["Spring", "Summer", "Autumn", "Winter"]


def choose_action(turn):
    print("\nCouncil actions:")
    print("1) Build farm (25 gold)")
    print("2) Build mine (30 gold)")
    print("3) Build infrastructure (40 gold)")
    print("4) Host feast (15 food)")
    print("5) Levy extra taxes")
    print("6) Recruit soldiers (20 gold)")
    print("7) Wait")
    try:
        choice = input("Choose an action (1-7): ").strip()
    except EOFError:
        choice = "7"
    options = {
        "1": "build_farm",
        "2": "build_mine",
        "3": "build_infra",
        "4": "feast",
        "5": "tax",
        "6": "recruit",
        "7": "wait",
    }
    return options.get(choice, "wait")

kingdom = Kingdom()
chronicle = Chronicle()
total_weeks = get_config()

print("=== Crownfall Prototype v0.2 ===")

for turn in range(1, 101):
    season = SEASONS[(turn - 1) % len(SEASONS)]
    print(f"\n--- Week {turn} ---")
    print(f"Season: {season}")
    action = choose_action(turn)
    kingdom.apply_action(action, chronicle)
    kingdom.produce(season)
    kingdom.consume(season)
    check_events(kingdom, chronicle, season)
    chronicle.log_turn(kingdom)

    kingdom.display()
    pause()

    if kingdom.collapsed:
        print("\n💀 The kingdom has collapsed.")
        break

print("\n=== CHRONICLE ===")
chronicle.print()
