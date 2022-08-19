import tkinter


def reverse():
    # entry_box.delete('0.0', END)
    entry_box_var.set('')
    string = entry_var.get()
    entry_box_var.set(string[::-1])
    entry_var.set('')
    return


window = tkinter.Tk()
window.title('icecream')
window.geometry('+500+300')
window.grid_columnconfigure(0, minsize=200)

entry_var = tkinter.StringVar()
entry_var.set('')
entry = tkinter.Entry(window, textvariable=entry_var)
entry.grid(row=0, column=0, padx=10, pady=10)

button = tkinter.Button(window, text='[::-1]', command=reverse)
button.grid(row=1, column=0, padx=10, pady=10)

entry_box_var = tkinter.StringVar()
entry_box_var.set('')
entry_box = tkinter.Entry(window, textvariable=entry_box_var)
entry_box.grid(row=2, column=0, padx=10, pady=10)

window.mainloop()
