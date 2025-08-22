import json
import os
from datetime import datetime

class Calculator:
    def _init_(self, history_file="calc_history.json"):
        self.history_file = history_file
        self.history = self.load_history()
        self.last_result = None

    def load_history(self):
        """Load calculation history from JSON file."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return []
        return []

    def save_history(self, operation, num1, num2, result):
        """Save calculation to history."""
        entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'num1': num1,
            'num2': num2,
            'operation': operation,
            'result': result
        }
        self.history.append(entry)
        try:
            with open(self.history_file, 'w') as file:
                json.dump(self.history, file, indent=4)
        except IOError:
            print("Error saving history.")

    def view_history(self):
        """Display calculation history."""
        if not self.history:
            print("No history available.")
            return
        print("\nCalculation History:")
        for i, entry in enumerate(self.history, 1):
            print(f"{i}. {entry['timestamp']}: {entry['num1']} {entry['operation']} {entry['num2']} = {entry['result']}")

    def get_last_result(self):
        """Return the last calculation result."""
        return self.last_result if self.last_result is not None else 0

    def validate_number(self, value):
        """Validate if input is a number or 'last' for last result."""
        if value.lower() == 'last':
            return self.get_last_result()
        try:
            return float(value)
        except ValueError:
            raise ValueError("Invalid number input. Please enter a number or 'last'.")

    def calculate(self, num1, num2, operation):
        """Perform the calculation based on the operation."""
        operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y if y != 0 else None,
            '': lambda x, y: x ** y,
            '%': lambda x, y: x % y if y != 0 else None,
            '//': lambda x, y: x // y if y != 0 else None
        }
        if operation not in operations:
            return "Error: Invalid operation. Use +, -, *, /, **, %, or //."
        if operation in ['/', '%', '//'] and num2 == 0:
            return "Error: Cannot divide by zero."
        result = operations[operation](num1, num2)
        self.last_result = result
        self.save_history(operation, num1, num2, result)
        return f"Result: {result}"

def main():
    calc = Calculator()
    valid_operations = ['+', '-', '', '/', '*', '%', '//']

    while True:
        print("\nAdvanced Calculator")
        print("Operations: +, -, *, /, ** (exponent), % (modulus), // (floor division)")
        print("1. Perform Calculation")
        print("2. View History")
        print("3. Exit")

        choice = input("Enter choice (1-3): ").strip()

        if choice == '1':
            try:
                num1_input = input("Enter first number (or 'last' for last result): ").strip()
                num1 = calc.validate_number(num1_input)
                num2_input = input("Enter second number (or 'last' for last result): ").strip()
                num2 = calc.validate_number(num2_input)
                operation = input("Choose operation (+, -, *, /, **, %, //): ").strip()
                if operation not in valid_operations:
                    print("Error: Invalid operation. Use +, -, *, /, **, %, or //.")
                    continue
                result = calc.calculate(num1, num2, operation)
                print(result)
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '2':
            calc.view_history()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
