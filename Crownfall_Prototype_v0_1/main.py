
import os
import random

from engine.kingdom import Kingdom
from engine.events import check_events
from engine.chronicle import Chronicle

SEASONS = ["Spring", "Summer", "Autumn", "Winter"]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def bar(value, maximum, width=20):
    if maximum <= 0:
        return "-" * width
    filled = int((clamp(value, 0, maximum) / maximum) * width)
    return "█" * filled + "░" * (width - filled)


def render_status(kingdom, season, turn):
    print("=== Crownfall Prototype v0.5 ===")
    print(f"Week {turn} | Season: {season}")
    print("-" * 56)
    print(
        f"Population {kingdom.population:>3} "
        f"[{bar(kingdom.population, 100)}]"
    )
    print(f"Food       {int(kingdom.food):>3} [{bar(kingdom.food, 200)}]")
    print(f"Gold       {kingdom.gold:>3} [{bar(kingdom.gold, 200)}]")
    print(f"Morale     {kingdom.morale:>3} [{bar(kingdom.morale, 100)}]")
    print(f"Loyalty    {kingdom.loyalty:>3} [{bar(kingdom.loyalty, 100)}]")
    print(f"Army       {kingdom.army:>3}  | Farms {kingdom.farms} ")
    print(f"Mines      {kingdom.mines:>3}  | Infra {kingdom.infrastructure}")
    print(f"Housing    {kingdom.housing:>3}  | Unrest {kingdom.unrest:>3}")
    print(f"Stability  {kingdom.stability:>3} [{bar(kingdom.stability, 100)}]")
    print(f"Tax rate   x{kingdom.tax_rate:.1f} | Focus {kingdom.focus}")
    print("-" * 56)


def choose_action(kingdom):
    print("Council actions:")
    print("1) Build farm (25 gold)")
    print("2) Build mine (30 gold)")
    print("3) Build infrastructure (40 gold)")
    print("4) Build housing (35 gold)")
    print("5) Host feast (15 food)")
    print("6) Levy extra taxes")
    print("7) Recruit soldiers (20 gold)")
    print("8) Hold royal parade (10 gold)")
    print("9) Send relief aid (15 gold)")
    print("10) Set focus: Economy")
    print("11) Set focus: Welfare")
    print("12) Set focus: Military")
    print("13) Set focus: Balanced")
    print("14) Review last chronicle entry")
    print("15) Wait")
    try:
        choice = input("Choose an action (1-15): ").strip()
    except EOFError:
        choice = "15"
    options = {
        "1": "build_farm",
        "2": "build_mine",
        "3": "build_infra",
        "4": "build_housing",
        "5": "feast",
        "6": "tax",
        "7": "recruit",
        "8": "parade",
        "9": "aid",
        "10": "focus_economy",
        "11": "focus_welfare",
        "12": "focus_military",
        "13": "focus_balanced",
        "14": "review",
        "15": "wait",
    }
    selection = options.get(choice, "wait")
    if selection == "review":
        return selection
    if selection == "build_farm" and kingdom.gold < 25:
        print("Not enough gold.")
        return "wait"
    if selection == "build_mine" and kingdom.gold < 30:
        print("Not enough gold.")
        return "wait"
    if selection == "build_infra" and kingdom.gold < 40:
        print("Not enough gold.")
        return "wait"
    if selection == "build_housing" and kingdom.gold < 35:
        print("Not enough gold.")
        return "wait"
    if selection == "feast" and kingdom.food < 15:
        print("Not enough food.")
        return "wait"
    if selection == "recruit" and kingdom.gold < 20:
        print("Not enough gold.")
        return "wait"
    if selection == "parade" and kingdom.gold < 10:
        print("Not enough gold.")
        return "wait"
    if selection == "aid" and kingdom.gold < 15:
        print("Not enough gold.")
        return "wait"
    return selection


def pause():
    try:
        input("\nPress Enter to continue...")
    except EOFError:
        return

def get_config():
    try:
        weeks = int(input("Number of weeks to simulate (default 52): ").strip() or "52")
    except EOFError:
        weeks = 52
    except ValueError:
        weeks = 52
    try:
        seed_value = input("Random seed (blank for random): ").strip()
    except EOFError:
        seed_value = ""
    if seed_value:
        random.seed(seed_value)
    else:
        random.seed()
    return weeks


kingdom = Kingdom()
chronicle = Chronicle()
total_weeks = get_config()

for turn in range(1, total_weeks + 1):
    season = SEASONS[(turn - 1) % len(SEASONS)]
    chronicle.start_turn()
    clear_screen()
    render_status(kingdom, season, turn)
    action = choose_action(kingdom)
    if action == "review":
        clear_screen()
        render_status(kingdom, season, turn)
        if chronicle.entries:
            print("Last chronicle entry:")
            print("-", chronicle.entries[-1])
        else:
            print("No chronicle entries yet.")
        pause()
        action = "wait"
    kingdom.apply_action(action, chronicle)
    kingdom.produce(season)
    kingdom.consume(season)
    check_events(kingdom, chronicle, season)
    kingdom.end_turn_adjustments(chronicle)
    chronicle.log_turn(kingdom)

    kingdom.display()
    print("\nTurn recap:")
    for entry in chronicle.last_turn_entries():
        print("-", entry)
    pause()

    if kingdom.collapsed:
        print("\n💀 The kingdom has collapsed.")
        break

print("\n=== CHRONICLE ===")
chronicle.print()
