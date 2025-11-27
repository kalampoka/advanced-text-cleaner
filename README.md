# Advanced Text Cleaner

The **Advanced Text Cleaner** is a high-precision text-processing tool built to aggressively clean, normalize, and sanitize raw text data.
It removes noise, fixes broken formatting, applies consistent casing rules, and prepares text for NLP pipelines, datasets, or general use.

## Features
- **Noise Removal:** Deletes special chars, weird unicode, repeated symbols, spammy patterns.  
- **Smart Whitespace Control:** Fixes double spaces, broken newlines, and messy indentation.  
- **Case Normalization:** Converts text to lower/title/sentence case based on your setting.  
- **Punctuation Correction:** Cleans duplicated punctuation and restores missing spacing.  
- **Profanity Filter:** Optional — censors or strips flagged words.  
- **Dataset-Ready Output:** Ensures stable encoding + consistent formatting.  
- **Extremely Modular:** Add or remove cleaning steps easily.

## Why Use This
Normal text cleaners only catch basic stuff.
This one goes **nuclear**, useful for:
- AI dataset prep  
- Preprocessing user input  
- Cleaning messy documents  
- Chatbot logs  
- OCR text fixes  
- Spam cleaning  

## Installation
```bash
pip install -r requirements.txt
```
## Usage
```bash
from cleaner import AdvancedTextCleaner

cleaner = AdvancedTextCleaner(
    lowercase=True,
    fix_spacing=True,
    remove_unicode_noise=True,
    filter_profanity=True
)

output = cleaner.clean("Your messy text here...")
print(output)
