# Description: Implementation of a hashmap with chaining.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        # use has function to determine index
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity

        # retreive list at given index
        bucket = self._buckets[index]

        # check if key exists in the list
        node = bucket.contains(key)
        if node:
            # update value
            node.value = value
        else:
            # insert new key-value pair
            bucket.insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capcity of the table. Transfer existing key/value pairs into the new table, rehashing table links.

        :param new_capacity: new capacity of the hash table
        """
        if new_capacity < 1:
            return

        # ensure new capcity is prime
        if self._is_prime(new_capacity):
            new_capacity = new_capacity
        else:
            new_capacity = self._next_prime(new_capacity)

        # create new array 
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(LinkedList())

        # store old array of lists for rehashing
        old_buckets = self._buckets
        old_capacity = self._capacity
        
        # update to the new buckets and capacity
        self._buckets = new_buckets
        self._capacity = new_capacity
        # reset size, will be updated during reinsertion
        self._size = 0  

        # rehash all key-value pairs into the new buckets
        for i in range(old_capacity):
            current_bucket = old_buckets[i]
            for node in current_bucket:
                self.put(node.key, node.value)
    
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
            if self._buckets[i].length() == 0:
                empty += 1

        return empty

    def get(self, key: str) -> object:
        """
        Return value associated with provided key. If not in the map, return None.

        :param key: key to search for

        :return: value of key
        """
        # determine index
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity

        # retreive list at given index
        bucket = self._buckets[index]

        # check if key exists in the list
        node = bucket.contains(key)
        if node:
            # return value
            return node.value
        else:
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

        # retreive list at given index
        bucket = self._buckets[index]

        # check if key exists in the list
        node = bucket.contains(key)
        if node:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Remove given key and associated value from the has map. Does nothing if no such pair exists.

        :param key: key to remove
        """
        if self._size == 0:
            return

        # determine hashed index
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity

        # retreive list at given index
        bucket = self._buckets[index]

        # check if key exists in the list
        node = bucket.contains(key)
        if node:
            bucket.remove(key)
            # decrement size after removal
            self._size -= 1
        else:
            return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a dynamic array where each index contains a tuple of each key/value pair stored in the hash map.

        :return: Dynamic array 
        """
        # create new array
        new_array = DynamicArray()

        # iterate through hash map
        for i in range(self._capacity):
            current_bucket = self._buckets[i]
            # if bucket contains items, iterate through and retrieve key-value pairs
            if current_bucket.length() > 0:
                for node in current_bucket:
                    new_array.append((node.key, node.value))
            else:
                continue
        return new_array


    def clear(self) -> None:
        """
        Clears contents of the hash map. Does not change capacity.
        """
        # reinitialize buckets
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        # reset size
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Find mode and number of occurrences from an unsorted dynamic array.

    :param da: dynamic array for mode search

    :return: (tuple) a tuple with a dynamic array containing all modes and the  
            integer amount of occurrences
    """
    # use seperate chaining hashmap
    map = HashMap()
    mode = DynamicArray()
    max_frequency = 0

    # populate hash with frequencies
    for i in range(da.length()):
        if map.contains_key(da[i]):
            frequency = map.get(da[i]) + 1
            map.put(da[i], frequency)
        else:
            frequency = 1
            map.put(da[i], 1)
    
        # update max_freq if needed
        if frequency > max_frequency:
                max_frequency = frequency

    # identify elements with maximum frequency
    key_values = map.get_keys_and_values()
    for i in range(key_values.length()):
        key, freq = key_values[i]
        if freq == max_frequency:
            mode.append(key)
    
    return (mode, max_frequency)
        
    

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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
