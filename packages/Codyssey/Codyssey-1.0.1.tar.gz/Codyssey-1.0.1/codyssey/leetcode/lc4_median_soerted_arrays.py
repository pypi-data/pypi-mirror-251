"""
Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).

Example 1:
    Input: nums1 = [1,3], nums2 = [2]
    Output: 2.00000
    Explanation: merged array = [1,2,3] and median is 2.

Example 2:
    Input: nums1 = [1,2], nums2 = [3,4]
    Output: 2.50000
    Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.

Constraints:
    nums1.length == m
    nums2.length == n
    0 <= m <= 1000
    0 <= n <= 1000
    1 <= m + n <= 2000
    -106 <= nums1[i], nums2[i] <= 106
"""
from typing import List


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        """Finds the median of two sorted arrays nums1 and nums2.

        Args:
            nums1 (List[int]): First sorted array
            nums2 (List[int]): Second sorted array

        Returns:
            float: The median of the merged and sorted array

        Time Complexity: O(m+n)
            Where m and n are the lengths of nums1 and nums2.

        Space Complexity: O(m+n)
            The merged array can contain up to m+n elements.
        """
        merged_array = self.merge_arrays(nums1, nums2)
        N = len(merged_array)
        return merged_array[N//2] if N%2 != 0 else (merged_array[N//2] + merged_array[N//2-1])/2

    def merge_arrays(self, nums1: List[int], nums2: List[int]) -> List[int]:
        """Merges two sorted arrays nums1 and nums2 into a single sorted array.

            Args:
                nums1 (List[int]): First sorted array
                nums2 (List[int]): Second sorted array

            Returns:
                List[int]: Merged sorted array

            Time Complexity: O(m+n)
                Where m and n are the lengths of nums1 and nums2.

            Space Complexity: O(m+n)
                The merged array can contain up to m+n elements.
            """

        merged_array = []
        i, j = 0, 0
        while i < len(nums1) and j < len(nums2):
            if nums1[i] < nums2[j]:
                merged_array.append(nums1[i])
                i += 1
            else:
                merged_array.append(nums2[j])
                j += 1

        return merged_array + nums1[i:] + nums2[j:]


if __name__ == "__main__":
    s = Solution()
    print(s.findMedianSortedArrays([1, 3], [2]))
    print(s.findMedianSortedArrays([1, 2], [3, 4]))
    print(s.findMedianSortedArrays([0, 0], [0, 0]))
    print(s.findMedianSortedArrays([1, 2, 3], [4, 5, 6]))