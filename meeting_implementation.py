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

# Multiple rooms: a combination would have multiple arrays instead of one
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

