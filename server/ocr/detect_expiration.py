import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re
from datetime import datetime

def detect_expiration_date(image_path):
    # Open image and preprocess
    image = Image.open(image_path)
    image = image.convert('L')  # Convert to grayscale
    image = image.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    text = pytesseract.image_to_string(image)

    # Keywords related to expiration date
    expiration_keywords = ['exp', 'expiry', 'use by', 'best before', 'expiration']

    # Regular expression to find dates in multiple formats
    date_patterns = [
        r'\b(\d{2}[./-]?\d{2}[./-]?\d{2,4})\b',  # Matches 01/01/24 or 01.01.2024
        r'\b(\d{2}\s\w+\s\d{2,4})\b',  # Matches 01 January 2024
        r'\b(\d{4}[./-]?\d{2}[./-]?\d{2})\b',  # Matches 2024/01/01 or 2024-01-01
    ]

    # Search for expiration-related keywords in the text
    for keyword in expiration_keywords:
        if keyword.lower() in text.lower():
            print(f"Found keyword: {keyword}")  # Debugging: keyword found

            # Extract text after the keyword and search for dates in that section
            keyword_position = text.lower().find(keyword.lower())
            text_after_keyword = text[keyword_position:]

            # Search for dates only after the keyword
            for pattern in date_patterns:
                matches = re.findall(pattern, text_after_keyword)
                if matches:
                    print(f"Found matches after '{keyword}': {matches}")  # Debugging: list of detected dates
                    for date_str in matches:
                        # Try parsing the date in multiple formats
                        for fmt in (
                        '%d/%m/%y', '%d/%m/%Y', '%d.%m.%y', '%d.%m.%Y', '%d-%m-%y', '%d-%m-%Y', '%Y-%m-%d', '%d %B %Y'):
                            try:
                                # Parse the date and return it if it's after today's date
                                expiration_date = datetime.strptime(date_str, fmt).date()
                                print(
                                    f"Detected expiration date: {expiration_date}")  # Debugging: valid expiration date
                                return expiration_date
                            except ValueError:
                                continue

    # If no expiration date is found, return None
    return None
