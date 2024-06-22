# Description: Implementation of a hashmap with open addressing using quadratic probing.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Update key/value pair in hash map. If key exists, associated value replaced with the new value. If not in the hashmap, new key/value pair added.

        :param key: key of the pair
        :param value: value of pair
        """
        # determine if resizing necessary
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # use has function to determine index
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity

        # quadratic probing to determine index
        j = 0
        new_index = index
        while self._buckets[new_index] is not None:
            if not self._buckets[new_index].is_tombstone and self._buckets[new_index].key == key:
                # update value if the key is found and not a tombstone
                self._buckets[new_index].value = value
                return   
            if self._buckets[new_index].is_tombstone and self._buckets[new_index].key == key:
                # reactivate tombstone entry and update value
                self._buckets[new_index].is_tombstone = False
                self._buckets[new_index].value = value
                self._size += 1
                return
            j += 1
            new_index = (index + j ** 2) % self._capacity


        # insert new key, value pair in an empty slot
        self._buckets[new_index] = HashEntry(key, value)
        self._size += 1

    
    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capacity of the underlying table. Transfer key/value pairs to new table (all non-tombstone has table links must be rehashed).

        :param new_capacity: (int) new capacity of table
        """
        if new_capacity < self._size:
            return
        
        # ensure new capcity is prime
        if self._is_prime(new_capacity):
            new_capacity = new_capacity
        else:
            new_capacity = self._next_prime(new_capacity)

        # create new array 
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(None)

        # store old array of lists for rehashing
        old_buckets = self._buckets
        
        # update to the new buckets and capacity
        self._buckets = new_buckets
        self._capacity = new_capacity

        # reset size, will be updated during reinsertion
        self._size = 0  

        # rehash into new hashmap
        for i in range(old_buckets.length()):
            if old_buckets[i] is not None and not old_buckets[i].is_tombstone:
                self.put(old_buckets[i].key, old_buckets[i].value)

    def table_load(self) -> float:
        """
        Determine current hash table load factor.

        :return: (float) load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return number of empty buckets in the hash table.

        :return: (int) number of empty buckets
        """
        empty = 0

        # iterate through hash table to count empty buckets
        for i in range(self._capacity):
            if self._buckets[i] is None or self._buckets[i].is_tombstone:
                empty +=1

        return empty

    def get(self, key: str) -> object:
        """
        Return value associated with provided key. If not in the map, return None.

        :param key: key to search for

        :return: value of key
        """
        
        # determine hashed index
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity

        # quadratic probing to determine index
        j = 0
        new_index = index
        while self._buckets[new_index] is not None:
            if self._buckets[new_index].key == key and not self._buckets[new_index].is_tombstone:
                # return value if non tombstone key found
                return self._buckets[new_index].value
            j += 1
            new_index = (index + j ** 2) % self._capacity   

        return None
    def contains_key(self, key: str) -> bool:
        """
        Determine if key exists in the hash map. Return true if it does, false otherwise.

        :param: key to search for

        :return: (bool) true if present, false otherwise
        """
        # false for empty hash map
        if self._size == 0:
            return False

        # determine hashed index
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity

        # quadratic probing to determine index
        j = 0
        new_index = index
        while self._buckets[new_index] is not None:
            if self._buckets[new_index].key == key and not self._buckets[new_index].is_tombstone:
                # return true if non tombstone key located
                return True
            j += 1
            new_index = (index + j ** 2) % self._capacity

        return False

    def remove(self, key: str) -> None:
        """
        Remove given key and associated value from the has map. Does nothing if no such pair exists.

        :param key: key to remove
        """
        # determine hashed index
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity

        # quadratic probing to determine index
        j = 0
        new_index = index
        while self._buckets[new_index] is not None:
            if self._buckets[new_index].key == key and not self._buckets[new_index].is_tombstone:
                # update tombstone status and reduce size
                self._buckets[new_index].is_tombstone = True
                self._size -= 1
                return
            j += 1
            new_index = (index + j ** 2) % self._capacity  

        return None

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a dynamic array where each index contains a tuple of each key/value pair stored in the hash map.

        :return: Dynamic array 
        """
        # create new array
        new_array = DynamicArray()

        # iterate through hash map to collect non-tombstone entries
        for i in range(self._capacity):
            if self._buckets[i] is not None and not self._buckets[i].is_tombstone:
                # append as a tuple (key, value)
                new_array.append((self._buckets[i].key, self._buckets[i].value))

        return new_array

    def clear(self) -> None:
        """
        Clears contents of the hash map. Does not change capacity.
        """
        # reinitialize buckets
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        # reset size
        self._size = 0

    def __iter__(self):
        """
        Create iterator for loop
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Return the next item from the hash map.
        """
        # iterate
        while self._index < self._capacity:
            current_entry = self._buckets[self._index]
            self._index += 1
            # return next entry
            if current_entry is not None and not current_entry.is_tombstone:
                return current_entry
        raise StopIteration


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
