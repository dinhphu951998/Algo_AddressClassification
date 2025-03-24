def longest_common_subsequence(s1, i, s2, j, length):
    if i >= len(s1) or j >= len(s2):
        return length
    if s1[i] == s2[j]:
        length += 1
        return longest_common_subsequence(s1, i + 1, s2, j + 1, length)
    return max(longest_common_subsequence(s1, i + 1, s2, j, length),
        longest_common_subsequence(s1, i, s2, j + 1, length))

def longest_common_subsequence_optimized(s1, s2):
    left = 0
    for i in range(len(s1)):
        j = i
        while j < len(s2) - 1 and s1[i] != s2[j]:
            j += 1
        if j < len(s2) and s1[i] == s2[j]:
            left += 1

    right = 0
    for j in range(len(s2)):
        i = j
        while i < len(s1) - 1 and s1[i] != s2[j]:
            i += 1
        if i < len(s1) and s1[i] == s2[j]:
            right += 1
    return max(left, right)
