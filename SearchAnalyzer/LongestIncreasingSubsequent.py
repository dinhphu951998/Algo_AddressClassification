class LongestIncreasingSubsequent:
    def process(self, A: []):
        n = len(A)
        lis = [0] * n
        for i in range(n):
            j = i - 1
            while j >= 0:
                if A[i] > A[j]:
                    lis[i] = max(lis[i], lis[j] + 1)
                j = j - 1
            if j < 0 and lis[i] == 0:
                lis[i] = 1
        return max(lis)