def w_list_value(w_list):
    spells = {"M": [53, 1, 4, 0, 0, 0, "M"],  # (Magic Missile) happens once
              "D": [73, 1, 2, 0, 2, 0, "D"],  # (Drain) happens once
              "S": [113, 6, 0, 7, 0, 0, "S"],  # (Shield) added at start, subtracted at end
              "P": [173, 6, 3, 0, 0, 0, "P"],  # (Poison) happens every turn
              "R": [229, 5, 0, 0, 0, 101, "R"]}  # (Recharge) happens every turn
    total = 0
    for name in w_list:
        cost = spells.get(name)[0]
        total += cost
    return total


def simulation(my_hit, my_armor, my_mana, boss_hit, boss_damage, mana_spent, my_turn,
               free_spells, active_spells, w_list, part):
    # print(my_hit, my_armor, my_mana, boss_hit, boss_damage, mana_spent, my_turn, free_spells, active_spells)

    # returns 0 (meaning unsuccessful path) or mana_spent
    #
    # my_hit, boss_hit - respective hp
    # my_armor, my_mana - current values
    # boss_damage - how much he hurts me
    # mana_spent - found so far
    # my_turn (bool) - mine or boss's
    # free_spells - list of names of spells that are free to use
    # active spells - list of lists like keys in 'spells' dictionary (copies of these with changes)
    #
    global min_mana
    if mana_spent > min_mana:
        return 0
    # spells is a dictionary:
    # {name: [0=cost, 1=turns_on, 2=damage_value, 3=armor_value, 4=hit_value, 5=extra_mana, 6=initial)]}
    spells = {"M":  [53,  1, 4, 0, 0, 0, "M"],      # (Magic Missile) happens once
              "D":  [73,  1, 2, 0, 2, 0, "D"],      # (Drain) happens once
              "S":  [113, 6, 0, 7, 0, 0, "S"],      # (Shield) added at start, subtracted at end
              "P":  [173, 6, 3, 0, 0, 0, "P"],      # (Poison) happens every turn
              "R":  [229, 5, 0, 0, 0, 101, "R"]}    # (Recharge) happens every turn

    # firstly, use active spells
    new_active_spells = list()
    while True:
        if len(active_spells) == 0:
            active_spells = new_active_spells
            break
        spell = active_spells[0].copy()
        active_spells.remove(spell)
        boss_hit -= spell[2]
        if boss_hit <= 0:
            if mana_spent < min_mana:
                min_mana = mana_spent
                print(min_mana)
                return min_mana
        my_armor += spell[3]
        my_hit += spell[4]
        my_mana += spell[5]
        spell[1] -= 1
        if spell[6] == "S":
            spell[3] = 0
        if spell[1] > 0:
            new_active_spells.append(spell)
        else:
            if spell[6] == "S":
                my_armor -= 7
            free_spells.append(spell[6])
    if my_turn:
        if part == 2:
            my_hit -= 1
        my_turn = not my_turn
        # now go through all possible free spells
        for spell_name in free_spells:
            spell = spells.get(spell_name)  # .copy()
            if my_mana >= spell[0]:
                temp_free_spells = free_spells.copy()
                temp_free_spells.remove(spell_name)
                new_mana_spent = simulation(my_hit, my_armor, my_mana - spell[0], boss_hit,
                                            boss_damage, mana_spent + spell[0], my_turn, temp_free_spells,
                                            active_spells + [spell], w_list + [spell_name], part)
                if 0 < new_mana_spent < min_mana:
                    min_mana = new_mana_spent
                    print(min_mana, w_list, w_list_value(w_list))
                    return min_mana
    else:
        my_turn = not my_turn
        my_hit -= max(boss_damage - my_armor, 1)
        if my_hit <= 0:
            return 0
        else:
            new_mana_spent = simulation(my_hit, my_armor, my_mana, boss_hit,
                                        boss_damage, mana_spent, my_turn, free_spells, active_spells, w_list, part)
            if 0 < new_mana_spent < min_mana:
                min_mana = new_mana_spent
                print(min_mana)
                return min_mana
    return 0


def main():
    global min_mana
    for part in [1, 2]:
        min_mana = 1000000
        print("part", part)
        simulation(50, 0, 500, 71, 10, 0, True, ["M", "D", "S", "P", "R"], [], [], part)


if __name__ == "__main__":
    min_mana = 10000000
    winning_sequence = list()
    main()
