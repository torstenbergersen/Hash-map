# Hash-map

# Overview

This code serves as the culmination of my Data Structures course at Oregon State University. It showcases my implementation of a hashmap. My project explores two methods for managing collisions within the hashmap: chaining and open addressing with quadratic probing.

In the chaining method, each slot of the hashmap array contains a linked list to hold multiple entries that hash to the same index. This approach simplifies handling collisions but can lead to inefficiencies if the lists become too long.

Alternatively, the open addressing method with quadratic probing avoids the need for additional data structures by resolving collisions within the array itself. With this technique I probe the hashmap at quadratically increasing intervals from the original point of conflict until an empty slot is found. This method is efficient in terms of space usage since all data is stored within the array itself and is particularly effective when the load factor is low to moderate.

By implementing both strategies in my final project, I was able to understand their mechanics, performance implications, and suitable use cases. This project reinforced my grasp of key theoretical concepts and honed my practical programming skills, preparing me for real-world software development challenges.
