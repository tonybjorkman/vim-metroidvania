from characters import *


def test_wordfactory():
    wordfactory = WordListFactory()
    input = "abc.123().tre_end"
    for i in input:
        wordfactory.append_word_from_chars((10,10),Character(i,(10,10)))
    output = "a.1(t"
    outstring = ""
    for w in wordfactory.words:
        for subw in w.subwords:
            print(subw.get_first_character().type)
            outstring += subw.get_first_character().type

    assert outstring == output