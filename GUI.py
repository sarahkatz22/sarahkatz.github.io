from tkinter import *
import tkinter as tk
import compare

def submit():
    value1 = entry1.get()
    value2 = entry2.get()

    soup1 = compare.get_soup(value1)
    soup2 = compare.get_soup(value2)

    at_risk = compare.at_risk(soup1, soup2)
    safe = compare.safe(soup1, soup2)
    result_label.config(text=f"Safe Products: {safe}\n\nAt Risk Products: {at_risk}", wraplength=500, justify=LEFT)

window = tk.Tk()
window.title("Comaprison Calculator")

label1 = tk.Label(window, text="First Website:")
label1.grid(row=0, column=0)

entry1 = tk.Entry(window, bg='white')
entry1.grid(row=0, column=1)

label2 = tk.Label(window, text="Second Website:")
label2.grid(row=1, column=0)

entry2 = tk.Entry(window)
entry2.grid(row=1, column=1)

submit_button = tk.Button(window, text="Compare", command=submit)
submit_button.grid(row=2, column=0, columnspan=2)

result_label = tk.Label(window, text="")
result_label.grid(row=3, column=0, columnspan=2)

window.mainloop()


#"https://www.speedcubes.co.za/12-2x2x2"
#"https://cubeco.co.za/collections/2x2"







