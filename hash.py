# Creation of a class for the hash table
class Hashtable:
    def __init__(self, initial_capacity=20):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # This allows a new item to be inserted into the hash table
    def insert_item(self, key, item):  # inserts and updates
        buck = hash(key) % len(self.table)
        bl = self.table[buck]

        # the key is updated if it's already in the bucket
        # bl = bucket list
        for kv in bl:  # O(n) time
            if kv[0] == key:
                kv[1] = item
                return True
        # if the key is not in the bucket, the item is inserted on the end of the bl (bucket list)
        key_value = [key, item]
        bl.append(key_value)
        return True

    # Gives ability to search for items within the hash table
    def lookup_item(self, key):
        buck = hash(key) % len(self.table)
        bl = self.table[buck]
        for duo in bl:
            if key == duo[0]:
                return duo[1]
        return None

    # Gives ability to remove an item from the hash table
    def remove_item(self, key):
        entry = hash(key) % len(self.table)
        location = self.table[entry]

        if key in location:
            location.remove(key)
