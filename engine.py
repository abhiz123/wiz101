import random
import uuid

class PipBag:
    def __init__(self, num_players=2):
        self.pips = []
        if num_players == 2:
            self.pips = ['Normal'] * 7 + ['Power'] * 10 + ['School'] * 4 + ['Shadow'] * 4 + ['Fizzle'] * 3 + ['Critical'] * 2
        else:
            self.pips = ['Normal'] * 13 + ['Power'] * 20 + ['School'] * 8 + ['Shadow'] * 8 + ['Fizzle'] * 7 + ['Critical'] * 4
        random.shuffle(self.pips)

    def draw(self):
        if not self.pips:
            return None
        return self.pips.pop()

    def return_pip(self, pip):
        self.pips.append(pip)
        random.shuffle(self.pips)

    def count(self):
        return len(self.pips)


class Card:
    def __init__(self, name, school, cost, accuracy=100):
        self.id = str(uuid.uuid4())
        self.name = name
        self.school = school
        self.cost = cost
        self.accuracy = accuracy
        self.type = 'normal'

    def cast(self, caster, target, pips_spent, game):
        pass

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'school': self.school,
            'cost': self.cost,
            'accuracy': self.accuracy,
            'type': self.type,
            'image': self.name + '.png'
        }

    def __str__(self):
        return f"{self.name} ({self.school}, Cost: {self.cost})"

class DamageSpell(Card):
    def __init__(self, name, school, cost, base_damage, accuracy=100):
        super().__init__(name, school, cost, accuracy)
        self.base_damage = base_damage
        self.type = 'damage'

    def to_dict(self):
        d = super().to_dict()
        d['base_damage'] = self.base_damage
        return d

    def cast(self, caster, target, pips_spent, game):
        game.log(f"{caster.name} casts {self.name} on {target.name}!")
        damage = self.base_damage

        is_critical = random.randint(1, 20) in [20, caster.lucky_number]
        if is_critical:
            damage *= 2
            game.log(f"CRITICAL HIT! Base damage doubled to {damage}.")

        charms_to_consume = []
        for charm in caster.charms:
            if charm['school'] in [self.school, 'Universal', 'Elemental', 'Spirit']:
                if charm['type'] in ['blade_flat', 'blade_fixed']:
                    damage += charm['value']
                    charms_to_consume.append(charm)
                    game.log(f"Blade triggered: +{charm['value']} -> Damage: {damage}")
                elif charm['type'] == 'weakness':
                    damage = int(damage * charm['value'])
                    charms_to_consume.append(charm)
                    game.log(f"Weakness triggered: x{charm['value']} -> Damage: {damage}")

        for c in charms_to_consume:
            caster.charms.remove(c)

        wards_to_consume = []
        for ward in target.wards:
           if ward['school'] in [self.school, 'Universal', 'Elemental', 'Spirit']:
               if ward['type'] in ['trap_flat', 'trap_fixed']:
                   damage += ward['value']
                   wards_to_consume.append(ward)
                   game.log(f"Trap triggered: +{ward['value']} -> Damage: {damage}")
               elif ward['type'] == 'shield':
                   damage = max(0, damage - ward['value'])
                   wards_to_consume.append(ward)
                   game.log(f"Shield blocked {ward['value']} -> Damage: {damage}")

        for w in wards_to_consume:
            target.wards.remove(w)

        game.log(f"{self.name} hits {target.name} for {damage} final damage.")
        target.take_damage(damage, game)

class DoTSpell(DamageSpell):
    def __init__(self, name, school, cost, initial_damage, dot_damage, dot_rounds, accuracy=100):
        super().__init__(name, school, cost, initial_damage, accuracy)
        self.dot_damage = dot_damage
        self.dot_rounds = dot_rounds
        self.type = 'dot'

    def to_dict(self):
        d = super().to_dict()
        d['dot_damage'] = self.dot_damage
        d['dot_rounds'] = self.dot_rounds
        return d

    def cast(self, caster, target, pips_spent, game):
        game.log(f"{caster.name} casts {self.name} DoT down on {target.name}!")
        damage = self.base_damage
        is_critical = random.randint(1, 20) in [20, caster.lucky_number]
        if is_critical:
            damage *= 2

        dot_bonus_flat = 0

        charms_to_consume = []
        for charm in caster.charms:
            if charm['school'] in [self.school, 'Universal', 'Elemental', 'Spirit']:
                 if charm['type'] in ['blade_flat', 'blade_fixed']:
                    damage += charm['value']
                    dot_bonus_flat += charm['value']
                    charms_to_consume.append(charm)
                 elif charm['type'] == 'weakness':
                    damage = int(damage * charm['value'])
                    charms_to_consume.append(charm)

        for c in charms_to_consume:
             caster.charms.remove(c)

        wards_to_consume = []
        for ward in target.wards:
           if ward['school'] in [self.school, 'Universal', 'Elemental', 'Spirit']:
               if ward['type'] in ['trap_flat', 'trap_fixed']:
                   damage += ward['value']
                   dot_bonus_flat += ward['value']
                   wards_to_consume.append(ward)
               elif ward['type'] == 'shield':
                   damage = max(0, damage - ward['value'])
                   wards_to_consume.append(ward)

        for w in wards_to_consume:
            target.wards.remove(w)

        game.log(f"{self.name} initial hit deals {damage} damage.")
        if damage > 0:
            target.take_damage(damage, game)

        final_dot_damage_per_tick = self.dot_damage + dot_bonus_flat
        target.dots.append({
            'name': self.name,
            'damage': final_dot_damage_per_tick,
            'rounds_left': self.dot_rounds
        })
        game.log(f"{self.name} will deal {final_dot_damage_per_tick} damage for {self.dot_rounds} rounds.")


class HealSpell(Card):
    def __init__(self, name, school, cost, heal_amount, accuracy=100):
        super().__init__(name, school, cost, accuracy)
        self.heal_amount = heal_amount
        self.type = 'heal'

    def to_dict(self):
        d = super().to_dict()
        d['heal_amount'] = self.heal_amount
        return d

    def cast(self, caster, target, pips_spent, game):
        heal = self.heal_amount
        is_critical = random.randint(1, 20) in [20, caster.lucky_number]
        if is_critical:
            heal *= 2
            game.log(f"CRITICAL HEAL! Double healing: {heal}")
        target.heal(heal, game)

class CharmSpell(Card):
    def __init__(self, name, school, cost, target_school, charm_type, value, accuracy=100):
        super().__init__(name, school, cost, accuracy)
        self.target_school = target_school
        self.charm_type = charm_type
        self.value = value
        self.type = 'charm'

    def to_dict(self):
        d = super().to_dict()
        d['target_school'] = self.target_school
        d['charm_type'] = self.charm_type
        d['value'] = self.value
        return d

    def cast(self, caster, target, pips_spent, game):
        if self.charm_type == 'blade_flat':
            # Per-pip blades: consume ALL pips, pre-compute bonus
            pip_count = pips_spent + len(caster.pips)
            computed_value = self.value * pip_count
            for p in list(caster.pips):
                game.bag.return_pip('School' if p == caster.school else p)
            caster.pips.clear()
            target.charms.append({
                'name': self.name,
                'school': self.target_school,
                'type': 'blade_flat',
                'value': computed_value
            })
            game.log(f"{caster.name} cast {self.name}: consumed {pip_count} pips -> +{computed_value} bonus stored.")
        elif self.charm_type == 'blade_fixed':
            # Fixed blades: no pip consumption, flat bonus
            target.charms.append({
                'name': self.name,
                'school': self.target_school,
                'type': 'blade_fixed',
                'value': self.value
            })
            game.log(f"{caster.name} cast {self.name}: +{self.value} bonus stored.")
        else:
            # weakness and other charms: no pip consumption
            target.charms.append({
                'name': self.name,
                'school': self.target_school,
                'type': self.charm_type,
                'value': self.value
            })
            game.log(f"{caster.name} cast {self.name} on {target.name}.")

class WardSpell(Card):
    def __init__(self, name, school, cost, target_school, ward_type, value, accuracy=100, self_value=None):
        super().__init__(name, school, cost, accuracy)
        self.target_school = target_school
        self.ward_type = ward_type
        self.value = value
        self.self_value = self_value
        self.type = 'ward'

    def to_dict(self):
        d = super().to_dict()
        d['target_school'] = self.target_school
        d['ward_type'] = self.ward_type
        d['value'] = self.value
        return d

    def cast(self, caster, target, pips_spent, game):
        if self.ward_type == 'trap_flat':
            # Per-pip traps: consume ALL pips, pre-compute bonus
            pip_count = pips_spent + len(caster.pips)
            computed_value = self.value * pip_count
            for p in list(caster.pips):
                game.bag.return_pip('School' if p == caster.school else p)
            caster.pips.clear()
            target.wards.append({
                'name': self.name,
                'school': self.target_school,
                'type': 'trap_flat',
                'value': computed_value
            })
            game.log(f"{caster.name} cast {self.name}: consumed {pip_count} pips -> +{computed_value} trap on {target.name}.")
        elif self.ward_type == 'trap_fixed':
            # Fixed traps: no pip consumption
            target.wards.append({
                'name': self.name,
                'school': self.target_school,
                'type': 'trap_fixed',
                'value': self.value
            })
            game.log(f"{caster.name} cast {self.name}: +{self.value} trap on {target.name}.")
            # Feint backlash: also place a trap on the caster
            if self.self_value is not None:
                caster.wards.append({
                    'name': f"{self.name} (backlash)",
                    'school': 'Universal',
                    'type': 'trap_fixed',
                    'value': self.self_value
                })
                game.log(f"Backlash: +{self.self_value} trap on {caster.name}.")
        else:
            # shield and other wards
            target.wards.append({
                'name': self.name,
                'school': self.target_school,
                'type': self.ward_type,
                'value': self.value
            })
            game.log(f"{caster.name} cast {self.name} on {target.name}.")

class Player:
    def __init__(self, name, school, max_health):
        self.name = name
        self.school = school
        self.max_health = max_health
        self.health = max_health
        self.pips = []
        self.deck = []
        self.hand = []
        self.discard = []
        self.charms = []
        self.wards = []
        self.dots = []
        self.lucky_number = random.randint(1, 19)
        self.is_dead = False
        self.has_drawn_pip_this_turn = False
        self.has_cast_this_turn = False

    def draw_card(self, amount=1):
        for _ in range(amount):
            if len(self.hand) >= 7:
                break
            if not self.deck:
                if not self.discard:
                    break
                self.deck = self.discard
                self.discard = []
                random.shuffle(self.deck)
            card = self.deck.pop(0)
            self.hand.append(card)

    def draw_pip(self, bag):
        if len(self.pips) < 10:
            p = bag.draw()
            if p:
                # Convert generic School pip to this player's school
                if p == 'School':
                    p = self.school
                self.pips.append(p)
                return p
        return None

    def take_damage(self, amount, game):
        self.health = max(0, self.health - amount)
        game.log(f"{self.name} takes {amount} damage! (Health: {self.health}/{self.max_health})")
        if self.health == 0:
            self.is_dead = True

    def heal(self, amount, game):
        if self.health > 0:
            self.health = min(self.max_health, self.health + amount)
            game.log(f"{self.name} heals for {amount}. (Health: {self.health}/{self.max_health})")

    def process_dots(self, game):
        remaining_dots = []
        for dot in self.dots:
            game.log(f"{self.name} takes {dot['damage']} DoT from {dot['name']}.")
            self.take_damage(dot['damage'], game)
            dot['rounds_left'] -= 1
            if dot['rounds_left'] > 0:
                remaining_dots.append(dot)
        self.dots = remaining_dots

    def can_cast(self, card):
        cost_remaining = card.cost
        if card.school == 'Shadow':
            return self.pips.count('Shadow') >= card.cost

        power_pips = self.pips.count('Power')
        school_pips = self.pips.count(self.school)
        normal_pips = self.pips.count('Normal')
        power_value_pips = power_pips + school_pips

        if self.school == card.school:
            return power_value_pips * 2 + normal_pips >= cost_remaining
        else:
            return school_pips * 2 + power_pips + normal_pips >= cost_remaining

    def spend_pips(self, card, bag):
        cost_remaining = card.cost
        pips_spent = 0
        pips_to_remove = []

        if card.school == 'Shadow':
             for p in self.pips:
                 if p == 'Shadow' and cost_remaining > 0:
                     pips_to_remove.append(p)
                     cost_remaining -= 1
                     pips_spent += 1
        else:
            for p in sorted(self.pips, key=lambda x: 1 if x == 'Normal' else 0):
                if cost_remaining <= 0: break
                if p == 'Power' and self.school == card.school:
                    cost_val = min(2, cost_remaining)
                    cost_remaining -= cost_val
                    pips_to_remove.append(p)
                    pips_spent += 1
                elif p == self.school:
                    cost_val = min(2, cost_remaining)
                    cost_remaining -= cost_val
                    pips_to_remove.append(p)
                    pips_spent += 1
                elif p == 'Normal' or p == 'Power':
                    cost_remaining -= 1
                    pips_to_remove.append(p)
                    pips_spent += 1

        for p in pips_to_remove:
            self.pips.remove(p)
            bag.return_pip('School' if p == self.school else p)
        return pips_spent

    def to_dict(self):
        return {
            'name': self.name,
            'school': self.school,
            'health': self.health,
            'max_health': self.max_health,
            'pips': self.pips,
            'hand': [c.to_dict() for c in self.hand],
            'deck_count': len(self.deck),
            'discard_count': len(self.discard),
            'charms': self.charms,
            'wards': self.wards,
            'dots': self.dots,
            'is_dead': self.is_dead,
            'has_drawn_pip': self.has_drawn_pip_this_turn,
            'has_cast': self.has_cast_this_turn
        }

class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.bag = PipBag(num_players=2)
        self.round = 1
        self.turn = self.p1.name
        self.logs = []
        # Setup hands
        self.p1.draw_card(7)
        self.p2.draw_card(7)

    def log(self, msg):
        self.logs.append(msg)
        print(msg)

    def active_player(self):
        return self.p1 if self.turn == self.p1.name else self.p2

    def inactive_player(self):
        return self.p2 if self.turn == self.p1.name else self.p1

    def draw_pip(self):
        if self.p1.is_dead or self.p2.is_dead:
            return False
        player = self.active_player()
        if not player.has_drawn_pip_this_turn:
            drawn = player.draw_pip(self.bag)
            player.has_drawn_pip_this_turn = True
            player.draw_card(1)
            player.process_dots(self)
            self.log(f"{player.name} started turn: drew pip [{drawn}], drew 1 card.")
            self.check_game_over()
            return True
        return False

    def cast_spell(self, card_id, target_name):
        if self.p1.is_dead or self.p2.is_dead:
            return False
        player = self.active_player()
        if not player.has_drawn_pip_this_turn or player.has_cast_this_turn:
            return False

        card = next((c for c in player.hand if c.id == card_id), None)
        if not card or not player.can_cast(card):
            return False

        self.log(f"{player.name} attempts to cast {card.name}.")
        player.hand.remove(card)
        player.has_cast_this_turn = True

        roll = random.randint(1, 100)
        if roll > card.accuracy:
            self.log(f"Fizzle! {card.name} fizzled.")
            player.discard.append(card)
            return True

        pips_spent = player.spend_pips(card, self.bag)
        target = self.p1 if target_name == self.p1.name else self.p2

        # Override target context for buffs/self-heals
        if isinstance(card, HealSpell) or (isinstance(card, CharmSpell) and card.charm_type in ['blade_flat', 'blade_fixed']):
            target = player
        elif isinstance(card, WardSpell) and card.ward_type == 'shield':
            target = player  # shields go on yourself
        elif isinstance(card, CharmSpell) and card.charm_type == 'weakness':
            target = self.inactive_player()
        elif not isinstance(card, HealSpell) and not isinstance(card, CharmSpell):
            target = self.inactive_player()

        card.cast(player, target, pips_spent, self)
        player.discard.append(card)
        self.check_game_over()
        return True

    def pass_turn(self):
        player = self.active_player()
        if not player.has_drawn_pip_this_turn:
             # Force start of turn stuff
             self.draw_pip()
        self.log(f"{player.name} ends their turn.")
        self.turn = self.inactive_player().name
        self.active_player().has_drawn_pip_this_turn = False
        self.active_player().has_cast_this_turn = False
        if self.turn == self.p1.name:
             self.round += 1

    def check_game_over(self):
        if self.p1.is_dead and self.p2.is_dead:
            self.log("Match Over: It's a draw!")
        elif self.p2.is_dead:
            self.log(f"Match Over: {self.p1.name} wins!")
        elif self.p1.is_dead:
            self.log(f"Match Over: {self.p2.name} wins!")

    def to_dict(self):
        return {
            'round': self.round,
            'turn': self.turn,
            'p1': self.p1.to_dict(),
            'p2': self.p2.to_dict(),
            'bag_count': self.bag.count(),
            'logs': self.logs[-10:], # Return last 10 logs for UI
            'game_over': self.p1.is_dead or self.p2.is_dead
        }
