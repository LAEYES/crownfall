
import os

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
    print("=== Crownfall Prototype v0.3 ===")
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
    print(f"Tax rate   x{kingdom.tax_rate:.1f}")
    print("-" * 56)


def choose_action(kingdom):
    print("Council actions:")
    print("1) Build farm (25 gold)")
    print("2) Build mine (30 gold)")
    print("3) Build infrastructure (40 gold)")
    print("4) Host feast (15 food)")
    print("5) Levy extra taxes")
    print("6) Recruit soldiers (20 gold)")
    print("7) Review last chronicle entry")
    print("8) Wait")
    try:
        choice = input("Choose an action (1-8): ").strip()
    except EOFError:
        choice = "8"
    options = {
        "1": "build_farm",
        "2": "build_mine",
        "3": "build_infra",
        "4": "feast",
        "5": "tax",
        "6": "recruit",
        "7": "review",
        "8": "wait",
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
    if selection == "feast" and kingdom.food < 15:
        print("Not enough food.")
        return "wait"
    if selection == "recruit" and kingdom.gold < 20:
        print("Not enough gold.")
        return "wait"
    return selection


def pause():
    try:
        input("\nPress Enter to continue...")
    except EOFError:
        return

kingdom = Kingdom()
chronicle = Chronicle()

for turn in range(1, 101):
    season = SEASONS[(turn - 1) % len(SEASONS)]
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
    chronicle.log_turn(kingdom)

    kingdom.display()
    pause()

    if kingdom.collapsed:
        print("\n💀 The kingdom has collapsed.")
        break

print("\n=== CHRONICLE ===")
chronicle.print()
