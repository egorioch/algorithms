# Definition for a binary tree node.
import heapq
from collections import defaultdict
from functools import reduce
from typing import Optional, List, Counter


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # Step 1: Count the frequency of each element using a hash map
        freq = {}
        for num in nums:
            freq[num] = freq.get(num, 0) + 1

        # Step 2: Use a min-heap to store the top k frequent elements
        heap = []
        for num, count in freq.items():
            if len(heap) < k:
                heapq.heappush(heap, (count, num))
            elif count > heap[0][0]:
                heapq.heappushpop(heap, (count, num))

        # Step 3: Return the elements in the heap
        return [num for count, num in heap]


sol = Solution()
#  [1,-2,-3,1,3,-2,null,-1]
print(sol.topKFrequent([4, 1, -1, 2, -1, 2, 3], 2))
