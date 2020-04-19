class Type:
    Melee = "Melee"
    Ranged = "Ranged"

class Weapon:
    def __init__(self, name: str, weaponType: Type, damage: int = 0, critMultiplier: int = 2, critThreshold: int = 20):
        self.name = name
        self.type = weaponType
        self.damage = damage
        self.critMultiplier = critMultiplier
        self.critThreshold = critThreshold

    def __repr__(self):
        return self.name

class Shortbow(Weapon):
    def __init__(self):
        super().__init__(
            name="Shortbow", 
            weaponType=Type.Ranged, 
            damage=6
        )


class Longbow(Weapon):
    def __init__(self):
        super().__init__(
            name="Longbow", 
            weaponType=Type.Ranged, 
            damage=8
        )


class Axe(Weapon):
    def __init__(self):
        super().__init__(
            name="Axe", 
            weaponType=Type.Melee, 
            damage=6
        )


class Dagger(Weapon):
    def __init__(self):
        super().__init__(
            name="Dagger", 
            weaponType=Type.Melee, 
            damage=4, 
            critThreshold=19
        )


class Shortsword(Weapon):
    def __init__(self):
        super().__init__(
            name="Shortsword",
            weaponType=Type.Melee,
            damage=4
        )


class Greatsword(Weapon):
    def __init__(self):
        super().__init__(
            name="Greatsword",
            weaponType=Type.Melee,
            damage=6,
            critThreshold=19
        )


class Longspear(Weapon):
    def __init__(self):
        super().__init__(
            name="Longspear",
            weaponType=Type.Melee,
            damage=8,
            critMultiplier=3
        )