"""
Simple Calculator with Basic Arithmetic Operations
Prompts user for two numbers and an operation choice.
Performs calculation and displays the result.
"""

import sys
import os

def clear_terminal():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

# Handle termcolor import with fallback
try:
    from termcolor import colored
    TERMCOLOR_AVAILABLE = True
except ImportError:
    TERMCOLOR_AVAILABLE = False
    try:
        print("termcolor module not found. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "termcolor"])
        from termcolor import colored
        TERMCOLOR_AVAILABLE = True
        print("termcolor installed successfully!")
    except Exception as e:
        print(f"Could not install termcolor: {e}")
        # Fallback function for colored output
        def colored(text, color=None, attrs=None):
            return text
        TERMCOLOR_AVAILABLE = False

class SimpleCalculator:
    """A simple calculator class with basic arithmetic operations"""
    
    def __init__(self):
        self.operations = {
            '1': ('+', 'Addition'),
            '2': ('-', 'Subtraction'), 
            '3': ('*', 'Multiplication'),
            '4': ('/', 'Division'),
            '5': ('%', 'Modulus'),
            '6': ('**', 'Power')
        }
    
    def display_menu(self):
        """Display the calculator menu"""
        if TERMCOLOR_AVAILABLE:
            print(colored("\n" + "="*50, "cyan"))
            print(colored("         SIMPLE CALCULATOR", "yellow", attrs=['bold']))
            print(colored("="*50, "cyan"))
            print(colored("Select an operation:", "green"))
        else:
            print("\n" + "="*50)
            print("         SIMPLE CALCULATOR")
            print("="*50)
            print("Select an operation:")
        
        for key, (symbol, name) in self.operations.items():
            if TERMCOLOR_AVAILABLE:
                print(colored(f"  {key}. {name} ({symbol})", "white"))
            else:
                print(f"  {key}. {name} ({symbol})")
        
        if TERMCOLOR_AVAILABLE:
            print(colored("  7. Exit", "red"))
            print(colored("="*50, "cyan"))
        else:
            print("  7. Exit")
            print("="*50)
    
    def get_number(self, prompt):
        """Get a valid number from user input"""
        while True:
            try:
                if TERMCOLOR_AVAILABLE:
                    user_input = input(colored(prompt, "cyan"))
                else:
                    user_input = input(prompt)
                return float(user_input)
            except ValueError:
                if TERMCOLOR_AVAILABLE:
                    print(colored("❌ Invalid input! Please enter a valid number.", "red"))
                else:
                    print("❌ Invalid input! Please enter a valid number.")
    
    def get_operation_choice(self):
        """Get operation choice from user"""
        while True:
            if TERMCOLOR_AVAILABLE:
                choice = input(colored("Enter your choice (1-7): ", "yellow"))
            else:
                choice = input("Enter your choice (1-7): ")
            
            if choice in self.operations or choice == '7':
                return choice
            else:
                if TERMCOLOR_AVAILABLE:
                    print(colored("❌ Invalid choice! Please select 1-7.", "red"))
                else:
                    print("❌ Invalid choice! Please select 1-7.")
    
    def add(self, a, b):
        """Addition operation"""
        return a + b
    
    def subtract(self, a, b):
        """Subtraction operation"""
        return a - b
    
    def multiply(self, a, b):
        """Multiplication operation"""
        return a * b
    
    def divide(self, a, b):
        """Division operation with zero division handling"""
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed!")
        return a / b
    
    def modulus(self, a, b):
        """Modulus operation with zero division handling"""
        if b == 0:
            raise ZeroDivisionError("Modulus by zero is not allowed!")
        return a % b
    
    def power(self, a, b):
        """Power operation"""
        return a ** b
    
    def calculate(self, num1, num2, operation):
        """Perform calculation based on operation choice"""
        try:
            if operation == '1':
                result = self.add(num1, num2)
                symbol = '+'
            elif operation == '2':
                result = self.subtract(num1, num2)
                symbol = '-'
            elif operation == '3':
                result = self.multiply(num1, num2)
                symbol = '*'
            elif operation == '4':
                result = self.divide(num1, num2)
                symbol = '/'
            elif operation == '5':
                result = self.modulus(num1, num2)
                symbol = '%'
            elif operation == '6':
                result = self.power(num1, num2)
                symbol = '**'
            
            return result, symbol
            
        except ZeroDivisionError as e:
            if TERMCOLOR_AVAILABLE:
                print(colored(f"❌ Error: {e}", "red"))
            else:
                print(f"❌ Error: {e}")
            return None, None
        except Exception as e:
            if TERMCOLOR_AVAILABLE:
                print(colored(f"❌ An error occurred: {e}", "red"))
            else:
                print(f"❌ An error occurred: {e}")
            return None, None
    
    def display_result(self, num1, num2, symbol, result):
        """Display the calculation result"""
        if TERMCOLOR_AVAILABLE:
            print(colored("\n" + "─"*40, "blue"))
            print(colored("RESULT:", "green", attrs=['bold']))
            print(colored(f"{num1} {symbol} {num2} = {result}", "blue", attrs=['bold']))
            print(colored("─"*40, "blue"))
        else:
            print("\n" + "─"*40)
            print("RESULT:")
            print(f"{num1} {symbol} {num2} = {result}")
            print("─"*40)
    
    def run(self):
        """Main calculator loop"""
        clear_terminal()  # Clear terminal at start
        if TERMCOLOR_AVAILABLE:
            print(colored("🔢 Welcome to the Simple Calculator! 🔢", "magenta", attrs=['bold']))
        else:
            print("🔢 Welcome to the Simple Calculator! 🔢")
        
        while True:
            try:
                self.display_menu()
                
                # Get operation choice
                choice = self.get_operation_choice()
                
                # Exit option
                if choice == '7':
                    if TERMCOLOR_AVAILABLE:
                        print(colored("\n👋 Thank you for using Simple Calculator! Goodbye!", "magenta"))
                    else:
                        print("\n👋 Thank you for using Simple Calculator! Goodbye!")
                    break
                
                # Get numbers
                num1 = self.get_number("Enter the first number: ")
                num2 = self.get_number("Enter the second number: ")
                
                # Perform calculation
                result, symbol = self.calculate(num1, num2, choice)
                
                # Display result if calculation was successful
                if result is not None:
                    self.display_result(num1, num2, symbol, result)
                
                # Ask if user wants to continue
                if TERMCOLOR_AVAILABLE:
                    continue_calc = input(colored("\nDo you want to perform another calculation? (y/n): ", "yellow")).lower()
                else:
                    continue_calc = input("\nDo you want to perform another calculation? (y/n): ").lower()
                
                if continue_calc not in ['y', 'yes']:
                    if TERMCOLOR_AVAILABLE:
                        print(colored("\n👋 Thank you for using Simple Calculator! Goodbye!", "magenta"))
                    else:
                        print("\n👋 Thank you for using Simple Calculator! Goodbye!")
                    break
                    
            except KeyboardInterrupt:
                if TERMCOLOR_AVAILABLE:
                    print(colored("\n\n⚠️ Calculator interrupted by user. Goodbye!", "yellow"))
                else:
                    print("\n\n⚠️ Calculator interrupted by user. Goodbye!")
                break
            except Exception as e:
                if TERMCOLOR_AVAILABLE:
                    print(colored(f"\n❌ An unexpected error occurred: {e}", "red"))
                    print(colored("Please try again.", "yellow"))
                else:
                    print(f"\n❌ An unexpected error occurred: {e}")
                    print("Please try again.")

# Alternative simple function-based calculator
def simple_calculator():
    """Alternative simple calculator function"""
    clear_terminal()  # Clear terminal at start
    print("Simple Calculator")
    print("Available operations: +, -, *, /, %, **")
    
    try:
        # Get input from user
        num1 = float(input("Enter first number: "))
        operator = input("Enter operator (+, -, *, /, %, **): ").strip()
        num2 = float(input("Enter second number: "))
        
        # Perform calculation
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                print("Error: Division by zero!")
                return
            result = num1 / num2
        elif operator == '%':
            if num2 == 0:
                print("Error: Modulus by zero!")
                return
            result = num1 % num2
        elif operator == '**':
            result = num1 ** num2
        else:
            print("Error: Invalid operator!")
            return
        
        # Display result
        print(f"\nResult: {num1} {operator} {num2} = {result}")
        
    except ValueError:
        print("Error: Please enter valid numbers!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # You can choose which calculator to run:
    
    # Option 1: Advanced calculator with menu and colored output
    calculator = SimpleCalculator()
    calculator.run()
    
    # Option 2: Simple function-based calculator (uncomment to use instead)
    # simple_calculator()
