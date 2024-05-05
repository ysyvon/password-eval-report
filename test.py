import unittest
from main import check_pwd 

class TestPasswordStrengthChecker(unittest.TestCase):

    def test_password_length(self):
        """Test password length check."""
        _, _, suggestions = check_pwd("short")
        self.assertTrue(any("Increase password length to at least 12 characters." in s for s in suggestions))

    def test_uppercase_requirement(self):
        """Test detection of missing uppercase characters."""
        _, _, suggestions = check_pwd("alllowercase1!")
        self.assertTrue(any("Add at least 1 uppercase letter(s)." in s for s in suggestions))

    def test_digit_requirement(self):
        """Test detection of missing digits."""
        _, _, suggestions = check_pwd("NoDigitsHere!")
        self.assertTrue(any("Include at least 1 digit(s)." in s for s in suggestions))

    def test_special_char_requirement(self):
        """Test detection of missing special characters."""
        _, _, suggestions = check_pwd("NoSpecials1")
        self.assertTrue(any("Include at least 1 special character(s) (e.g., !, @, #, $)." in s for s in suggestions))

    def test_common_passwords(self):
        """Test detection of common passwords."""
        _, _, suggestions = check_pwd("password")  
        expected_message = "Password contains common password elements: password. Avoid common passwords."
        self.assertTrue(any(expected_message in s for s in suggestions),
                        f"Expected a warning about common passwords in suggestions, got {suggestions}")

if __name__ == '__main__':
    unittest.main()
