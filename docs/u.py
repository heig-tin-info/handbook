def fib_calls(n):
    if n <= 1:
        return n, 1

    # Initial conditions for Fibonacci and call counts
    fib_n_minus_2, calls_n_minus_2 = 0, 1
    fib_n_minus_1, calls_n_minus_1 = 1, 1

    for i in range(2, n + 1):
        fib_n = fib_n_minus_1 + fib_n_minus_2
        calls_n = calls_n_minus_1 + calls_n_minus_2 + 1

        # Update for the next iteration
        fib_n_minus_2, calls_n_minus_2 = fib_n_minus_1, calls_n_minus_1
        fib_n_minus_1, calls_n_minus_1 = fib_n, calls_n

    return fib_n, calls_n

# Example usage:
n = 10
fib_value, total_calls = fib_calls(n)
print(f"fib({n}) = {fib_value}, total calls = {total_calls}")