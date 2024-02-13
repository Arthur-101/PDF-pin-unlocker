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
    print('\n\n'+'Selected file:', file_path, '\n')
    return file_path

# Function to generate next PIN combination
def next_pin(pin_length):
    for digits in range(pin_length, pin_length + 1):
        for i in range(0, 10 ** digits):
            yield str(i).zfill(digits)


# Main function
def main():
    file_path = choose_file()
    if not file_path:
        print("No file selected.")
        return

    if not is_pdf_encrypted(file_path):
        print("The PDF file is not encrypted.")
        return

    def ask_user():
        ask = input("Do You know the length of the PIN used? (y/n) : ")
        if ask == 'y' or ask == 'Y':
            ask = True
        elif ask == 'n' or ask == 'N':
            ask = False
        else:
            print('Please enter correct choice...')
            ask_user()
        
        return ask
    
    choice = ask_user()
    
    correct_pin = None
    pin_length = 0
    
    if choice == False:
        while True:
            for pin in next_pin(pin_length):
                print("Trying PIN:", pin)
                
                if int(pin) == int('1' + '0' * pin_length) - 1:
                    pin_length += 1
                    
                if try_opening_pdf(file_path, pin):
                    correct_pin = pin
                    break
                
            if correct_pin:
                break
    
    elif choice == True:
        length = int(input("Enter the length of the PIN : "))
        if length > 0:            
            for pin in next_pin(length):
                print("Trying PIN:", pin)
                    
                if try_opening_pdf(file_path, pin):
                    correct_pin = pin
                    break
                
                if correct_pin:
                    break
            

    # Print the correct PIN if found
    if correct_pin:
        print("Correct PIN found:", correct_pin)
    else:
        print("Unable to open the PDF file with any PIN.")

if __name__ == "__main__":
    main()
