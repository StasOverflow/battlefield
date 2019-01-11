from models.units.unit import Unit


@Unit.register('squad')
class Squad:
    hp = 0
    attack = 0
    damage = 0
    call_sign = ''

    def __init__(self, unit_quantity, call):
        unit_types = list(Unit.UNIT)
        print(unit_types)
        self.units = [Unit.new() for _ in range(unit_quantity)]

    def __repr__(self):
        print("i have this many units ", len(self.units))
        string = self.call_sign
        print(string)
        for x in self.units:
            print(x)
        # string = string + '\n'.join(str(self.units))
        return ''
