import tkinter as tk

root = tk.Tk()
board_size = int(root.winfo_screenheight() * 0.75)
root.geometry(f"{board_size}x{board_size}")
root.title("Reti")

label = tk.Label(root, text="Would you like to play a game?", font=('Arial', 18))
label.pack(padx=0, pady=int(board_size * .5))

root.mainloop()