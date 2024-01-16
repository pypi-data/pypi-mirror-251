"""
Given a string s, return the longest
palindromic substring in s.

Example 1:
    Input: s = "babad"
    Output: "bab"
    Explanation: "aba" is also a valid answer.

Example 2:
    Input: s = "cbbd"
    Output: "bb"

Constraints:
    1 <= s.length <= 1000
    s consist of only digits and English letters.
"""

class Solution:
    def longestPalindrome(self, s: str) -> str:
        """
        Finds the longest palindrome substring in the given string s.

        Time Complexity: O(n^2)
        - We have two nested loops iterating over the string,
            and a Palindrome Check of O(n), giving Cubic time complexity.

        Space Complexity: O(1)
        - We only use a constant amount of extra space for variables like maxlen, maxpal.
        """
        maxlen = 0
        maxpal = None
        for i in range(len(s)):
            for j in range(i, len(s)):
                if self.isPalindrome(s[i:j+1]):
                    if len(s[i:j+1]) > maxlen:
                        maxlen = len(s[i:j+1])
                        maxpal = s[i:j+1]
        return maxpal

    def isPalindrome(self, s: str) -> bool:
        """
        Checks if the given string s is a palindrome.

        Time Complexity: O(n)
        - We iterate through half the string, giving linear time complexity.

        Space Complexity: O(1)
        """
        if len(s) <= 1:
            return True
        for i in range(len(s)//2 + 1):
            if s[i] != s[-i-1]:
                return False
        return True

    def longestPalindromeDP(self, s: str) -> str:
        """
        Finds the longest palindrome substring in string s using dynamic programming.

        Time Complexity: O(n^2)
        - We have nested loops iterating over the string, giving quadratic time complexity.

        Space Complexity: O(n^2)
        - We use a 2D DP array of size n x n to store results, which takes quadratic space.
        """
        n = len(s)
        dp = [[False] * n for _ in range(n)]
        ans = [0, 0]

        for i in range(n):
            dp[i][i] = True

        for i in range(n - 1):
            if s[i] == s[i + 1]:
                dp[i][i + 1] = True
                ans = [i, i + 1]

        for diff in range(2, n):
            for i in range(n - diff):
                j = i + diff
                if s[i] == s[j] and dp[i + 1][j - 1]:
                    dp[i][j] = True
                    ans = [i, j]

        i, j = ans
        return s[i:j + 1]

    def expand_center(self, s: str, p: int) -> str:
        """
        Expands palindrome centered at index p in string s.

        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        i = 1
        while p - i >= 0 and p + i < len(s) and s[p - i] == s[p + i]:
            i += 1
        return s[p - i + 1:p + i]

    def expand_neighbors(self, s: str, p: int) -> str:
        """
        Expands palindrome centered between indices p and p+1 in string s.

        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        if p + 1 >= len(s) or s[p] != s[p + 1]:
            return ''

        i = 1
        while p - i >= 0 and p + 1 + i < len(s) and s[p - i] == s[p + 1 + i]:
            i += 1
        return s[p - i + 1:p + i + 1]

    def longestPalindromeManacher(self, s: str) -> str:
        """
        Finds longest palindrome substring in string s using Manacher's algorithm.
        Manacher's algorithm is a linear time algorithm that finds the longest palindrome substring in a string.
        https://cp-algorithms.com/string/manacher.html

        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        if not s:
            return ''

        best = ''
        for p in range(len(s)):
            tmp = self.expand_center(s, p)
            if len(tmp) > len(best):
                best = tmp

            tmp = self.expand_neighbors(s, p)
            if len(tmp) > len(best):
                best = tmp

        return best


if __name__ == "__main__":
    s = Solution()
    print(s.longestPalindromeDP("babad"))
    print(s.longestPalindromeDP("cbbd"))
    print(s.longestPalindromeDP("a"))
