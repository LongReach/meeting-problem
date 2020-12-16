# Represents a single meeting
class Item(object):

    items = []

    def __init__(self, start, last, index, score=1):
        self.start = start
        self.last = last
        self.index = index
        self.unsorted_id = index # Useful if we presort the set of meetings, but want to track by original order
        self.score = score
        Item.items.append(self)

    def set_unsorted_id(self, id):
        self.unsorted_id = id

    # Returns True if this item clashes with another
    def clash(self, other):
        if self.last >= other.start and self.last <= other.last: return True # my right edge overlaps with other
        if self.start >= other.start and self.start <= other.last: return True # my left edge overlaps with other
        if self.start <= other.start and self.last >= other.last: return True # other is entirely inside my space
        return False

    # Each meeting is assigned a letter for ease of identification
    def get_letter(self):
        return chr(ord('a') + self.unsorted_id)

    # Print out a line of text indicating where this meeting is located in time
    def print_representation(self):
        letter = self.get_letter()
        spaces = self.start
        num_lets = self.last - self.start + 1
        idx_as_str = str(self.index)
        idx_as_str = idx_as_str + ":" + " " * (3 - len(idx_as_str))
        print(idx_as_str + " " * spaces + letter * num_lets)

    def __str__(self):
        return "{}: ({},{})".format(self.index, self.start, self.last)

    # Gets an item by index
    @staticmethod
    def get_item(idx):
        return Item.items[idx]

    # Number of known items
    @staticmethod
    def num_items():
        return len(Item.items)

    # Clear list of items, so a new set can be generated
    @staticmethod
    def clear():
        Item.items = []

# A combination represents a group of compatible items (i.e. meetings that don't conflict)
class Combination(object):

    def __init__(self, item=None):
        self.score = 0
        # array[n] contains reference to item if in combo, None otherwise
        self.array = [None] * len(Item.items)
        if item is not None:
            self.array[item.index] = item
            self.score = item.score

    # Puts an item into combination. Caller must make sure it doesn't clash
    def add_item(self, item):
        self.array[item.index] = item
        self.score = self.score + item.score

    # Returns true if specified item is in this combination
    def has_item(self, item):
        return self.array[item.index] is not None

    # Makes a copy of this combination, returns new instance
    def copy(self):
        new_combo = Combination()
        new_combo.score = self.score
        for n,item in enumerate(self.array):
            new_combo.array[n] = self.array[n]
        return new_combo

    # Determines if any item in this combination clashes with other item
    # Returns True or False, item with which there is a clash
    def clashes(self, other_item):
        for item in self.array:
            if item is not None:
                if item.clash(other_item):
                    return True, item
        return False, None

    # Returns combination as list of strings
    def get_as_str_list(self):
        str_list = []
        for item in self.array:
            if item is not None:
                str_list.append(item.get_letter())
        return str_list

    # Returns a string representing combination
    def get_as_str(self):
        out_str, sep_str = "(", ""
        for item in self.array:
            if item is not None:
                out_str = out_str + sep_str + item.get_letter()
                sep_str = ","
        out_str = out_str + ")"
        return out_str

    def __str__(self):
        return self.get_as_str()

    # Given a list of combinations, represent them all as a single string
    @staticmethod
    def get_combo_list_as_str(combos):
        out_str, sep_str = "", ""
        for c in combos:
            out_str = out_str + sep_str + str(c)
            sep_str = ","
        return out_str

    # Given a list of numerical indices representing items, generate that Combination
    @staticmethod
    def make_test_combo(list_of_indices):
        combo = Combination()
        for idx in list_of_indices:
            item = Item.items[idx]
            clash, clash_item = combo.clashes(item)
            if not clash:
                combo.add_item(item)
            else:
                pass
        return combo

    # Given a list of existing combinations, generate a list of new combinations that contain specified item.
    # Only valid combinations are returned; if there's a clash with an existing combination, the new one isn't used.
    @staticmethod
    def generate_new_combos(old_list, new_item):
        fresh_list = []
        for combo in old_list:
            fresh_list.append(combo.copy())

        # Now, we reduce the list, removing combos that clash
        while True:
            was_clash, clash_item = False, None
            for combo in fresh_list:
                was_clash, clash_item = combo.clashes(new_item)
                if was_clash: break

            # If no clashes, then the new_list is good to go
            if not was_clash: break

            # Prune down new list; all combos that contain the clash item must go
            kept_combo_list = []
            for combo in fresh_list:
                if not combo.has_item(clash_item):
                    kept_combo_list.append(combo)
            # Now, this will be the pruned list
            fresh_list = kept_combo_list

        # Now that we have a list of combos that don't clash with new_item, add new_item to each one
        for combo in fresh_list:
            combo.add_item(new_item)
        return fresh_list

# The entry for each subset (1...n) contains a dictionary of:
#     combinations found by solving the subset
#     combinations removed
#     best score
#     removal score
combinations_for_subset = []
biggest_subset_size = 0

# The workhorse function. When a list of items has been established, we call this function. It returns a list of
# the best combinations found. If n is specified, then the function solves the problem only for the subset of
# items from 1 to n. It calls itself recursively.
# Returns: a list of combinations that are the best solutions for subset 1 to n
def get_combinations(n=None):
    global combinations_for_subset
    global biggest_subset_size
    n = Item.num_items()-1 if n is None else n
    subset_info_dict = {'combos':[], 'removed':[], 'best_score':0, 'removal_score':0, 'subset':0}
    if n == 0:
        # Most trivial subset
        combos = [Combination(), Combination(Item.items[0])]
        combinations_for_subset = [None for i in Item.items] # initialize this array
        biggest_subset_size = 0
        subset_info_dict['combos'] = combos
        subset_info_dict['best_score'] = 1
        combinations_for_subset[n] = subset_info_dict
        return combos

    # Get combinations that solve the smaller subset
    combos = get_combinations(n-1)
    # Generate combinations specific to this subset
    new_combos = Combination.generate_new_combos(combos, Item.items[n])
    combos = combos + new_combos
    combos.sort(key=lambda x: x.score, reverse=True)

    # remove any combos that underperform
    if len(combos) > 1:
        potential_points_left = Item.num_items() - 1 - n
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
        underperformers = []
        fresh_list = []
        for c in combos:
            if c.score >= scores[0]:
                fresh_list.append(c)
            else:
                underperformers.append(c)
        subset_info_dict['removed'] = underperformers
        subset_info_dict['best_score'] = scores[-1]
        subset_info_dict['removal_score'] = scores[0]-1
        combos = fresh_list

    subset_info_dict['combos'] = combos
    subset_info_dict['subset'] = n
    combinations_for_subset[n] = subset_info_dict
    if len(combos) > biggest_subset_size:
        biggest_subset_size = len(combos)

    return combos

# Returns a dictionary containing information about the solution to subset 1 to n
# Contains: "combos", "removed", "best_score", "removal_score"
def get_stored_info_dict(subset_num):
    return combinations_for_subset[subset_num]

# One subset produces more combinations than any other. Return the number of combinations.
def get_biggest_subset_size():
    return biggest_subset_size