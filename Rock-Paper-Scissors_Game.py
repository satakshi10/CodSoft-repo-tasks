import random
import time

def clear_screen():
    """Clear the screen for better user experience."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def print_with_delay(text, delay=0.03):
    """Print text with a typing effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def get_user_choice():
    """Get the user's choice for rock, paper, or scissors with improved user experience."""
    print("\n" + "🎯" * 20)
    print("🎮 YOUR TURN! Make your choice:")
    print("🎯" * 20)
    print("💡 Quick Tips:")
    print("   • Type just 'r' for Rock 🪨")
    print("   • Type just 'p' for Paper 📄") 
    print("   • Type just 's' for Scissors ✂️")
    print("   • Type 'quit' or 'q' to exit")
    print("🎯" * 20)
    
    while True:
        try:
            choice = input("\n🎲 Enter your choice: ").lower().strip()
            
            if choice in ['rock', 'r']:
                print("✅ You chose: 🪨 ROCK!")
                return 'rock'
            elif choice in ['paper', 'p']:
                print("✅ You chose: 📄 PAPER!")
                return 'paper'
            elif choice in ['scissors', 's']:
                print("✅ You chose: ✂️ SCISSORS!")
                return 'scissors'
            elif choice in ['quit', 'q', 'exit']:
                print("👋 Thanks for playing!")
                return None
            else:
                print("❌ Oops! I didn't understand that.")
                print("💡 Please try: 'r' (rock), 'p' (paper), 's' (scissors), or 'quit'")
                print("   You can also type the full word like 'rock', 'paper', 'scissors'")
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Game interrupted. Thanks for playing!")
            return None

def get_computer_choice():
    """Generate a random choice for the computer with dramatic reveal."""
    choices = ['rock', 'paper', 'scissors']
    choice = random.choice(choices)
    
    # Add suspense
    print("\n🤖 Computer is thinking...")
    time.sleep(0.8)
    print("🎲 Computer is making its choice...")
    time.sleep(0.5)
    
    return choice

def determine_winner(user_choice, computer_choice):
    """Determine the winner based on game rules."""
    if user_choice == computer_choice:
        return "tie"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "scissors" and computer_choice == "paper") or \
         (user_choice == "paper" and computer_choice == "rock"):
        return "user"
    else:
        return "computer"

def display_result(user_choice, computer_choice, result):
    """Display the choices and result with enhanced visual appeal."""
    # Create dramatic countdown
    print("\n🥁 And the results are...")
    time.sleep(0.5)
    print("3...")
    time.sleep(0.4)
    print("2...")
    time.sleep(0.4)
    print("1...")
    time.sleep(0.4)
    print("🎊 REVEAL! 🎊")
    time.sleep(0.3)
    
    # Map choices to emojis
    emoji_map = {
        'rock': '🪨',
        'paper': '📄',
        'scissors': '✂️'
    }
    
    user_emoji = emoji_map[user_choice]
    computer_emoji = emoji_map[computer_choice]
    
    # Display choices with visual appeal
    print("\n" + "=" * 40)
    print(f"   {user_emoji} YOU:      {user_choice.upper()}")
    print("   🆚")
    print(f"   {computer_emoji} COMPUTER: {computer_choice.upper()}")
    print("=" * 40)
    
    # Announce result with appropriate celebration
    if result == "tie":
        print("🤝 IT'S A TIE! Great minds think alike!")
        print("🔄 Nobody gets a point this round.")
    elif result == "user":
        print("🎉🎊 CONGRATULATIONS! YOU WIN! 🎊🎉")
        print(f"✨ {user_choice.capitalize()} beats {computer_choice.capitalize()}!")
        print("⭐ +1 point for you!")
    else:
        print("🤖 COMPUTER WINS THIS ROUND!")
        print(f"💻 {computer_choice.capitalize()} beats {user_choice.capitalize()}!")
        print("🔧 +1 point for computer!")
    
    print("=" * 40)

def display_score(user_score, computer_score):
    """Display the current score with visual progress bars."""
    total_rounds = user_score + computer_score
    
    print(f"\n📊 SCOREBOARD 📊")
    print("=" * 30)
    
    # Create visual score bars
    if total_rounds > 0:
        user_percentage = (user_score / total_rounds) * 100
        computer_percentage = (computer_score / total_rounds) * 100
        
        # Create progress bars (20 characters wide)
        user_bar = "█" * int(user_percentage / 5) + "░" * (20 - int(user_percentage / 5))
        computer_bar = "█" * int(computer_percentage / 5) + "░" * (20 - int(computer_percentage / 5))
        
        print(f"👤 YOU:      [{user_bar}] {user_score} ({user_percentage:.1f}%)")
        print(f"🤖 COMPUTER: [{computer_bar}] {computer_score} ({computer_percentage:.1f}%)")
    else:
        print(f"👤 YOU:      [░░░░░░░░░░░░░░░░░░░░] {user_score}")
        print(f"🤖 COMPUTER: [░░░░░░░░░░░░░░░░░░░░] {computer_score}")
    
    print("=" * 30)
    
    # Show current status
    if user_score > computer_score:
        print("🔥 You're in the LEAD! Keep it up!")
    elif computer_score > user_score:
        print("😤 Computer is ahead! Time for a comeback!")
    else:
        print("⚖️ It's perfectly TIED! Neck and neck!")

def play_again():
    """Ask if the user wants to play another round with friendly prompts."""
    print("\n" + "🎮" * 15)
    while True:
        try:
            again = input("🔄 Ready for another round? (y/yes or n/no): ").lower().strip()
            if again in ['yes', 'y', 'yeah', 'yep', 'sure']:
                print("🚀 Awesome! Let's keep playing!")
                return True
            elif again in ['no', 'n', 'nope', 'nah']:
                print("👍 Got it! Let's see the final results...")
                return False
            else:
                print("💭 I didn't catch that! Please type:")
                print("   • 'y' or 'yes' to continue playing")
                print("   • 'n' or 'no' to finish the game")
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Game interrupted. Let's finish up!")
            return False

def show_welcome():
    """Display an attractive welcome screen."""
    clear_screen()
    
    welcome_text = """
🎮🎊🎮🎊🎮🎊🎮🎊🎮🎊🎮🎊🎮🎊🎮🎊🎮🎊🎮🎊🎮🎊🎮🎊🎮
🎊                                              🎊
🎮       🪨 📄✂️  ROCK PAPER SCISSORS ✂️ 📄🪨       🎮
🎊                                              🎊
🎮              THE ULTIMATE SHOWDOWN!          🎮
🎊                                              🎊
🎮🎊🎮🎊🎮🎊🎮🎊🎮🎊🎮🎊🎮🎊🎮🎊🎮🎊🎮🎊🎮🎊🎮🎊🎮
"""
    
    print_with_delay(welcome_text, 0.01)
    time.sleep(0.5)
    
    print("🎯 GAME RULES - Simple and Fun!")
    print("=" * 45)
    print("🪨 ROCK crushes ✂️ SCISSORS")
    print("✂️ SCISSORS cuts 📄 PAPER") 
    print("📄 PAPER covers 🪨 ROCK")
    print("=" * 45)
    
    print("\n💡 QUICK CONTROLS:")
    print("   • Press 'r' for 🪨 Rock")
    print("   • Press 'p' for 📄 Paper")
    print("   • Press 's' for ✂️ Scissors")
    print("   • Type 'quit' anytime to exit")
    
    print("\n🌟 Ready to test your luck and strategy?")
    input("🚀 Press ENTER to start the game! ")

def main():
    """Main game function with enhanced user experience."""
    show_welcome()
    
    user_score = 0
    computer_score = 0
    round_number = 0
    
    while True:
        round_number += 1
        
        # Round header
        clear_screen()
        print(f"🎮 ROUND {round_number} 🎮".center(50))
        print("🔥" * 50)
        
        # Show current score if not first round
        if round_number > 1:
            display_score(user_score, computer_score)
        
        # Get user choice
        user_choice = get_user_choice()
        if user_choice is None:  # User chose to quit
            break
        
        # Get computer choice
        computer_choice = get_computer_choice()
        
        # Determine winner
        result = determine_winner(user_choice, computer_choice)
        
        # Update scores
        if result == "user":
            user_score += 1
        elif result == "computer":
            computer_score += 1
        
        # Display result
        display_result(user_choice, computer_choice, result)
        
        # Display updated score
        display_score(user_score, computer_score)
        
        # Ask if user wants to play again
        if not play_again():
            break
    
    # Final score summary with celebration
    show_final_results(user_score, computer_score, round_number)

def show_final_results(user_score, computer_score, total_rounds):
    """Display final results with celebration."""
    clear_screen()
    
    print("🎊" * 50)
    print("🏆           FINAL RESULTS           🏆".center(50))
    print("🎊" * 50)
    
    # Display final scores with visual bars
    display_score(user_score, computer_score)
    
    # Determine overall winner and show appropriate message
    if total_rounds == 1:
        print("\n🎮 Thanks for trying the game!")
    elif user_score > computer_score:
        print("\n🎉🎊🎉 VICTORY CELEBRATION! 🎉🎊🎉")
        print("🏆 YOU ARE THE CHAMPION! 🏆")
        print("✨ Outstanding performance!")
        if user_score >= computer_score * 2:
            print("🔥 DOMINANT WIN! You crushed it!")
    elif computer_score > user_score:
        print("\n🤖 COMPUTER WINS THIS BATTLE!")
        print("💪 But don't give up! Practice makes perfect!")
        print("🎯 Come back for a rematch anytime!")
    else:
        print("\n🤝 INCREDIBLE! IT'S A PERFECT TIE!")
        print("⚖️ You're evenly matched with the computer!")
        print("🎭 A draw worthy of legends!")
    
    # Show game statistics
    if total_rounds > 1:
        print(f"\n📈 GAME STATISTICS:")
        print(f"   🎮 Total Rounds Played: {total_rounds - 1}")
        win_rate = (user_score / (total_rounds - 1)) * 100 if total_rounds > 1 else 0
        print(f"   📊 Your Win Rate: {win_rate:.1f}%")
        
        if win_rate >= 70:
            print("   ⭐ Rating: EXPERT PLAYER!")
        elif win_rate >= 50:
            print("   👍 Rating: SKILLED PLAYER!")
        else:
            print("   💪 Rating: IMPROVING PLAYER!")
    
    print("\n" + "🎊" * 50)
    print("🙏 Thank you for playing! Come back soon! 🙏")
    print("🎊" * 50)
    
    # Wait before closing
    input("\n🚀 Press ENTER to exit...")

if __name__ == "__main__":
    main()