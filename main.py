import string
import getpass
import msvcrt
import zxcvbn
import os
import sys
from datetime import datetime

# Hardcoded a list of common passwords
common_passwords = [
    "password", "123456", "12345678", "1234", "qwerty", "12345", "dragon", "pussy", "baseball", 
    "football", "letmein", "monkey", "696969", "abc123", "mustang", "michael", "shadow", "master", 
    "jennifer", "111111", "2000", "jordan", "superman", "harley", "1234567"
]

# Guidelines for password strength
guidelines = {
    'min_length': 12,  # Minimum password length updated to 12 characters
    'uppercase': 1,    # Minimum number of uppercase letters
    'lowercase': 1,    # Minimum number of lowercase letters
    'digits': 1,       # Minimum number of digits
    'special_chars': 1 # Minimum number of special characters
}

def check_pwd(password):
    results = {
        'length': len(password),
        'uppercase': sum(1 for char in password if char.isupper()),
        'lowercase': sum(1 for char in password if char.islower()),
        'digits': sum(1 for char in password if char.isdigit()),
        'special_chars': sum(1 for char in password if char in string.punctuation)
    }

    # Use zxcvbn to estimate password strength
    result = zxcvbn.zxcvbn(password)
    score = result['score']
    suggestions = result['feedback']['suggestions']

    # Check against each guideline
    guideline_results = {
        'min_length': results['length'],
        'uppercase': results['uppercase'],
        'lowercase': results['lowercase'],
        'digits': results['digits'],
        'special_chars': results['special_chars']
    }

    for key, value in guidelines.items():
        if guideline_results[key] < value:
            suggestions.append(get_guideline_message(key, value))

    if not suggestions and score >= 3:
        suggestions.append("This password is acceptable and secure!")

    # Custom security checks for common passwords
    for common_pw in common_passwords:
        if common_pw.lower() in password.lower():
            suggestions.append(f"Password contains common password elements: {common_pw}. Avoid common passwords.")

    # Generate strength remarks based on zxcvbn score
    remarks = ["Very Weak Password", "Weak Password", "Fair Password", "Good Password", "Strong Password", "Very Strong Password"][score]
    
    return score, remarks, suggestions

def get_guideline_message(key, value):
    messages = {
        'min_length': f"Increase password length to at least {value} characters.",
        'uppercase': f"Add at least {value} uppercase letter(s).",
        'lowercase': f"Add at least {value} lowercase letter(s).",
        'digits': f"Include at least {value} digit(s).",
        'special_chars': f"Include at least {value} special character(s) (e.g., !, @, #, $)."
    }
    return messages[key]

def get_password_input():
    print("Enter Password: ", end="", flush=True)
    password = ""
    while True:
        char = msvcrt.getch()
        if char == b'\r':
            print()
            break
        elif char == b'\x08':
            if len(password) > 0:
                password = password[:-1]
                print("\b \b", end="", flush=True)
        else:
            password += char.decode("utf-8")
            print("*", end="", flush=True)
    return password

def ask_pwd():
    while True:
        password = get_password_input()
        if len(password) < guidelines['min_length']:
            print(f"Password is too short. Please ensure it is at least {guidelines['min_length']} characters long.")
        else:
            return password

def ask_another_pwd():
    while True:
        choice = input('Do you want to enter another password? (y/n): ').lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print('Invalid entry, try again!')

def generate_report(password, score, remarks, suggestions):
    with open("password_strength_report.txt", "a") as file:
        file.write(f"Password Analysis Report - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("---------------------------------------------------------------------\n")
        file.write("NOTE: This file will be deleted automatically upon program closure. Please make a note of any important information.\n")
        file.write("---------------------------------------------------------------------\n")
        file.write(f"Password Tested: {password}\n")
        file.write(f"Password Strength: {remarks}\n")
        file.write("Recommendations:\n")
        for suggestion in suggestions:
            file.write(f"- {suggestion}\n")
        file.write("\n\n")

def open_report():
    report_path = "password_strength_report.txt"
    try:
        if os.name == 'nt':  # For Windows
            os.system(f'start {report_path}')
        elif os.name == 'posix':  # For macOS and Linux
            opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
            os.system(f'{opener} {report_path}')
    except Exception as e:
        print(f"Failed to open the report automatically: {e}")

if __name__ == '__main__':
    print('+++ Welcome to the Password Strength Evaluator and Report Generator +++')
    try:
        while True:
            password = ask_pwd()
            score, remarks, suggestions = check_pwd(password)
            print("Processing your report...")
            generate_report(password, score, remarks, suggestions)
            print("Report has been generated and saved to 'password_strength_report.txt'.")
            open_report()
            if not ask_another_pwd():
                break
    finally:
        try:
            os.remove("password_strength_report.txt")
            print("Temporary report file deleted for security.")
        except FileNotFoundError:
            print("No report file found to delete.")
