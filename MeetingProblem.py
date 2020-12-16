import random
import argparse
from meeting_implementation import Item
from meeting_implementation import Combination
from meeting_implementation import get_combinations
from meeting_implementation import get_stored_info_dict
from meeting_implementation import get_biggest_subset_size

parser = argparse.ArgumentParser(description='Solutions to the Meeting Problem')
parser.add_argument("--test", help="Which test to run (see README for codes)", type=int, default=1)
args = parser.parse_args()

# Turns a spartan list of meeting data into a more useful set of Item objects.
# Note that the IDs match the order of the original unsorted list.
def process_meeting_list(m_list, sort_method="none"):
    # Generating a new list of items, so remove existing ones
    Item.clear()

    # Copy the list so we can sort it
    # This is a little tricky: we want to add the initial ID for each item in the copied list, third in tuple
    list_copy = [(m[0], m[1], i) for i,m in enumerate(m_list)]
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
        item.set_unsorted_id(m[2])

# Prints out a list of the potential meetings for the day
def print_item_set(item_list=None):
    item_list = Item.items if item_list is None else item_list
    print("meetings are")
    print("-------------------------------------------")
    for item in item_list:
        item.print_representation()

# Prints info about the performance of a solution to a problem subset
def print_stored_info_dict(dict):
    # Contains: "combos", "removed", "best_score", "removal_score", "subset"
    print("------")
    print("subset:", dict['subset'])
    print("combos:", len(dict['combos']), Combination.get_combo_list_as_str(dict['combos']))
    print("removed:", len(dict['removed']), Combination.get_combo_list_as_str(dict['removed']))
    print("best score:", dict['best_score'])
    print("removal score:", "-" if dict['removal_score'] == -1 else str(dict['removal_score']))

# Tests for a clash between two items, given their indices
def test_clash(idx1, idx2):
    item1 = Item.items[idx1]
    item2 = Item.items[idx2]
    return item1.clash(item2)

# Runs some simple tests, for a predefined set of meetings
def run_test_simple():
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

# Runs a more elaborate series of tests for a predefined set of meetings
def run_test_fixed_set():
    meetings = [(9,14), (0,12), (4,7), (11,21), (0,1), (5,7), (10,10), (15,22), (9,12), (2,5)]
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
        print("biggest subset size:",get_biggest_subset_size())

# Generates a random set of meetings, then runs four tests, one with each sort method
# Returns a list of dictionaries, containing data about best test and worst test
def execute_random_tests():
    # Assumptions: there are thirty slots throughout the day, no meeting consumes more than ten. There are fifteen meetings
    # in total
    sort_methods = ["none", "start", "shortest", "longest"]
    total_slots = 30
    num_random_meetings = 15
    max_length = 10
    random_meeting_specs = []
    for i in range(num_random_meetings):
        length = random.randrange(max_length) + 1
        start = random.randrange(total_slots - length)
        end = start + length - 1
        random_meeting_specs.append((start, end))

    results = [{}, {}]

    # We try all the initial sorting methods and determine which yields the best results
    least_combinations_generated = 10000000
    most_combinations_generated = -1
    for i, sm in enumerate(sort_methods):
        process_meeting_list(random_meeting_specs, sm)
        combos = get_combinations()
        biggest_subset_size = get_biggest_subset_size()
        if biggest_subset_size < least_combinations_generated:
            least_combinations_generated = biggest_subset_size
            results[0]['items'] = Item.items
            results[0]['method'] = sm
            results[0]['combos'] = combos
            results[0]['biggest_subset'] = biggest_subset_size
        if biggest_subset_size > most_combinations_generated:
            most_combinations_generated = biggest_subset_size
            results[1]['items'] = Item.items
            results[1]['method'] = sm
            results[1]['combos'] = combos
            results[1]['biggest_subset'] = biggest_subset_size
    return results

# Generates a random set of meetings, then runs tests on them
def run_test_random_meetings():
    # Now, we generate some random meetings

    results = execute_random_tests()

    print("\nRandomly-chosen meetings")
    print("best sort method:",results[0]['method'])
    print_item_set(results[0]['items'])
    for combo in results[0]['combos']:
        print(combo.get_as_str())
    print("biggest subset size:",results[0]['biggest_subset'])
    print("worst sort method:",results[1]['method'])
    print_item_set(results[1]['items'])
    for combo in results[1]['combos']:
        print(combo.get_as_str())
    print("biggest subset size:",results[1]['biggest_subset'])

# Runs the algorithm on a large series of randomly-generated meeting sets. Collects statistics.
def collect_sorting_method_stats():

    sort_methods = ["none", "start", "shortest", "longest"]
    best_method_counts = {}
    worst_method_counts = {}
    for sm in sort_methods:
        best_method_counts[sm] = 0
        worst_method_counts[sm] = 0

    for i in range(100):
        if i % 10 == 0:
            print("Running set {} of random tests".format(int(i/10)))
        results = execute_random_tests()
        best_method_counts[results[0]['method']] = best_method_counts[results[0]['method']] + 1
        worst_method_counts[results[1]['method']] = worst_method_counts[results[1]['method']] + 1

    print("Best sort method")
    for k,v in best_method_counts.items():
        print("    {}: {}".format(k, v))
    print("Worst sort method")
    for k,v in worst_method_counts.items():
        print("    {}: {}".format(k, v))

if args.test == 0:
    run_test_simple()
elif args.test == 1:
    run_test_fixed_set()
elif args.test == 2:
    run_test_random_meetings()
elif args.test == 3:
    collect_sorting_method_stats()