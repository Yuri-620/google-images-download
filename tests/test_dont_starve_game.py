from google_images_download.dont_starve import DontStarveGame, format_status


def test_gather_and_inventory_updates():
    game = DontStarveGame()
    response = game.gather("wood")
    assert "gathered" in response
    assert game.state.inventory["wood"] == 1
    assert game.state.energy < 100
    assert game.state.hunger < 50


def test_eating_restores_hunger_and_health():
    game = DontStarveGame()
    game.state.inventory["berries"] = 2
    game.state.hunger = 20
    game.state.health = 80

    response = game.eat("berries")
    assert "berries" in response
    assert game.state.inventory["berries"] == 1
    assert game.state.hunger > 20
    assert game.state.health > 80


def test_rest_recovers_energy():
    game = DontStarveGame()
    game.state.energy = 40
    response = game.rest()
    assert "rest" in response
    assert game.state.energy > 40


def test_crafting_campfire_consumes_wood():
    game = DontStarveGame()
    game.state.inventory["wood"] = 3
    response = game.craft("campfire")
    assert "campfire" in response
    assert game.state.inventory["wood"] == 1
    assert "campfire" in game.state.crafted


def test_format_status_contains_core_stats():
    game = DontStarveGame()
    status = format_status(game.state)
    assert "Day" in status
    assert "Health" in status
    assert "Inventory" in status
