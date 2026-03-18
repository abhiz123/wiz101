import random
from engine import (DamageSpell, DoTSpell, HealSpell, CharmSpell, WardSpell,
                    ReshuffleSpell, DrainSpell, UtilitySpell, WildBoltSpell,
                    DamageHoTSpell, DamageWithTrapSpell, SacrificeDamageSpell,
                    ClearBladeSpell, ClearShieldSpell, DamageStealBladeSpell,
                    EnchantSpell, AuraSpell, StunSpell, CleanseTrapSpell,
                    DisarmSpell, DonatePowerSpell, StealPipSpell)

ELEMENTAL_SCHOOLS = {'Fire', 'Ice', 'Storm'}


def get_universal_cards(school):
    cards = []
    if school in ELEMENTAL_SCHOOLS:
        cards += [CharmSpell("Elemental Blade", "Universal", 1, "Elemental", "blade_fixed", 75)] * 2
        cards += [WardSpell("Elemental Trap", "Universal", 1, "Elemental", "trap_fixed", 100)] * 2
    else:
        cards += [CharmSpell("Spirit Blade", "Universal", 1, "Spirit", "blade_fixed", 75)] * 2
        cards += [WardSpell("Spirit Trap", "Universal", 1, "Spirit", "trap_fixed", 100)] * 2
    cards += [WardSpell("Feint", "Death", 1, "Universal", "trap_fixed", 300, self_value=100)] * 3
    cards += [ReshuffleSpell("Reshuffle", "Universal", 4)] * 2
    cards += [HealSpell("Pixie", "Life", 2, 400)] * 2
    cards += [EnchantSpell("Colossal", "Universal", 0, "damage", "base_damage", 200) for _ in range(2)]
    cards += [EnchantSpell("Epic", "Universal", 0, "damage", "base_damage", 250) for _ in range(2)]
    cards += [EnchantSpell("Potent Trap", "Universal", 0, "trap", "value", 20) for _ in range(2)]
    cards += [EnchantSpell("Potent Blade", "Universal", 0, "blade", "value", 20) for _ in range(2)]
    return cards


def get_fire_deck():
    cards = [
        *[WardSpell("Fire Trap", "Fire", 0, "Fire", "trap_flat", 50)] * 5,
        *[CharmSpell("Fire Blade", "Fire", 0, "Fire", "blade_flat", 30)] * 3,
        *[DamageSpell("Fire Cat", "Fire", 1, 120)] * 2,
        *[DamageSpell("Sun Bird", "Fire", 3, 355)] * 2,
        *[DamageSpell("Meteor Strike", "Fire", 4, 345)] * 2,
        *[DamageSpell("Phoenix", "Fire", 5, 595)] * 2,
        *[DoTSpell("Fire Dragon", "Fire", 7, 540, 47, 3)] * 2,
        *[ClearShieldSpell("Meltdown", "Fire", 2, 2, 12, 3, school_pip_cost=1)] * 2,
        *[DoTSpell("Fire Elf", "Fire", 2, 100, 70, 3)] * 2,
        *[SacrificeDamageSpell("Immolate", "Fire", 4, 600, 200)] * 2,
        DamageSpell("Krampus", "Fire", 2, 460, school_pip_cost=1),
        DamageStealBladeSpell("Nautilus Unleashed", "Fire", 3, 505, school_pip_cost=1),
        DamageWithTrapSpell("Brimstone Revenant", "Fire", 2, 470, "Fire", 100, school_pip_cost=1),
    ]
    cards += get_universal_cards('Fire')
    random.shuffle(cards)
    return cards


def get_death_deck():
    cards = [
        *[WardSpell("Death Trap", "Death", 0, "Death", "trap_flat", 50)] * 3,
        WardSpell("Tower Shield", "Ice", 2, "Universal", "shield", 350),
        *[CharmSpell("Death Blade", "Death", 0, "Death", "blade_flat", 30)] * 4,
        *[DamageSpell("Dark Sprite", "Death", 1, 110)] * 2,
        *[DamageSpell("Banshee", "Death", 3, 300)] * 2,
        *[DrainSpell("Vampire", "Death", 4, 340)] * 2,
        *[DamageSpell("Wraith", "Death", 6, 500)] * 2,
        *[DrainSpell("Scarecrow", "Death", 7, 590)] * 2,
        *[DamageSpell("Skeletal Pirate", "Death", 5, 510)] * 2,
        *[DrainSpell("Ghoul", "Death", 2, 160)] * 2,
        *[UtilitySpell("Empower", "Death", 0, "add_pips", 3, self_damage=250)] * 2,
        DamageSpell("Kii Yaaa", "Death", 2, 300, school_pip_cost=1, image="Kii Yaaa.png"),
        DrainSpell("Ship of Fools", "Death", 4, 300, image="Ship Of Fools.png"),
        DoTSpell("Deer Knight", "Death", 3, 300, 30, 3, school_pip_cost=1, image="DeerKnight.png"),
    ]
    cards += get_universal_cards('Death')
    random.shuffle(cards)
    return cards


def get_ice_deck():
    cards = [
        *[WardSpell("Ice Trap", "Ice", 0, "Ice", "trap_flat", 50)] * 3,
        *[WardSpell("Tower Shield", "Ice", 2, "Universal", "shield", 350)] * 4,
        *[CharmSpell("Ice Blade", "Ice", 0, "Ice", "blade_flat", 30)] * 2,
        *[DamageSpell("Frost Beetle", "Ice", 1, 100, image="Frost Beetle.png")] * 2,
        *[DamageSpell("Snow Serpent", "Ice", 2, 180, image="Snow Serpent.png")] * 2,
        *[DamageSpell("Blzzard", "Ice", 4, 300, image="Blzzard.png")] * 2,
        *[DamageSpell("Colossus", "Ice", 6, 500)] * 2,
        *[ClearBladeSpell("Wall of Blades", "Ice", 2, 2, 100, image="Wall of Blades.png")] * 2,
        *[DamageSpell("Snowball Barrage", "Ice", 2, 160, image="Snowball Barrage.png")] * 2,
        *[DamageSpell("Freeze Ray", "Ice", 6, 300, image="Freeze Ray.png")] * 2,
        WardSpell("Deermouse Trap", "Ice", 3, "Universal", "trap_fixed", 300, image="Deermouse Trap.png"),
        DamageSpell("Winter Moon", "Ice", 4, 500, image="Winter Moon.png"),
        DamageSpell("Handsome Fimori", "Ice", 3, 500, image="Handsome Fimori.png"),
    ]
    cards += get_universal_cards('Ice')
    random.shuffle(cards)
    return cards


def get_life_deck():
    cards = [
        *[WardSpell("Life Trap", "Life", 0, "Life", "trap_flat", 50, image="Life Trap.png")] * 2,
        *[CharmSpell("Life Blade", "Life", 0, "Life", "blade_flat", 30, image="Life Blade.png")] * 5,
        *[DamageSpell("Imp", "Life", 1, 120)] * 2,
        *[DamageSpell("Leprechaun", "Life", 2, 200)] * 2,
        *[WardSpell("Spirit Armor", "Life", 3, "Universal", "shield", 400, image="Spirit Armor.png")] * 2,
        *[DamageHoTSpell("Seraph", "Life", 4, 350, 17, 3)] * 2,
        *[HealSpell("Satyr", "Life", 4, 800)] * 2,
        *[DamageSpell("Centaur", "Life", 6, 600)] * 2,
        *[DamageSpell("Forest Lord", "Life", 7, 700, image="Forest Lord.png")] * 2,
        *[DamageSpell("Natures Wrath", "Life", 3, 250, image="Naures Wrath.png")] * 2,
        HealSpell("Pigsie", "Life", 2, 750, image="Pigsie.png"),
        DamageSpell("Ratatoskrs Spin", "Life", 2, 400, image="Ratatoskrs spin.png"),
        DamageSpell("Camp Bandit", "Life", 3, 300, image="Camp Bandit.png"),
    ]
    cards += get_universal_cards('Life')
    random.shuffle(cards)
    return cards


def get_myth_deck():
    cards = [
        *[WardSpell("Myth Trap", "Myth", 0, "Myth", "trap_flat", 50, image="Myth Trap.png")] * 3,
        *[WardSpell("Tower Shield", "Ice", 2, "Universal", "shield", 350)] * 3,
        *[CharmSpell("Myth Blade", "Myth", 0, "Myth", "blade_flat", 30, image="Myth Blade.png")] * 2,
        *[DamageSpell("Blood Bat", "Myth", 1, 110, image="Blood Bat.png")] * 2,
        *[DamageSpell("Troll", "Myth", 2, 210)] * 2,
        *[DamageSpell("Minotaur", "Myth", 5, 445)] * 2,
        *[DamageSpell("Earthquake", "Myth", 6, 370)] * 2,
        *[DamageSpell("Orthrus", "Myth", 7, 785)] * 2,
        *[DamageSpell("Humungofrog", "Myth", 4, 315, image="Humungofrog.png")] * 2,
        *[UtilitySpell("Draw Power", "Myth", 1, "add_pips", 2, image="Draw Power.png")] * 2,
        DamageSpell("Athena Battle Sight", "Myth", 3, 520, image="Athena Battle Sight.png"),
        DamageSpell("Keeper of Flame", "Myth", 2, 400, image="Keeper of flame.png"),
        DamageSpell("Ninja Pigs", "Myth", 4, 685, image="Ninja Pigs.png"),
    ]
    cards += get_universal_cards('Myth')
    random.shuffle(cards)
    return cards


def get_storm_deck():
    cards = [
        *[WardSpell("Storm Trap", "Storm", 0, "Storm", "trap_flat", 50, image="Storm Trap.png")] * 3,
        *[CharmSpell("Storm Blade", "Storm", 0, "Storm", "blade_flat", 30, image="Storm Blade.png")] * 4,
        *[DamageSpell("Thunder Snake", "Storm", 1, 130, image="Thunder Snake.png")] * 2,
        *[DamageSpell("Lightening Bats", "Storm", 2, 270, image="Lightening Bats.png")] * 2,
        *[DamageSpell("Onis Attrition", "Storm", 2, 100, image="Onis Attrition.png")] * 2,
        *[DamageSpell("Kraken", "Storm", 4, 550)] * 2,
        *[HealSpell("Jinns Restoration", "Storm", 3, 300, image="Jinns Restoration.png")] * 2,
        *[WildBoltSpell("Wild Bolt", "Storm", 2)] * 2,
        *[DamageSpell("Tempest", "Storm", 5, 600, image="Tempest.png")] * 2,
        *[DamageSpell("Storm Lord", "Storm", 7, 690, image="Storm Lord.png")] * 2,
        DamageSpell("Catalan", "Storm", 3, 650, image="Catalan.png"),
        DamageSpell("Queen Calypso", "Storm", 2, 470, image="Queen Calypso.png"),
        DamageSpell("Catch of the Day", "Storm", 4, 550, image="Catch of the day.png"),
    ]
    cards += get_universal_cards('Storm')
    random.shuffle(cards)
    return cards


def get_center_deck():
    cards = []
    cards += [CharmSpell("Balance Blade", "Universal", 0, "Universal", "blade_flat", 20, image="Central/Balance Blade.png") for _ in range(2)]
    cards += [AuraSpell("Berserk", "Universal", 0, "combat", outgoing_bonus=300, incoming_bonus=400, rounds=3, image="Central/Berserk.png") for _ in range(2)]
    cards += [CleanseTrapSpell("Cleanse Ward", "Universal", 0, image="Central/Cleanse Ward.png") for _ in range(2)]
    cards += [DisarmSpell("Disarm", "Universal", 1, image="Central/Disarm.png") for _ in range(2)]
    cards += [DonatePowerSpell("Donate Power", "Universal", 1, image="Central/Donate Power.png") for _ in range(2)]
    cards += [AuraSpell("Empowerment", "Universal", 0, "empowerment", pip_threshold=4, rounds=4, image="Central/Empowerment.png") for _ in range(2)]
    cards += [AuraSpell("Frenzy", "Universal", 0, "combat", outgoing_bonus=400, incoming_bonus=300, rounds=3, image="Central/Frenzy.png") for _ in range(2)]
    cards += [WardSpell("Hex", "Universal", 0, "Universal", "trap_flat", 30, image="Central/Hex.png") for _ in range(2)]
    cards += [StealPipSpell("Steal Pip", "Universal", 0, image="Central/Steal Pip.png") for _ in range(2)]
    cards += [StunSpell("Stun", "Universal", 0, image="Central/Stun.png") for _ in range(2)]
    cards += [WardSpell("Tower Shield", "Ice", 2, "Universal", "shield", 350, image="Central/Tower Shield.png") for _ in range(2)]
    cards += [HealSpell("Unicorn", "Life", 3, 400, image="Central/Unicorn.png") for _ in range(2)]
    random.shuffle(cards)
    return cards
