def count_up_to(n):
    for i in range(1, n + 1):
        yield i  # pause here and return i


gen = count_up_to(3)

print(next(gen))
print(next(gen))
