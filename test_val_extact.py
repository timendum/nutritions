from coop import KCAL_TO_KJ, Coop


def main():
    assert Coop._prase_value("3,7 g") == 3.7
    assert Coop._prase_value("3,7g") == 3.7
    assert Coop._prase_value("0.1 g") == 0.1
    assert Coop._prase_value("0.1g") == 0.1
    assert Coop._prase_value("<0.1 g") == 0
    assert Coop._prase_value("<0,1g") == 0
    assert Coop._prase_value("<0.6g") == 0
    assert Coop._prase_value("<0,6g") == 0
    assert Coop._prase_value("431 kj") == 431 / KCAL_TO_KJ
    assert Coop._prase_value("102 kcal") == 102
    assert Coop._prase_value("431kj") == 431 / KCAL_TO_KJ
    assert Coop._prase_value("102kcal") == 102
    assert Coop._prase_value("224 kj / 53 kcal") == 53
    assert Coop._prase_value("224 kj 53 kcal") == 53
    assert Coop._prase_value("224 kcal 53 kj") == 224
    assert Coop._prase_value("93 kcal / 394kj") == 93
    assert Coop._prase_value("224kj / 53kcal") == 53
    assert Coop._prase_value("224kj 53kcal") == 53
    assert Coop._prase_value("224kcal 53kj") == 224
    assert Coop._prase_value("93kcal / 394kj") == 93
    assert Coop._prase_value("309 kj (74 kcal)") == 74
    assert Coop._prase_value("3mg") == 0.003
    assert Coop._prase_value("96µg") is None
    assert Coop._prase_value("") is None


main()
