import time

def factorize_sync(*args):
    results = []
    for e in args:
        factors = []
        for i in range(1, e + 1):
            if e % i == 0:
                factors.append(i)
        results.append(factors)
    return results

# Тестування функції та вимірювання часу виконання
start_time = time.time()

a, b, c, d = factorize_sync(128, 255, 99999, 10651060)

end_time = time.time()
sync_time = end_time - start_time

assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

print(f"Синхронна версія виконалася за {sync_time:.4f} секунд")
print(a)
print(b)
print(c)
print(d)
