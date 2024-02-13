import PyPDF2
import tkinter as tk
from tkinter import filedialog

# Function to check if the PDF file is encrypted
def is_pdf_encrypted(file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            return pdf_reader.is_encrypted
    except Exception as e:
        print("Error:", e)
        return False

# Function to try opening the PDF file with a given PIN
def try_opening_pdf(file_path, pin):
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            if pdf_reader.decrypt(pin):
                return True
            else:
                return False
    except Exception as e:
        print("Error:", e)
        return False

# Function to handle file selection
def choose_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    print('Selected file:', file_path)
    return file_path

# Function to generate next PIN combination
def next_pin(pin):
    if not pin:  # If pin is empty, return '1'
        return '1'
    
    carry = 1
    new_pin = ''
    for digit in pin[::-1]:
        new_digit = (int(digit) + carry) % 10
        carry = (int(digit) + carry) // 10
        new_pin = str(new_digit) + new_pin
    if carry:
        new_pin = str(carry) + new_pin
    return new_pin.zfill(len(pin))  # Ensure the new PIN has the same length as the input PIN

# Main function
def main():
    file_path = choose_file()  # Prompt user to choose the PDF file
    if not file_path:
        print("No file selected.")
        return

    if not is_pdf_encrypted(file_path):
        print("The PDF file is not encrypted. No need to try PINs.")
        return

    pin = ''
    correct_pin = None
    pin_length = 1

    print('before while loop 1')
    while True:
        print('started while loop 1')
        pin = '0' * pin_length
        while pin != '1' + '0' * (pin_length - 1):
            print("Trying PIN:", pin)
            if try_opening_pdf(file_path, pin):
                correct_pin = pin
                break
            pin = next_pin(pin)
        if correct_pin:
            break
        pin_length += 1

    # Print the correct PIN if found
    if correct_pin:
        print("Correct PIN found:", correct_pin)
    else:
        print("Unable to open the PDF file with any PIN.")

if __name__ == "__main__":
    main()
