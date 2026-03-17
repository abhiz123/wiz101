from engine import DamageSpell, DoTSpell, HealSpell, CharmSpell, WardSpell

def get_fire_deck():
    return [
        DamageSpell("Fire Cat", "Fire", 1, 120),
        DamageSpell("Sun Bird", "Fire", 3, 355),
        DamageSpell("Meteor Strike", "Fire", 4, 345),
        DamageSpell("Phoenix", "Fire", 5, 595),
        DoTSpell("Fire Dragon", "Fire", 7, initial_damage=540, dot_damage=47, dot_rounds=3),
        DoTSpell("Fire Elf", "Fire", 2, initial_damage=100, dot_damage=70, dot_rounds=3),
        DamageSpell("Krampus", "Fire", 2, 460, school_pip_cost=1),
        CharmSpell("Fire Blade", "Fire", 0, "Fire", "blade_flat", 30),        # +30 per pip
        CharmSpell("Elemental Blade", "Universal", 1, "Fire", "blade_fixed", 75),  # flat +75
        WardSpell("Fire Trap", "Fire", 0, "Fire", "trap_flat", 50),           # +50 per pip
        WardSpell("Tower Shield", "Ice", 2, "Universal", "shield", 350),      # -350 flat
        WardSpell("Tower Shield", "Ice", 2, "Universal", "shield", 350),
        HealSpell("Pixie", "Life", 2, 400),
        HealSpell("Satyr", "Life", 4, 800)
    ]

def get_death_deck():
    return [
        DamageSpell("Dark Sprite", "Death", 1, 110),
        DamageSpell("Banshee", "Death", 3, 300),
        DamageSpell("Vampire", "Death", 4, 340),
        DamageSpell("Wraith", "Death", 6, 500),
        DamageSpell("Scarecrow", "Death", 7, 590),
        DamageSpell("Skeletal Pirate", "Death", 5, 510),
        CharmSpell("Death Blade", "Death", 0, "Death", "blade_flat", 30),     # +30 per pip
        CharmSpell("Death Blade", "Death", 0, "Death", "blade_flat", 30),
        WardSpell("Death Trap", "Death", 0, "Death", "trap_flat", 50),        # +50 per pip
        WardSpell("Death Shield", "Death", 2, "Death", "shield", 300),        # -300 flat
        WardSpell("Tower Shield", "Ice", 2, "Universal", "shield", 350),      # -350 flat
        WardSpell("Feint", "Death", 1, "Universal", "trap_fixed", 300, self_value=100),  # +300 trap, +100 backlash
        HealSpell("Pixie", "Life", 2, 400)
    ]
