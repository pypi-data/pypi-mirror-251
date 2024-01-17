
def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def is_odd_or_even(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

def is_prime(num):
    if num <= 1:
        return False
    elif num == 2:
        return True
    elif num % 2 == 0:
        return False
    else:
        # Check for factors up to the square root of the number
        for i in range(3, int(num**0.5) + 1, 2):
            if num % i == 0:
                return False
        return True
