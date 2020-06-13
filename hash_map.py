# hash_map.py
# ===================================================
# Implement a hash map with chaining
# ===================================================

class SLNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + (self.key)  + ', ' + str(self.value) + ')'

    def returnNode(self): 
        returnNode = (self.key, self.value)
        return returnNode

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """
        i = 0
        while i < (self.capacity):
            curNode = self._buckets[i].head

            if(self._buckets[i] != None): #iterate through hash table and delete each node that exists
                while curNode != None:
                    self._buckets[i].remove(curNode.key)
                    curNode = curNode.next
                    self.size = self.size - 1

            if i == self.capacity -1:
                break
            i = i + 1
        
        
    def get(self, key):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """

        if self.contains_key(key) == False:
            return None
        hashedKey= self._hash_function(key)
        bucket = hashedKey % self.capacity
        curNode = self._buckets[bucket].head #finds the node based on hashed key if it exists return val
        if(curNode!= None):
            if(curNode.key == key):
                return curNode.value 
            while curNode.next != None:
                curNode = curNode.next
                if(curNode.key == key):
                    return curNode.value

    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """

        newHash = HashMap(capacity, self._hash_function)


        
        i = 0
        while i < (self.capacity): #iterate through each bucket and node to rehash the node into new node
            curNode = self._buckets[i].head
            if(curNode != None):
                newVal = curNode.value
                newKey = curNode.key
                newHash.put(newKey, newVal)
                while curNode.next != None: 
                    curNode = curNode.next
                    newVal = curNode.value
                    newKey = curNode.key
                    newHash.put(newKey, newVal)
            if i == self.capacity -1:
                break
            i = i + 1
        self.capacity = newHash.capacity
        self._buckets = newHash._buckets
        self.size = newHash.size
        self._hash_function = newHash._hash_function



    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: they key to use to has the entry
            value: the value associated with the entry
        """

        hashedKey= self._hash_function(key)
        bucket = hashedKey % self.capacity

        
        
        if(self._buckets[bucket].contains(key) == None): #simply add new key to table if it doesnt exist
            self._buckets[bucket].add_front(key,value)
            self.size = self.size + 1

        else:
            updateNode = self._buckets[bucket].contains(key) #update value if key exists 
            updateNode.value = value 




    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            key: they key to search for and remove along with its value
        """

        if self.contains_key(key) == False:
            return None

        elif self.contains_key(key) == True:
            hashedKey= self._hash_function(key)
            bucket = hashedKey % self.capacity
            curNode = self._buckets[bucket]
            if(curNode!= None):
                curNode.remove(key) 

    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """
        hashedKey= self._hash_function(key)
        bucket = hashedKey % self.capacity

        
        
        if(self._buckets[bucket].contains(key) == None):
            return False

        else:
            return True


    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """
        i = 0
        count = 0
        while i < (self.capacity):
            if(self._buckets[i].head == None):
                count = 1 + count

            if i == self.capacity -1:
                break
            i = i + 1
        
        return count

    def bucket_keys(self):
        """
        Returns:
            A list of all the the buckets that are filled
        """
        L1 = []
        i = 0
        while i < (self.capacity):
            if(self._buckets[i].head != None):
                curNode = self._buckets[i].head
                L1.append(curNode)
                while curNode.next != None: 
                    curNode =curNode.next
                    L1.append(curNode)

            if i == self.capacity - 1:
                break
            i = i + 1
        return L1

    def returnNode(self,key):
        """
        Returns:
            Returns the node based on the key arguement
        """

        hashedKey= self._hash_function(key)
        bucket = hashedKey % self.capacity

        
        
        if(self._buckets[bucket].contains(key) == None):
            return None
        else:
            updateNode = self._buckets[bucket].contains(key)
            return updateNode


    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """

        numBuckets = self.capacity

        ratio = self.size / numBuckets

        return float(ratio) 


    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out
