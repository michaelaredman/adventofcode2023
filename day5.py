from collections import OrderedDict
from bisect import bisect_left
import re

example = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


class S2D:

    def __init__(self, init: list[list[int]]):
        self.d = OrderedDict()
        # d[source] = (range, destination)
        init.sort(key=lambda i: i[1])
        for interval in init:
            self.d[interval[1]] = (interval[2], interval[0])
        self.keys = list(self.d.keys())

    def __call__(self, source):
        # if source in self.d:
        #     return self.d[source][1]
        # elif bisect_left(self.keys, source) != 0:
        #     key = self.keys[bisect_left(self.keys, source) - 1]
        #     if source < key + self.d[key][0]:
        #         return self.d[key][1] + source - key
        # return source
        possible = max(
            (key for key in self.d if key <= source), default=None)
        if possible != None:
            if source < possible + self.d[possible][0]:
                return self.d[possible][1] + source - possible
        return source


def find_intervals(s2r_string: str) -> list[list[int]]:
    intervals = []
    for interval in re.findall(r'\n(.+)', s2r_string):
        intervals.append([int(x) for x in interval.split()])
    return intervals


def find_smallest_location(file):
    with open(file, 'r') as f:
        string_input = f.read()
    split_s = re.split(r'\n\n', string_input)
    seeds = [int(x) for x in re.search(r': (.+)', split_s[0]).group(1).split()]
    seed_to_soil = S2D(find_intervals(split_s[1]))
    soil_to_fertilizer = S2D(find_intervals(split_s[2]))
    fertilizer_to_water = S2D(find_intervals(split_s[3]))
    water_to_light = S2D(find_intervals(split_s[4]))
    light_to_temperature = S2D(find_intervals(split_s[5]))
    temperature_to_humididty = S2D(find_intervals(split_s[6]))
    humididty_to_location = S2D(find_intervals(split_s[7]))
    locations = []
    for seed in seeds:
        locations.append(humididty_to_location(
            temperature_to_humididty(
                light_to_temperature(
                    water_to_light(
                        fertilizer_to_water(
                            soil_to_fertilizer(
                                seed_to_soil(seed))))))))
    print(sorted(locations))
    return min(locations)


print(find_smallest_location('inputs/day5'))


def find_smallest_location_range(file):
    with open(file, 'r') as f:
        string_input = f.read()
    split_s = re.split(r'\n\n', string_input)
    seed_ranges = [int(x) for x in re.search(
        r': (.+)', split_s[0]).group(1).split()]
    seeds = [s for s in range(seed_ranges[0], seed_ranges[0] + seed_ranges[1])] + \
        [s for s in range(seed_ranges[2], seed_ranges[2] + seed_ranges[3])]
    seed_to_soil = S2D(find_intervals(split_s[1]))
    soil_to_fertilizer = S2D(find_intervals(split_s[2]))
    fertilizer_to_water = S2D(find_intervals(split_s[3]))
    water_to_light = S2D(find_intervals(split_s[4]))
    light_to_temperature = S2D(find_intervals(split_s[5]))
    temperature_to_humididty = S2D(find_intervals(split_s[6]))
    humididty_to_location = S2D(find_intervals(split_s[7]))
    min_location = 99999999999999
    print(f"{seed_ranges[1]=}")
    i = 0
    for seed in range(seed_ranges[0], seed_ranges[0] + seed_ranges[1]):
        i += 1
        if i % 1000000 == 0:
            print("Reached:", seed)
        min_location = min(min_location,
                           humididty_to_location(
                               temperature_to_humididty(
                                   light_to_temperature(
                                       water_to_light(
                                           fertilizer_to_water(
                                               soil_to_fertilizer(
                                                   seed_to_soil(seed))))))))
    print("half way!")
    for seed in range(seed_ranges[2], seed_ranges[2] + seed_ranges[3]):
        min_location = min(min_location,
                           humididty_to_location(
                               temperature_to_humididty(
                                   light_to_temperature(
                                       water_to_light(
                                           fertilizer_to_water(
                                               soil_to_fertilizer(
                                                   seed_to_soil(seed))))))))
    return min_location


# print(find_smallest_location_range('inputs/day5'))
