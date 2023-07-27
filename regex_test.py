import unittest
from preprocessing import redact_personal_information

class TestRegex(unittest.TestCase):

    def test_email(self):
        """Tests that the function can redact an email address."""
        text = "My email address is johndoe@example.com."
        redacted_text = redact_personal_information(text)
        self.assertEqual(redacted_text, "My email address is REDACTED.")
    
    def test_email_with_multiple_dots(self):
        """Tests that an email with multiple dots can be correctly redacted."""
        text = "My email address is johndoe@example.co.za."
        redacted_text = redact_personal_information(text)
        self.assertEqual(redacted_text, "My email address is REDACTED.")

    def test_telephone(self):
        """Tests that the function can redact a telephone number."""
        text = "My phone number is 123-456-7890."
        redacted_text = redact_personal_information(text)
        self.assertEqual(redacted_text, "My phone number is REDACTED.")
    
    def test_phone_number_with_national_prefix(self):
        """Tests that a phone number with the national prefix can be correctly redacted."""
        text = "My phone number is 021 123 4567."
        redacted_text = redact_personal_information(text)
        self.assertEqual(redacted_text, "My phone number is REDACTED.")
    
    def test_phone_number_without_national_prefix(self):
        """Tests that a phone number without the national prefix can be correctly redacted."""
        text = "My phone number is 21-123-4567."
        redacted_text = redact_personal_information(text)
        self.assertEqual(redacted_text, "My phone number is REDACTED.")
    
    def test_phone_number_with_international_prefix(self):
        """Tests that a phone number with the international prefix can be correctly redacted."""
        text = "My phone number is +27 21 123 4567."
        redacted_text = redact_personal_information(text)
        self.assertEqual(redacted_text, "My phone number is REDACTED.")

    def test_phone_number_with_multiple_spaces(self):
        """Tests that a phone number with multiple spaces can be correctly redacted."""
        text = "My phone number is 021 123 4567."
        redacted_text = redact_personal_information(text)
        self.assertEqual(redacted_text, "My phone number is REDACTED.")

    def test_phone_number_with_hyphens(self):
        """Tests that a phone number with hyphens can be correctly redacted."""
        text = "My phone number is 021-123-4567."
        redacted_text = redact_personal_information(text)
        self.assertEqual(redacted_text, "My phone number is REDACTED.")
        
if __name__ == "__main__":
    unittest.main()