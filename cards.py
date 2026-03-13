from engine import DamageSpell, DoTSpell, HealSpell, CharmSpell, WardSpell

def get_fire_deck():
    return [
        DamageSpell("Fire Cat", "Fire", 1, 100, accuracy=75),
        DamageSpell("Sun Bird", "Fire", 3, 300, accuracy=75),
        DamageSpell("Meteor Strike", "Fire", 4, 325, accuracy=75), # AoE simplified to ST for 1v1
        DamageSpell("Phoenix", "Fire", 5, 550, accuracy=75),
        DamageSpell("Fire Dragon", "Fire", 7, 440, accuracy=75), # Initial hit only for now
        DoTSpell("Fire Elf", "Fire", 2, initial_damage=50, dot_damage=70, dot_rounds=3, accuracy=75),
        DoTSpell("Krampus", "Fire", 4, initial_damage=100, dot_damage=100, dot_rounds=2, accuracy=75),
        CharmSpell("Fire Blade", "Fire", 0, "Fire", "blade_mult", 1.35),
        CharmSpell("Elemental Blade", "Universal", 1, "Fire", "blade_mult", 1.35),
        WardSpell("Fire Trap", "Fire", 0, "Fire", "trap_mult", 1.25),
        WardSpell("Tower Shield", "Ice", 0, "Universal", "shield", 0.50),
        WardSpell("Tower Shield", "Ice", 0, "Universal", "shield", 0.50),
        HealSpell("Pixie", "Life", 2, 400),
        HealSpell("Satyr", "Life", 4, 860)
    ]

def get_death_deck():
    return [
        DamageSpell("Dark Sprite", "Death", 1, 95, accuracy=85),
        DamageSpell("Banshee", "Death", 3, 300, accuracy=85),
        DamageSpell("Vampire", "Death", 4, 350, accuracy=85), # Drain mechanic simplified to damage
        DamageSpell("Wraith", "Death", 6, 500, accuracy=85),
        DamageSpell("Scarecrow", "Death", 7, 400, accuracy=85),
        DamageSpell("Skeletal Pirate", "Death", 5, 430, accuracy=85),
        CharmSpell("Death Blade", "Death", 0, "Death", "blade_flat", 30), # Flat +30 per pip
        CharmSpell("Death Blade", "Death", 0, "Death", "blade_flat", 30),
        WardSpell("Death Trap", "Death", 0, "Death", "trap_flat", 50), # Flat +50 per pip
        WardSpell("Death Shield", "Death", 0, "Death", "shield", 0.20), # 80% shield
        WardSpell("Tower Shield", "Ice", 0, "Universal", "shield", 0.50),
        WardSpell("Feint", "Death", 1, "Universal", "trap_mult", 1.70), # 70% trap
        HealSpell("Pixie", "Life", 2, 400)
    ]
