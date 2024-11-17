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

    # Regular expression to find dates in multiple formats
    date_patterns = [
        r'\b(\d{2}/\d{2}/\d{4})\b',
        r'\b(\d{2}-\d{2}-\d{4})\b',
        r'\b(\d{4}-\d{2}-\d{2})\b',
        r'\b(\d{2}\s\w+\s\d{4})\b',
    ]

    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        if matches:
            for date_str in matches:
                for fmt in ('%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%d %B %Y'):
                    try:
                        expiration_date = datetime.strptime(date_str, fmt).date()
                        return expiration_date
                    except ValueError:
                        continue
    return None