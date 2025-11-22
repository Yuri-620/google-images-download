"""A lightweight text-based survival mini-game inspired by *Don't Starve*.

The game is intentionally simple so it can run in a terminal. Players
choose actions each day to gather resources, craft, and manage their
hunger, health, and energy.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class PlayerState:
    """Mutable snapshot of the player's status."""

    health: int = 100
    hunger: int = 50
    energy: int = 100
    day: int = 1
    inventory: Dict[str, int] = field(default_factory=lambda: {"berries": 0, "wood": 0, "stone": 0})
    crafted: List[str] = field(default_factory=list)

    def clamp(self) -> None:
        """Keep core stats within sensible bounds."""

        self.health = max(0, min(100, self.health))
        self.hunger = max(0, min(100, self.hunger))
        self.energy = max(0, min(100, self.energy))


class DontStarveGame:
    """Core simulation for the text-based game."""

    def __init__(self) -> None:
        self.state = PlayerState()

    def gather(self, resource: str) -> str:
        """Gather resources, spending energy and hunger."""

        if resource not in self.state.inventory:
            return f"Unknown resource: {resource}."
        if self.state.energy < 10:
            return "You are too tired to gather anything. Try resting."

        self.state.energy -= 10
        self.state.hunger = max(0, self.state.hunger - 5)
        self.state.inventory[resource] += 1
        return f"You gathered some {resource}."

    def eat(self, item: str) -> str:
        """Eat a food item to restore hunger and a bit of health."""

        if item != "berries":
            return "Only berries are edible for now."
        if self.state.inventory[item] <= 0:
            return "You have no berries to eat."

        self.state.inventory[item] -= 1
        self.state.hunger = min(100, self.state.hunger + 20)
        self.state.health = min(100, self.state.health + 5)
        return "The berries taste fresh and restore your strength."

    def rest(self) -> str:
        """Rest to restore energy at the cost of some hunger."""

        self.state.energy = min(100, self.state.energy + 30)
        self.state.hunger = max(0, self.state.hunger - 10)
        return "You rest by the fire and feel your energy return."

    def craft(self, item: str) -> str:
        """Craft simple items using resources."""

        if item == "campfire":
            if self.state.inventory["wood"] < 2:
                return "You need at least 2 wood to build a campfire."
            self.state.inventory["wood"] -= 2
            self.state.crafted.append("campfire")
            return "You build a small campfire. Nights will be safer now."
        return f"You don't know how to craft {item} yet."

    def end_day(self) -> str:
        """Advance the day counter and apply nightly effects."""

        self.state.day += 1
        self.state.hunger = max(0, self.state.hunger - 15)
        if self.state.hunger == 0:
            self.state.health -= 20
        self.state.clamp()
        return f"Night passes. You survived to day {self.state.day}."

    def is_alive(self) -> bool:
        """Check if the player has health remaining."""

        return self.state.health > 0

    def step(self, action: str, **kwargs: str) -> str:
        """Perform a single game action and return narrative text."""

        actions = {
            "gather": self.gather,
            "eat": self.eat,
            "rest": lambda: self.rest(),
            "craft": self.craft,
            "end_day": lambda: self.end_day(),
        }
        if action not in actions:
            return "Unknown action. Try gather, eat, rest, craft, or end_day."

        handler = actions[action]
        if action in {"gather", "eat", "craft"}:
            item = kwargs.get("item") or kwargs.get("resource")
            if not item:
                return "Specify what you want to interact with."
            return handler(item)  # type: ignore[misc]

        return handler()  # type: ignore[return-value]


def format_status(state: PlayerState) -> str:
    """Return a concise status string for the current state."""

    inventory_str = ", ".join(f"{k}: {v}" for k, v in state.inventory.items())
    crafted_str = ", ".join(state.crafted) if state.crafted else "none"
    return (
        f"Day {state.day} | Health: {state.health} | Hunger: {state.hunger} | "
        f"Energy: {state.energy}\nInventory: {inventory_str}\nCrafted: {crafted_str}"
    )


def play() -> None:
    """Interactive command loop for the mini-game."""

    game = DontStarveGame()
    print("Welcome to the mini survival challenge! Type 'help' for actions.")
    while game.is_alive():
        print("\n" + format_status(game.state))
        command = input("> ").strip().lower()
        if command in {"quit", "exit"}:
            print("You head into the wilderness, game over.")
            return
        if command == "help":
            print("Actions: gather <resource>, eat <item>, rest, craft <item>, end_day")
            continue

        parts = command.split()
        action = parts[0] if parts else ""
        target = parts[1] if len(parts) > 1 else None
        print(game.step(action, item=target, resource=target))

    print("You have perished in the wilderness. Thanks for playing!")


if __name__ == "__main__":
    play()
