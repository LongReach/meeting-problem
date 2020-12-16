from meeting_implementation import Item
from meeting_implementation import Combination
from meeting_implementation import get_combinations
from meeting_implementation import get_stored_info_dict

# Turns a spartan list of meeting data into a more useful set of Item objects
def process_meeting_list(m_list, sort_method="none"):
    # Generating a new list of items, so remove existing ones
    Item.clear()

    # copy the list so we can sort it
    list_copy = [m for m in m_list]
    if sort_method == "start":
        # Sort the meetings by start time to make results easier to see
        list_copy.sort(key=lambda x: x[0])
    elif sort_method == "shortest":
        # Sort the meetings by length to make results easier to see
        list_copy.sort(key=lambda x: (x[1] - x[0] + 1))
    elif sort_method == "longest":
        # Sort the meetings by length to make results easier to see
        list_copy.sort(key=lambda x: (x[1] - x[0] + 1), reverse=True)
    for i, m in enumerate(list_copy):
        item = Item(m[0], m[1], i)

def print_item_set():
    print("meetings are")
    print("-------------------------------------------")
    for item in Item.items:
        item.print_representation()

def print_stored_info_dict(dict):
    # Contains: "combos", "removed", "best_score", "removal_score", "subset"
    print("------")
    print("subset:", dict['subset'])
    print("combos:", Combination.get_combo_list_as_str(dict['combos']))
    print("removed:", Combination.get_combo_list_as_str(dict['removed']))
    print("best score:", dict['best_score'])
    print("removal score:", "-" if dict['removal_score'] == -1 else str(dict['removal_score']))

def test_clash(idx1, idx2):
    item1 = Item.items[idx1]
    item2 = Item.items[idx2]
    return item1.clash(item2)

meetings = [(9,14), (0,12), (4,7), (11,21), (0,1), (5,7), (10,10), (15,22), (9,12), (2,5)]
process_meeting_list(meetings)

print("\nInitial meeting list")
print("-----------------------------------")
print_item_set()

print("\ntest combos")
print("-----------------------------------")
some_test_combos = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]
expected_outcomes = ["(a,c)", "(a,c)", "(b)", "(b)", "(a,c)", "(a,c)"]
for n, tc_spec in enumerate(some_test_combos):
    tc = Combination.make_test_combo(tc_spec)
    if str(tc) == expected_outcomes[n]:
        print("As expected:", tc_spec, "to", tc.get_as_str())
    else:
        print("Bad result:", tc_spec, "to", tc.get_as_str())

print("\ntest clashes")
print("-----------------------------------")
test_clashes = [(0, 1, True), (1, 2, True), (2, 1, True), (4, 0, False), (5, 9, True)]
for t_cl in test_clashes:
    result = test_clash(t_cl[0], t_cl[1])
    result_str = "as expected" if result == t_cl[2] else "NOT as expected"
    print("Clash test of ({},{}) returns result {} {}".format(t_cl[0], t_cl[1], result, result_str))

# Now we try the initial meeting set with different sorting arrangements
sort_methods = ["none", "start", "shortest", "longest"]
for sm in sort_methods:
    process_meeting_list(meetings, sm)
    print("\nMeeting list with sort method:", sm)
    print_item_set()
    combos = get_combinations()
    for n in range(Item.num_items()):
        dict = get_stored_info_dict(n)
        print_stored_info_dict(dict)
    print("-------\nfinal outcome")
    for combo in combos:
        print(combo.get_as_str())
