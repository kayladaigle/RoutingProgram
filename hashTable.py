
# Develop a hash table that has an insertion function that takes the package ID as input

# ref:C950 Webinar 1 - Let's Go Hashing

class HashTable:
    def __init__(self, initial_capacity=10):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # have insert function do hash chaining so that collision  does not happen
    def insert(self, key, item):

        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        bucket_list.append([key, item])
        return True

    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for keyValue in bucket_list:
            if keyValue[0] == key:
                return keyValue[1]

        return None

    def remove(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv)
                return True
"""
test hash table functionality
theHash = HashTable()
theHash.insert(1, 'Kayla')
theHash.insert(10, 'Bob')
theHash.insert(40, 'Carl')
theHash.insert(5, 'Casey')
theHash.remove(1, 'Kayla')
theHash.remove(40, 'Carl')
theHash.remove(5, 'Casey')
theHash.remove(10, 'Bob')
print(theHash.table)
"""

