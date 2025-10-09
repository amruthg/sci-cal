#!/usr/bin/env python3
import math

MENU = """
Scientific Calculator
---------------------
1) √x        (square root)
2) x!        (factorial)
3) ln(x)     (natural log, base e)
4) x^b       (power)
5) Exiting
"""

def sqrt_x(x: float) -> float:
    if x < 0:
        raise ValueError("Square root is undefined for negative numbers.")
    return math.sqrt(x)

def factorial_x(n: int) -> int:
    if isinstance(n, float) and not n.is_integer():
        raise ValueError("Factorial is only defined for integers.")
    n = int(n)
    if n < 0:
        raise ValueError("Factorial is undefined for negative integers.")
    return math.factorial(n)

def ln_x(x: float) -> float:
    if x <= 0:
        raise ValueError("Natural log is defined only for positive numbers.")
    return math.log(x)

def power_x_b(x: float, b: float) -> float:
    # math.pow handles many edge cases (including negative bases with integer exponents)
    if x < 0 and not float(b).is_integer():
        raise ValueError("Negative base to a non-integer power is not real.")
    return math.pow(x, b)

def _input_float(prompt: str) -> float:
    return float(input(prompt).strip())

def _input_int(prompt: str) -> int:
    return int(input(prompt).strip())

def main():
    while True:
        print(MENU)
        choice = input("Choose an option (1-5): ").strip()

        try:
            if choice == "1":
                x = _input_float("Enter x: ")
                print(f"√{x} = {sqrt_x(x)}\n")
            elif choice == "2":
                n = _input_int("Enter n (integer ≥ 0): ")
                print(f"{n}! = {factorial_x(n)}\n")
            elif choice == "3":
                x = _input_float("Enter x (> 0): ")
                print(f"ln({x}) = {ln_x(x)}\n")
            elif choice == "4":
                x = _input_float("Enter base x: ")
                b = _input_float("Enter exponent b: ")
                print(f"{x}^{b} = {power_x_b(x, b)}\n")
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please select 1–5.\n")
        except ValueError as e:
            print(f"Error: {e}\n")
        except Exception as e:
            print(f"Unexpected error: {e}\n")

if __name__ == "__main__":
    main()

