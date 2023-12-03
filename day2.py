import re

example = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


def game_to_draws(game_str: str) -> list[tuple]:
    draw_values = []
    all_games = re.search(r": (.*)", game_str).group(1)
    game_list = re.split(r"; ", all_games)
    for game in game_list:
        rgb = [0, 0, 0]
        draws = re.split(r", ", game)
        for draw in draws:
            if r := re.search(r"(\d*) red", draw):
                rgb[0] = int(r.group(1))
            elif g := re.search(r"(\d*) green", draw):
                rgb[1] = int(g.group(1))
            elif b := re.search(r"(\d*) blue", draw):
                rgb[2] = int(b.group(1))
        draw_values.append(tuple(rgb))
    return draw_values


def valid_game(dice: tuple, draws: list[tuple]) -> bool:
    return all(all(draw_col <= dice_col for draw_col, dice_col in zip(draw, dice))
               for draw in draws)


# for game in example.splitlines():
#     print(re.search(r"([^:]+):", game).group(1))
#     print(game_to_draws(game))
#     print(valid_game((12, 13, 14), game_to_draws(game)))
#     print(re.search(r"Game (\d*):", game).group(1))


with open('inputs/day2', 'r') as f:
    sum_valid_games = 0
    for game in f:
        if valid_game((12, 13, 14), game_to_draws(game)):
            sum_valid_games += int(re.search(r"Game (\d*):", game).group(1))
    print(sum_valid_games)


def game_power(game: list[tuple]) -> int:
    power = 1
    dice = [0, 0, 0]
    for draw in game_to_draws(game):
        dice[0] = max(dice[0], draw[0])
        dice[1] = max(dice[1], draw[1])
        dice[2] = max(dice[2], draw[2])
    return dice[0]*dice[1]*dice[2]


with open('inputs/day2', 'r') as f:
    power_sum = 0
    for game in f:
        power_sum += game_power(game)
    print(power_sum)
