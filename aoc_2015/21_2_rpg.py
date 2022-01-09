import math


def get_items_from_data(my_file="21_items.txt"):
    weapons = dict()
    armors = dict()
    rings = dict()
    items = [weapons, armors, rings]
    with open(my_file) as f:
        for i in range(3):
            while True:
                line = f.readline()
                line = line.strip()
                if "0" in line:
                    line = line.split()
                    if i < 2:
                        items[i][line[0]] = list(map(int, line[-3:]))
                    else:
                        items[i][" ".join(line[:2])] = list(map(int, line[-3:]))
                if len(line) == 0:
                    break
    items[1]["None"] = [0, 0, 0]
    items[2]["None 1"] = [0, 0, 0]
    items[2]["None 2"] = [0, 0, 0]
    return items


class Player:
    def __init__(self, hit, damage, armor):
        self.hit = hit
        self.damage = damage
        self.armor = armor

    def survives(self, damage):
        damage_dealt = max(damage - self.armor, 1)
        return math.ceil(self.hit / damage_dealt)

    def worst_arrangement(self, boss):
        weapons, armors, rings = get_items_from_data()
        worst_cost = 0
        worst_choice = None
        for weapon_name, (w_cost, w_damage, w_armor) in weapons.items():
            for armor_name, (a_cost, a_damage, a_armor) in armors.items():
                for ring1_name, (r1_cost, r1_damage, r1_armor) in rings.items():
                    for ring2_name, (r2_cost, r2_damage, r2_armor) in rings.items():
                        if ring2_name == ring1_name:
                            continue
                        self.damage += w_damage + r1_damage + r2_damage
                        self.armor += a_armor + r1_armor + r2_armor
                        i_can_survive = self.survives(boss.damage)
                        boss_can_survive = boss.survives(self.damage)
                        if i_can_survive < boss_can_survive:
                            total_cost = w_cost + a_cost + r1_cost + r2_cost
                            if total_cost > worst_cost:
                                worst_cost = total_cost
                                worst_choice = (weapon_name, armor_name, ring1_name, ring2_name)
                        self.damage -= (w_damage + r1_damage + r2_damage)
                        self.armor -= (a_armor + r1_armor + r2_armor)
        return worst_cost, worst_choice


def main():
    me = Player(100, 0, 0)
    boss = Player(109, 8, 2)
    print(me.worst_arrangement(boss))


if __name__ == "__main__":
    main()
