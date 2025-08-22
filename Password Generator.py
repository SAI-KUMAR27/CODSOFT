import random
import string
import re

class PasswordGenerator:
    def _init_(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = string.punctuation

    def check_password_strength(self, password):
        """Evaluate the strength of a password."""
        score = 0
        if len(password) >= 8:
            score += 1
        if re.search(r"[a-z]", password):
            score += 1
        if re.search(r"[A-Z]", password):
            score += 1
        if re.search(r"\d", password):
            score += 1
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            score += 1
        
        if score == 5:
            return "Strong"
        elif score >= 3:
            return "Moderate"
        else:
            return "Weak"

    def generate_password(self, length, use_lower=True, use_upper=True, use_digits=True, use_symbols=True, min_lower=1, min_upper=1, min_digits=1, min_symbols=1):
        """Generate a password with specified requirements."""
        if length < 1:
            return "Error: Password length must be at least 1"
        if length < (min_lower + min_upper + min_digits + min_symbols):
            return f"Error: Password length must be at least {min_lower + min_upper + min_digits + min_symbols} to meet minimum character requirements"

        # Build character set based on user preferences
        chars = ""
        if use_lower:
            chars += self.lowercase
        if use_upper:
            chars += self.uppercase
        if use_digits:
            chars += self.digits
        if use_symbols:
            chars += self.symbols

        if not chars:
            return "Error: At least one character set must be selected"

        # Ensure minimum requirements
        password = []
        if use_lower and min_lower > 0:
            password.extend(random.choice(self.lowercase) for _ in range(min_lower))
        if use_upper and min_upper > 0:
            password.extend(random.choice(self.uppercase) for _ in range(min_upper))
        if use_digits and min_digits > 0:
            password.extend(random.choice(self.digits) for _ in range(min_digits))
        if use_symbols and min_symbols > 0:
            password.extend(random.choice(self.symbols) for _ in range(min_symbols))

        # Fill remaining length with random characters
        remaining_length = length - len(password)
        if remaining_length > 0:
            password.extend(random.choice(chars) for _ in range(remaining_length))

        # Shuffle the password
        random.shuffle(password)
        password = ''.join(password)

        # Check strength
        strength = self.check_password_strength(password)
        return {"password": password, "strength": strength}

def main():
    generator = PasswordGenerator()
    
    while True:
        print("\nAdvanced Password Generator")
        print("1. Generate Single Password")
        print("2. Generate Multiple Passwords")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            try:
                length = int(input("Enter desired password length: "))
                if length < 1:
                    print("Error: Password length must be at least 1")
                    continue
                
                # Character set preferences
                use_lower = input("Include lowercase letters? (y/n, default y): ").strip().lower() != 'n'
                use_upper = input("Include uppercase letters? (y/n, default y): ").strip().lower() != 'n'
                use_digits = input("Include digits? (y/n, default y): ").strip().lower() != 'n'
                use_symbols = input("Include symbols? (y/n, default y): ").strip().lower() != 'n'

                # Minimum requirements
                min_lower = int(input("Minimum lowercase letters (default 1): ") or 1)
                min_upper = int(input("Minimum uppercase letters (default 1): ") or 1)
                min_digits = int(input("Minimum digits (default 1): ") or 1)
                min_symbols = int(input("Minimum symbols (default 1): ") or 1)

                result = generator.generate_password(
                    length, use_lower, use_upper, use_digits, use_symbols,
                    min_lower, min_upper, min_digits, min_symbols
                )
                
                if isinstance(result, str):
                    print(result)
                else:
                    print(f"Generated Password: {result['password']}")
                    print(f"Password Strength: {result['strength']}")
            
            except ValueError:
                print("Error: Please enter valid numbers for length and minimum requirements")
        
        elif choice == "2":
            try:
                length = int(input("Enter desired password length: "))
                num_passwords = int(input("Enter number of passwords to generate: "))
                if num_passwords < 1:
                    print("Error: Number of passwords must be at least 1")
                    continue

                # Character set preferences
                use_lower = input("Include lowercase letters? (y/n, default y): ").strip().lower() != 'n'
                use_upper = input("Include uppercase letters? (y/n, default y): ").strip().lower() != 'n'
                use_digits = input("Include digits? (y/n, default y): ").strip().lower() != 'n'
                use_symbols = input("Include symbols? (y/n, default y): ").strip().lower() != 'n'

                # Minimum requirements
                min_lower = int(input("Minimum lowercase letters (default 1): ") or 1)
                min_upper = int(input("Minimum uppercase letters (default 1): ") or 1)
                min_digits = int(input("Minimum digits (default 1): ") or 1)
                min_symbols = int(input("Minimum symbols (default 1): ") or 1)

                print("\nGenerated Passwords:")
                for i in range(num_passwords):
                    result = generator.generate_password(
                        length, use_lower, use_upper, use_digits, use_symbols,
                        min_lower, min_upper, min_digits, min_symbols
                    )
                    if isinstance(result, str):
                        print(result)
                        break
                    print(f"{i+1}. {result['password']} (Strength: {result['strength']})")
            
            except ValueError:
                print("Error: Please enter valid numbers for length and number of passwords")
        
        elif choice == "3":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()