import csv
import os

class DataHandler():
    def __init__(self):
        self.session_data = []
        self.lifetime_data = []
        self.new_appends = []
        self.filename = "all_in_data.csv"
        self.header = ["Probability", "Outcome"]
        self.autosave_count = 10


    def ensure_file_exists(self, filename):
        if not os.path.exists(filename):
            print(f"New {filename} file with headers created.")
            with open(filename, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.header)


    def update_lifetime_data(self):
        self.lifetime_data.extend(self.session_data)
        self.clear_sesh_data()
        print(f"lifetime data: {self.lifetime_data}")


    def load_lifetime_data(self):
        try:
            with open(self.filename, "r") as f:
                reader = csv.reader(f)
                next(reader)
                self.lifetime_data = [(float(row[0]), row[1]) for row in reader]
        except FileNotFoundError:
            print(f"File {f} not found. Starting with empty data.")
        except StopIteration:
            print("File has no data.")
            return []
        return self.lifetime_data


    def add_entry(self, probability, outcome_str):
        self.session_data.append((probability, outcome_str))
        self.new_appends.append((probability, outcome_str))
        if len(self.new_appends) == self.autosave_count:
            self.autosave(self.filename)
            print(f"New appends autosaved to {self.filename}.")

        print(f"Saved: Probability={probability}, Outcome={outcome_str}")
        print(f"Session data: {self.session_data}\nNew appends: {self.new_appends}")


    def autosave(self, filename):
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.new_appends)
            self.new_appends.clear()


    def undo_autosave(self, filename, num_entries):
        last_entries = self.get_and_remove_last_entries(filename, num_entries)
        self.new_appends.extend(last_entries)


    def get_and_remove_last_entries(self, filename, num_entries):
        last_entries = []
        updated_rows = []

        with open(filename, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
            if len(rows) <= num_entries:
                last_entries = rows[1:]
                updated_rows = rows[:1]
            else:
                last_entries = rows[-num_entries:]
                updated_rows = rows[:-num_entries]
            
        with open(filename, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(updated_rows)
        
        return last_entries
    
    
    def get_lifetime_data(self):
        return self.lifetime_data
    

    def get_sesh_data(self):
        return self.session_data
    

    def get_new_appends(self):
        return self.new_appends


    def clear_sesh_data(self):
        self.session_data.clear()
        print("Session data cleared.")

    
    def clear_new_appends(self):
        self.new_appends.clear()
        print("New appends cleared.")


    def clear_csv(self, filename):
        with open(self.filename, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.header)


    def remove_most_recent(self): 
        self.session_data.pop()
        if self.new_appends:
            self.new_appends.pop()    
        
        print(f"Session data after remove: {self.session_data}")
        print(f"New appends after remove: {self.new_appends}")
        
