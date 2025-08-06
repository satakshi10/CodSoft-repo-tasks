import random
import string

def generate_password(length, include_uppercase=True, include_lowercase=True, 
                     include_digits=True, include_symbols=True):
    """
    Generate a random password with specified length and complexity.
    
    Args:
        length (int): Desired length of the password
        include_uppercase (bool): Include uppercase letters
        include_lowercase (bool): Include lowercase letters
        include_digits (bool): Include digits
        include_symbols (bool): Include special symbols
    
    Returns:
        str: Generated password
    """
    # Define character sets
    characters = ""
    
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_digits:
        characters += string.digits
    if include_symbols:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Ensure at least one character set is selected
    if not characters:
        raise ValueError("At least one character type must be selected!")
    
    # Generate password
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def get_user_preferences():
    """
    Get user preferences for password generation.
    
    Returns:
        tuple: (length, complexity_options)
    """
    print("=== Password Generator ===")
    print()
    
    # Get password length
    while True:
        try:
            length = int(input("Enter the desired password length (minimum 4): "))
            if length < 4:
                print("Password length should be at least 4 characters.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    print()
    print("Choose password complexity (you can select multiple options):")
    
    # Get complexity preferences
    include_lowercase = input("Include lowercase letters (a-z)? (y/n, default: y): ").lower()
    include_lowercase = include_lowercase != 'n'
    
    include_uppercase = input("Include uppercase letters (A-Z)? (y/n, default: y): ").lower()
    include_uppercase = include_uppercase != 'n'
    
    include_digits = input("Include digits (0-9)? (y/n, default: y): ").lower()
    include_digits = include_digits != 'n'
    
    include_symbols = input("Include special symbols (!@#$...)? (y/n, default: y): ").lower()
    include_symbols = include_symbols != 'n'
    
    # Ensure at least one option is selected
    if not any([include_lowercase, include_uppercase, include_digits, include_symbols]):
        print("At least one character type must be selected. Using default settings.")
        include_lowercase = include_uppercase = include_digits = include_symbols = True
    
    return length, (include_uppercase, include_lowercase, include_digits, include_symbols)

def assess_password_strength(password):
    """
    Assess the strength of the generated password.
    
    Args:
        password (str): The password to assess
    
    Returns:
        str: Strength assessment
    """
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Consider using at least 8 characters")
    
    # Character variety checks
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Add lowercase letters")
    
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Add uppercase letters")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Add numbers")
    
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1
    else:
        feedback.append("Add special characters")
    
    # Determine strength
    if score >= 6:
        return "Very Strong 🔒"
    elif score >= 4:
        return "Strong 💪"
    elif score >= 2:
        return "Moderate ⚠️"
    else:
        return "Weak ❌"

def main():
    """
    Main function to run the password generator application.
    """
    try:
        while True:
            # Get user preferences
            length, complexity = get_user_preferences()
            
            # Generate password
            password = generate_password(length, *complexity)
            
            # Display results
            print("\n" + "="*50)
            print("🔐 GENERATED PASSWORD 🔐")
            print("="*50)
            print(f"Password: {password}")
            print(f"Length: {len(password)} characters")
            print(f"Strength: {assess_password_strength(password)}")
            print("="*50)
            
            # Ask if user wants to generate another password
            print()
            another = input("Generate another password? (y/n): ").lower()
            if another != 'y':
                break
            print()
        
        print("\nThank you for using the Password Generator! 🔐")
        
    except KeyboardInterrupt:
        print("\n\nPassword generation cancelled.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()