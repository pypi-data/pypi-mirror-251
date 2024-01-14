def levenshtein_distance(string1: str, string2: str) -> int:
    # got this from chatgpt tbh
    string1_length, string2_length = len(string1), len(string2)

    dp = [[0] * (string2_length + 1) for _ in range(string1_length + 1)]

    for i in range(string1_length + 1):
        dp[i][0] = i
    for j in range(string2_length + 1):
        dp[0][j] = j

    for i in range(1, string1_length + 1):
        for j in range(1, string2_length + 1):
            cost = 0 if string1[i - 1] == string2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost,
            )

    return dp[string1_length][string2_length]
