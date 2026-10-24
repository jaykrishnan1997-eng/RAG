#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_garden_analytics.py                               :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/12 15:03:28 by jkrishna            #+#    #+#            #
#   Updated: 2026/06/29 13:34:10 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

class Plant:
    class Stat:
        def __init__(self) -> None:
            self.stat_age = 0
            self.stat_grow = 0
            self.stat_show = 0

        def show_stat(self, name: str) -> None:
            print(f"[statistics for {name}]")
            print(f"Stats: {self.stat_grow} grow, "
                  f"{self.stat_age} age, "
                  f"{self.stat_show} show")

    def __init__(self, name: str, height: float, age: float) -> None:
        self._name = name
        self._height = height
        self._age = age
        self._stat = Plant.Stat()

    def set_age(self) -> None:
        self._age += 1
        self._stat.stat_age += 1

    def set_grow(self) -> None:
        self._height = round(self._height + 8.0, 1)
        self._stat.stat_grow += 1

    # def get_age(self) -> float:
    #     return (self._age)

    # def get_grow(self) -> float:
    #     return (self._height)

    def show(self) -> None:
        print(self._name + ": " + str(self._height) + "cm, " +
              str(self._age) + " days old")
        self._stat.stat_show += 1

    def stat(self) -> None:
        self._stat.show_stat(self._name)

    @staticmethod
    def check_age(ch_age: float) -> None:
        res = str(ch_age > 365)
        print("Is " + str(ch_age) + " days more than a year? -> " + res)

    @classmethod
    def create_anonymous(cls) -> "Plant":
        return cls("Unknown plant", 0.0, 0)


class Flower(Plant):
    def __init__(
        self, name: str, height: float, age: float, color: str
    ) -> None:
        super().__init__(name, height, age)
        self._color = color
        self._bloom = 0

    def bloom(self) -> None:
        # print("[asking the " + self._name + " to bloom]")
        self._bloom = 1

    def show(self) -> None:
        super().show()
        print(" Color: " + self._color)
        if (self._bloom == 0):
            print(" " + self._name + " has not bloomed yet")
        else:
            print(" " + self._name + " is blooming beautifully!")


class Tree(Plant):
    class Stat(Plant.Stat):
        def __init__(self) -> None:
            super().__init__()
            self.stat_shade = 0

        def show_stat(self, name: str) -> None:
            super().show_stat(name)
            print(f" {self.stat_shade} shade")

    def __init__(
        self, name: str, height: float, age: float, trunk_diameter: float
    ) -> None:
        super().__init__(name, height, age)
        self._trunk_diameter = trunk_diameter
        self._tree_stat = Tree.Stat()

    def stat(self) -> None:
        self._tree_stat.show_stat(self._name)

    def produce_shade(self) -> None:
        print("[asking the " + self._name + " to produce shade]")
        print("Tree " + self._name + " now produces a shade of " +
              str(self._height) + "cm long and " + str(self._trunk_diameter)
              + "cm wide.")
        self._tree_stat.stat_shade += 1

    def show(self) -> None:
        super().show()
        self._tree_stat.stat_show += 1
        print(" Trunk diameter: " + str(self._trunk_diameter) + "cm")


class Seed(Flower):
    def __init__(
        self, name: str, height: float, age: float, color: str, seeds: float
    ) -> None:
        super().__init__(name, height, age, color)
        self._seeds = seeds

    def set_age(self) -> None:
        self._age += 20
        self._stat.stat_age += 1

    def set_grow(self) -> None:
        self._height = round(self._height + 30.0, 1)
        self._stat.stat_grow += 1

    def bloom(self) -> None:
        super().bloom()
        self._seeds = 42

    def show(self) -> None:
        super().show()
        print(f" Seeds: {self._seeds}")


def display_stats(plant: Plant) -> None:
    plant.stat()


if __name__ == "__main__":
    print("=== Garden statistics ===")
    print("=== Check year-old")
    Plant.check_age(30)
    Plant.check_age(400)
    print("\n=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    rose.show()
    rose.stat()
    print("[asking the rose to grow and bloom]")
    rose.set_grow()
    rose.bloom()
    rose.show()
    rose.stat()
    print("\n=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    oak.stat()
    oak.produce_shade()
    oak.stat()
    print("\n=== Seed")
    sunflower = Seed("Sunflower", 80.0, 45, "yellow", 0)
    sunflower.show()
    print("[make " + sunflower._name + " grow, age and bloom]")
    sunflower.set_grow()
    sunflower.set_age()
    sunflower.bloom()
    sunflower.show()
    sunflower.stat()
    print("\n=== Anonymous")
    unknown = Plant.create_anonymous()
    unknown.show()
    display_stats(unknown)
