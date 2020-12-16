class Item(object):

    items = []

    def __init__(self, start, last, index, score=1):
        self.start = start
        self.last = last
        self.index = index
        self.score = score
        Item.items.append(self)

    def clash(self, other):
        if self.last >= other.start and self.last <= other.last: return True # my right edge overlaps with other
        if self.start >= other.start and self.start <= other.last: return True # my left edge overlaps with other
        if self.start <= other.start and self.last >= other.last: return True # other is entirely inside my space
        return False

    def print_representation(self):
        letter = chr(ord('a') + self.index)
        spaces = self.start
        num_lets = self.last - self.start + 1
        idx_as_str = str(self.index)
        idx_as_str = idx_as_str + ":" + " " * (3 - len(idx_as_str))
        print(idx_as_str + " " * spaces + letter * num_lets)

    def __str__(self):
        return "{}: ({},{})".format(self.index, self.start, self.last)

    @staticmethod
    def get_item(idx):
        return Item.items[idx]


class Combination(object):

    def __init__(self, item=None):
        self.score = 0
        # array[n] contains reference to item if in combo, None otherwise
        self.array = [None] * len(Item.items)
        if item is not None:
            self.array[item.index] = item
            self.score = item.score

    def add_item(self, item):
        self.array[item.index] = item
        self.score = self.score + item.score

    def has_item(self, item):
        return self.array[item.index] is not None

    def copy(self):
        new_combo = Combination()
        new_combo.score = self.score
        for n,item in enumerate(self.array):
            new_combo.array[n] = self.array[n]
        return new_combo

    # Returns True or False, item with which there is a clash
    def clashes(self, other_item):
        for item in self.array:
            if item is not None:
                if item.clash(other_item):
                    return True, item
        return False, None

    def get_as_str_list(self):
        str_list = []
        for item in self.array:
            if item is not None:
                str_list.append(str(chr(ord('a') + item.index)))
        return str_list

    def get_as_str(self):
        out_str = "("
        sep_str = ""
        for item in self.array:
            if item is not None:
                out_str = out_str + sep_str + chr(ord('a') + item.index)
                sep_str = ","
        out_str = out_str + ")"
        return out_str

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

def process_meeting_list(m_list):
    # Sort the meetings by start time to make results easier to see
    m_list.sort(key=lambda x: x[0])
    for i, m in enumerate(m_list):
        item = Item(m[0], m[1], i)

meetings = [(9,14), (0,12), (4,7), (11,21), (0,1), (5,7), (10,10), (15,22), (9,12), (2,5)]

process_meeting_list(meetings)

def get_combinations(n):
    if n == 0:
        # Most trivial subset
        return [Combination(), Combination(Item.items[0])]

    combos = get_combinations(n-1)
    new_combos = Combination.generate_new_combos(combos, Item.items[n])
    return combos + new_combos

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
