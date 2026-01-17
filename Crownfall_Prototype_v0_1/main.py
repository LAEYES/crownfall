
from engine.kingdom import Kingdom
from engine.events import check_events
from engine.chronicle import Chronicle

kingdom = Kingdom()
chronicle = Chronicle()

print("=== Crownfall Prototype v0.1 ===")

for turn in range(1, 101):
    print(f"\n--- Week {turn} ---")
    kingdom.produce()
    kingdom.consume()
    check_events(kingdom, chronicle)
    chronicle.log_turn(kingdom)

    kingdom.display()

    if kingdom.collapsed:
        print("\n💀 The kingdom has collapsed.")
        break

print("\n=== CHRONICLE ===")
chronicle.print()
