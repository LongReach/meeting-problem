from meeting_implementation import Item
from meeting_implementation import Combination

def process_meeting_list(m_list):
    # Sort the meetings by start time to make results easier to see
    m_list.sort(key=lambda x: x[0])
    for i, m in enumerate(m_list):
        item = Item(m[0], m[1], i)

meetings = [(9,14), (0,12), (4,7), (11,21), (0,1), (5,7), (10,10), (15,22), (9,12), (2,5)]

process_meeting_list(meetings)

# Each
combinations_for_subset = []

def get_combinations(n):
    if n == 0:
        # Most trivial subset
        return [Combination(), Combination(Item.items[0])]

    combos = get_combinations(n-1)
    new_combos = Combination.generate_new_combos(combos, Item.items[n])
    combos = combos + new_combos
    combos.sort(key=lambda x: x.score, reverse=True)

    # remove any combos that underperform
    if len(combos) > 1:
        potential_points_left = len(Item.items) - 1 - n
        # Find the best and worst scores. If worst score can be added to potential points remaining and still
        # not beat best score, throw it out.
        scores = []
        for c in combos:
            if c.score not in scores:
                scores.insert(0, c.score)
        if len(scores) > 1:
            while(True):
                remove_lowest_score = False
                for i in range(1,len(scores)):
                    if scores[0] + potential_points_left <= scores[i]:
                        remove_lowest_score = True
                        break
                if not remove_lowest_score:
                    break
                scores.pop(0)
        # Now we have an array of scores that are valid. Remove every combo that scores lower than lowest score
        print("*** Remove scores at or below",scores[0]-1,", potential points left",potential_points_left,", best score",scores[-1])
        underperformers = []
        fresh_list = []
        for c in combos:
            if c.score >= scores[0]:
                fresh_list.append(c)
            else:
                underperformers.append(c.get_as_str())
        print("   underperformers were ", underperformers)
        combos = fresh_list

    return combos

def print_item_set():
    print("\nmeetings are")
    print("-------------------------------------------")
    for item in Item.items:
        item.print_representation()

def test_clash(idx1, idx2):
    item1 = Item.items[idx1]
    item2 = Item.items[idx2]
    #print("test clash for [{}],[{}]".format(str(item1), str(item2)))
    if item1.clash(item2):
        if not item2.clash(item1):
            print("bad clash test")
        else:
            print("clash for {},{}".format(idx1, idx2))
    else:
        print("no clash for {},{}".format(idx1, idx2))

print_item_set()

print("\ntest combos")
some_test_combos = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]
for tc_spec in some_test_combos:
    tc = Combination.make_test_combo(tc_spec)
    print(tc_spec, "to", tc.get_as_str())

print("\ntest clashes")
test_clash(0, 1)
test_clash(1, 2)
test_clash(2, 1)
test_clash(4, 0)

print_item_set()

subset_size = 10
print("\ncombos for subset size {} are:".format(subset_size))
combos = get_combinations(subset_size-1)
for combo in combos:
    print(combo.get_as_str())
