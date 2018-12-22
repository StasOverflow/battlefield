class Unit:
    hp = 0
    recharge_time = 0
    damage = 0
    attack_success_prob = 0
    damage = 0
    cooldown = 0

    def __repr__(self):
        type_of = self.__class__.__name__
        repr_string = type_of + ' | HP: ' + str(self.hp) \
                              + ' | DMG: ' + str(self.damage) \
                              + ' | cd: ' + str(self.cooldown) + ' |'
        # print(repr_string)
        return repr_string

