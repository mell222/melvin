import tkinter as tk
from tkinter import messagebox
from functools import partial
import random



class CRC:
    def __init__(self, polynomial):
        self.polynomial = polynomial

    def encode(self, data):
        # Append zeroes for padding
        padded_data = data + [0] * (len(self.polynomial) - 1)
        # Perform polynomial division
        _, remainder = self.polynomial_division(padded_data, self.polynomial)
        # Return original data with remainder appended
        return data + remainder

    def decode(self, received_data):
        # Perform polynomial division
        _, remainder = self.polynomial_division(received_data, self.polynomial)
        # If remainder contains any non-zero elements, error detected
        return any(remainder)

    def polynomial_division(self, dividend, divisor):
        # Perform polynomial division
        remainder = list(dividend)
        # While remainder length is greater or equal to divisor length
        while len(remainder) >= len(divisor):
            # Calculate next remainder
            for i in range(len(divisor)):
                remainder[i] ^= divisor[i]
            # Remove leading zeros
            while remainder and remainder[0] == 0:
                remainder.pop(0)
        # Return quotient and remainder
        return dividend[:-len(remainder)], remainder

class CRC_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CRC Encoder/Decoder")

        # Polynomial input
        self.poly_label = tk.Label(root, text="Polynomial (e.g., x^2 + 1 represented as 101):")
        self.poly_label.grid(row=0, column=0, sticky="w")
        self.poly_entry = tk.Entry(root)
        self.poly_entry.grid(row=0, column=1)

        # Data input
        self.data_label = tk.Label(root, text="Data:")
        self.data_label.grid(row=1, column=0, sticky="w")
        self.data_entry = tk.Entry(root)
        self.data_entry.grid(row=1, column=1)

        # Encode button
        self.encode_btn = tk.Button(root, text="Encode", command=self.encode_data)
        self.encode_btn.grid(row=2, column=0)

        # Decode button
        self.decode_btn = tk.Button(root, text="Decode", command=self.decode_data)
        self.decode_btn.grid(row=2, column=1)

        # Simulate errors checkbutton
        self.simulate_errors_var = tk.IntVar()
        self.simulate_errors_check = tk.Checkbutton(root, text="Simulate Errors", variable=self.simulate_errors_var)
        self.simulate_errors_check.grid(row=3, column=0, columnspan=2)

    def encode_data(self):
        polynomial = self.poly_entry.get()
        data = self.data_entry.get()
        try:
            polynomial = [int(bit) for bit in polynomial]
            data = [int(bit) for bit in data]
            crc = CRC(polynomial)
            encoded_data = crc.encode(data)
            if self.simulate_errors_var.get():
                self.simulate_errors(encoded_data)
            messagebox.showinfo("Encoded Data", "Encoded data: " + ' '.join(map(str, encoded_data)))
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter binary digits (0 or 1).")

    def decode_data(self):
        polynomial = self.poly_entry.get()
        received_data = self.data_entry.get()
        try:
            polynomial = [int(bit) for bit in polynomial]
            received_data = [int(bit) for bit in received_data]
            crc = CRC(polynomial)
            if self.simulate_errors_var.get():
                self.simulate_errors(received_data)
            error_detected = crc.decode(received_data)
            if error_detected:
                messagebox.showerror("Error", "Errors detected. Data corrupted.")
            else:
                messagebox.showinfo("Success", "No errors detected. Data intact.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter binary digits (0 or 1).")

    def simulate_errors(self, data):
        error_rate = 0.1  # Example error rate
        num_errors = random.randrange(len(data))
        print(num_errors)
        error_indices = random.sample(range(len(data)), num_errors)
        for i in error_indices:
            data[i] ^= 1
        messagebox.showinfo("Simulated Errors", f"Simulated errors at indices: {error_indices}")



if __name__ == "__main__":
    root = tk.Tk()
    gui = CRC_GUI(root)
    root.mainloop()
