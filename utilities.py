
from datetime import datetime
            
class Utilities:
    def __init__(self, number):
        self.number = number

    def get_item_number(self, prefix_format=''):
        return f"{prefix_format}-{str(self.number).zfill(3)}"

    def digit_to_word_indian(self, number):
        """Convert a float number to words in the Indian numbering system with 'Rupees' and 'Paise' for currency.
        
        Args:
            number (int or float): The number to convert (0 to 100 quintillion for integer part, up to 2 decimal places for paise).
            
        Returns:
            str: The number in words (e.g., 'One Arab Twenty Five Crore Forty Two Lakh Fifty One Thousand Two Hundred Sixty Rupees and Fifty Paise only').
            
        Raises:
            ValueError: If the number is out of range or has more than 2 decimal places.
        """
        # Validate input
        if not isinstance(number, (int, float)) or number < 0 or number > 100000000000000000000:
            return "Number out of range (0 to 100 quintillion)"

        # Split integer and decimal parts
        integer_part = int(number)
        decimal_part = 0
        if isinstance(number, float):
            # Convert decimal to paise (multiply by 100 and round to integer)
            decimal_str = str(number).split('.')
            if len(decimal_str) > 1 and len(decimal_str[1]) > 2:
                return "Number has more than 2 decimal places"
            decimal_part = round((number - integer_part) * 100)

        # Arrays for words
        units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
        teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", 
                 "Seventeen", "Eighteen", "Nineteen"]
        tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
        thousands = ["", "Thousand", "Lakh", "Crore", "Arab", "Kharab", "Neel", "Padma", "Shankh"]

        def convert_less_than_thousand(num):
            """Convert numbers less than 1000 to words."""
            if num == 0:
                return ""
            elif num < 10:
                return units[num]
            elif num < 20:
                return teens[num - 10]
            elif num < 100:
                return tens[num // 10] + (" " + units[num % 10] if num % 10 != 0 else "")
            else:
                return units[num // 100] + " Hundred" + (" " + convert_less_than_thousand(num % 100) if num % 100 != 0 else "")

        def convert_integer_part(num):
            """Convert the integer part to words."""
            if num == 0:
                return "Zero"
            
            # Break number into groups for Indian system: first 3 digits, then pairs
            groups = []
            if num >= 1000:
                groups.append(num % 1000)
                num //= 1000
            while num > 0:
                groups.append(num % 100)
                num //= 100

            result = []
            for i, group in enumerate(groups):
                if group != 0:
                    if i == 0:
                        word = convert_less_than_thousand(group)
                    else:
                        if group < 10:
                            word = units[group]
                        elif group < 20:
                            word = teens[group - 10]
                        else:
                            word = tens[group // 10] + (" " + units[group % 10] if group % 10 != 0 else "")
                    result.append(word + (" " + thousands[i] if thousands[i] else ""))
            
            if not result:
                return "Zero"
            
            return " ".join(reversed(result)).strip()

        # Convert integer part
        integer_words = convert_integer_part(integer_part)
        result = integer_words + " Rupees"

        # Convert decimal part (paise)
        if decimal_part > 0:
            if decimal_part < 10:
                paise_words = units[decimal_part]
            elif decimal_part < 20:
                paise_words = teens[decimal_part - 10]
            else:
                paise_words = tens[decimal_part // 10] + (" " + units[decimal_part % 10] if decimal_part % 10 != 0 else "")
            result += f" and {paise_words} Paise"

        # Add 'only' suffix
        result += " only"
        
        return result

if __name__ == "__main__":
    try:
        util = Utilities()
        # Example usage of digit_to_word_indian with float and integer numbers
        test_numbers = [12540325,13640235]
        for num in test_numbers:
            print(f"{num}: {util.digit_to_word_indian(num)}")
    except ValueError as e:
        print(f"Error: {e}")