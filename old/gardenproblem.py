def RoadNum(n):
    n = n//2
    nums = [1]*(n+1)
    if n <= 1:
        return n
    for i in range(2,n+1):
        nums[i] = 0
        for j in range(i):
            nums[i] += nums[j]*nums[i-j-1]

    return nums[i]


print(RoadNum(6))
