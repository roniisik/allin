import tkinter as tk
import atexit
from data_handler import*
from calc import *

class PokerApp:
    def __init__(self):
        self.data_handler = DataHandler()
        dh = self.data_handler
        atexit.register(self.cleanup)
        dh.ensure_file_exists(dh.filename)
        self.lifetime_data = dh.load_lifetime_data()
        
        # Main window setup
        self.root = tk.Tk()
        self.root.title("Poker Luck Tracker")
        self.root.geometry("400x300")
        
        #Frames
        self.topframe = tk.Frame(self.root)
        self.mid1frame = tk.Frame(self.root)
        self.mid1frame.grid_columnconfigure((0, 1), weight=1)
        self.mid1frame.grid_rowconfigure(0, weight=1)
        self.mid2frame = tk.Frame(self.root, bg="gray")
        self.mid2frame.grid_columnconfigure((0,1), weight=1)
        self.mid2frame.grid_rowconfigure(0, weight=1)
        self.botframe = tk.Frame(self.root, bg="gray")
        

        # GUI elements
        # Top
        prompt_lbl = tk.Label(self.topframe, text="Enter your probability and outcome (e.g., 0,75+):")
        prompt_lbl.pack(padx=5, pady=5)
        self.probability_entry = tk.Entry(self.topframe)
        self.probability_entry.pack(pady=5)
        self.topframe.pack(pady=10, fill="x")
        # Middle 1
        self.sub_btn = tk.Button(self.mid1frame, text="Submit", command=self.submit_data, width=10)
        self.sub_btn.grid(row=0, column=0, padx=15, pady=0, sticky="e")
        self.undo_btn = tk.Button(self.mid1frame, text="Undo", command=self.undo_data, width=5)
        self.undo_btn.grid(row=0, column=1, padx=5, pady=0, sticky="w")
        self.mid1frame.pack(pady=10, fill="both")
        # Middle 2
        self.sesh_deviation_lbl = tk.Label(self.mid2frame, text=f"Session deviation: 0", bg="gray")
        self.lifetime_deviation_lbl = tk.Label(self.mid2frame, text=f"Lifetime deviation: {calc_deviation(self.lifetime_data)}", bg="gray")
        self.lifetime_deviation_lbl.grid(row=0, column=1, sticky="nesw", padx=5)
        self.sesh_deviation_lbl.grid(row=0, column=0, sticky="nesw", padx=5)
        self.mid2frame.pack(expand=True, fill="both")
        # Bottom
        self.reset_btn = tk.Button(self.botframe, text="Reset", command=self.reset_session)
        self.sesh_total_label = tk.Label(self.botframe, text=f"Session total hands: {len(dh.get_sesh_data())}", bg="gray")
        self.lifetime_total_label = tk.Label(self.botframe, text=f"Lifetime total hands: {len(dh.get_lifetime_data())}", bg="gray")
        self.reset_btn.place(relx=1, rely=1, anchor="se", x=-10, y=-10)
        self.sesh_total_label.place(relx=0, rely=0.2, anchor="w", x=10)
        self.lifetime_total_label.place(relx=1, rely=0.2, anchor="e", x=-10)

        self.botframe.pack(fill="both", expand=True)

        # Bind Enter keys
        self.root.bind('<Return>', lambda event: self.submit_data())
        self.root.bind('<KP_Enter>', lambda event: self.submit_data())

    
    def reset_session(self):
        dh = self.data_handler
        s_data = dh.get_sesh_data()
        l_data = dh.get_lifetime_data()
        dh.update_lifetime_data()
        self.configure_deviation(s_data, self.sesh_deviation_lbl, "Session")
        self.configure_deviation(l_data, self.lifetime_deviation_lbl, "Lifetime")
        self.configure_total_hands(s_data, self.sesh_total_label, "Session")
        self.configure_total_hands(l_data, self.lifetime_total_label, "Lifetime")
        
    
    def configure_deviation(self, data, label, title):
        deviation = calc_deviation(data)
        label.configure(text=f"{title} deviation: {deviation}")


    def configure_total_hands(self, data, label, title):
        total = len(data)
        label.configure(text=f"{title} total: {total}")

    
    def undo_data(self):
        dh = self.data_handler
        s_data = dh.get_sesh_data()
        try:
            if not s_data:
                raise IndexError("No session data to undo.")
            if not dh.get_new_appends():
                dh.undo_autosave(dh.filename, dh.autosave_count)
            dh.remove_most_recent()
            self.show_custom_message("Success", "Most recent data entry was removed.")
            self.configure_deviation(s_data, self.sesh_deviation_lbl, "Session")
            self.configure_total_hands(s_data, self.sesh_total_label, "Session")
        except IndexError as e:
            self.show_custom_message("Error", e)


    def submit_data(self):
        dh = self.data_handler
        input_text = self.probability_entry.get()
        try:
            if not input_text[-1] in ['+', '-']:
                raise ValueError("Input must end with '+' for Win or '-' for Loss.")
            
            prob_text = input_text[:-1].replace(',', '.')
            outcome = input_text[-1]
            
            prob = float(prob_text)
            if not (0 <= prob <= 1):
                raise ValueError("Probability must be between 0 and 1.")
            if (prob == 1 and outcome == '-') or (prob == 0 and outcome == '+'):
                raise ValueError(f"Outcome '{outcome}' not possible for {prob}.")
            
            outcome_str = "Win" if outcome == '+' else "Loss"  
            dh.add_entry(prob, outcome_str)  # Save to data handler

            self.configure_deviation(dh.get_sesh_data(), self.sesh_deviation_lbl, "Session")
            self.configure_total_hands(dh.get_sesh_data(), self.sesh_total_label, "Session")
            self.show_custom_message("Success", f"Data saved: Probability={prob}, Outcome={outcome_str}")
            self.probability_entry.delete(0, tk.END)
        except ValueError as e:
            self.show_custom_message("Input Error", f"Invalid input: {e}")

    
    def cleanup(self):
        self.data_handler.autosave(self.data_handler.filename)
    
    
    def run(self):
        self.root.mainloop()


    def show_custom_message(self, title, message):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.transient(self.root)
        dialog.grab_set()

        # Calculate position to center the dialog on top of the root window
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        
        dialog_width = 300
        dialog_height = 150
        
        pos_x = root_x + (root_width // 2) - (dialog_width // 2)
        pos_y = root_y + (root_height // 2) - (dialog_height // 2)
        
        dialog.geometry(f"{dialog_width}x{dialog_height}+{pos_x}+{pos_y}")

        tk.Label(dialog, text=message, wraplength=250).pack(pady=20)

        def close_dialog():
            dialog.destroy()

        ok_button = tk.Button(dialog, text="OK", command=close_dialog)
        ok_button.pack(pady=10)

        dialog.bind("<Return>", lambda event: close_dialog())
        dialog.bind("<KP_Enter>", lambda event: close_dialog())