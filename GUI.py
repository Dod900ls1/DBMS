from db import Database
import os
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv
import re


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.db = Database('database.sqlite3')
        self.window.geometry('300x500')

        # Create GUI elements here
        buttons = [
            ('Add Record', self.add_record, '#FF5C5C'),
            ('Update Record', self.update_record, '#FFB647'),
            ('Delete Record', self.delete_record, 'black'),
            ('Search Records', self.search_records, '#52DF6F'),
            ('Sort Records', self.sort_records, '#00008B'),
            ('Show All Records', self.show_all_records, '#A85CC4'),
            ('Create Printable Document', self.create_printable_document, '#795548'),
            ('Import CSV', self.import_csv, '#00bcd4'),
            ('Export CSV', self.export_csv, '#2196F3'),
            ('Exit', self.exit_app, '#9E9E9E')
        ]

        for text, command, color in buttons:
            button = tk.Button(self.window, text=text, command=command, font=('Helvetica', 14),
                               fg='white', bg=color, borderwidth=2, relief='groove')
            button.pack()

        self.window.mainloop()

    def exit_app(self):
        self.window.destroy()

    def import_csv(self):
        file_path = filedialog.askopenfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])
        if file_path:
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header row
                for row in reader:
                    name, model, memory, camera = row
                    self.db.execute_query(f"INSERT INTO records (name, model, memory, camera) VALUES (?, ?, ?, ?)",
                                          (name, model, memory, camera))
            print("Data imported successfully.")

    def export_csv(self):
        file_path = tk.filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])
        if file_path:
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Model', 'Memory', 'Camera'])  # Write header row
                for row in self.db.execute_query("SELECT name, model, memory, camera FROM records"):
                    writer.writerow(row)
            print("Data exported successfully.")

    def add_record(self):
        # Create a new window for input
        input_window = tk.Toplevel(self.window)

        # Create labels and entry widgets for each field in the record
        name_label = tk.Label(input_window, text='Name')
        name_entry = tk.Entry(input_window)
        name_label.grid(row=0, column=0)
        name_entry.grid(row=0, column=1)

        model_label = tk.Label(input_window, text='Model')
        model_entry = tk.Entry(input_window)
        model_label.grid(row=1, column=0)
        model_entry.grid(row=1, column=1)

        memory_label = tk.Label(input_window, text='Memory')
        memory_entry = tk.Entry(input_window)
        memory_label.grid(row=2, column=0)
        memory_entry.grid(row=2, column=1)

        camera_label = tk.Label(input_window, text='Camera')
        camera_entry = tk.Entry(input_window)
        camera_label.grid(row=3, column=0)
        camera_entry.grid(row=3, column=1)

        # Create a button to submit the input
        submit_button = tk.Button(input_window, text='Add Record',
                                  command=lambda: self.submit_record(name_entry.get(), model_entry.get(),
                                                                     memory_entry.get(), camera_entry.get(),
                                                                     input_window))
        submit_button.grid(row=4, column=0, columnspan=2)

    def submit_record(self, name, model, memory, camera, input_window):
        # Add "GB" to the memory field if it doesn't already have it
        if not memory.endswith('GB'):
            memory += 'GB'

        # Add "MP" to the camera field if it doesn't already have it
        if not camera.endswith('MP'):
            camera += 'MP'

        query = "INSERT INTO records (name, model, memory, camera) VALUES (?, ?, ?, ?)"
        params = (name, model, memory, camera)
        self.db.execute_query(query, params)

        input_window.destroy()

    def update_record(self):
        input_window = tk.Toplevel(self.window)

        self.show_all_records()

        id_label = tk.Label(input_window, text='ID')
        id_entry = tk.Entry(input_window)
        id_label.grid(row=0, column=0)
        id_entry.grid(row=0, column=1)

        name_label = tk.Label(input_window, text='Name')
        name_entry = tk.Entry(input_window)
        name_label.grid(row=1, column=0)
        name_entry.grid(row=1, column=1)

        model_label = tk.Label(input_window, text='Model')
        model_entry = tk.Entry(input_window)
        model_label.grid(row=2, column=0)
        model_entry.grid(row=2, column=1)

        memory_label = tk.Label(input_window, text='Memory')
        memory_entry = tk.Entry(input_window)
        memory_label.grid(row=3, column=0)
        memory_entry.grid(row=3, column=1)

        camera_label = tk.Label(input_window, text='Camera')
        camera_entry = tk.Entry(input_window)
        camera_label.grid(row=4, column=0)
        camera_entry.grid(row=4, column=1)

        submit_button = tk.Button(input_window, text='Update Record',
                                  command=lambda: self.submit_update(id_entry.get(), name_entry.get(),
                                                                     model_entry.get(),
                                                                     memory_entry.get(), camera_entry.get(),
                                                                     input_window))
        submit_button.grid(row=5, column=0, columnspan=2)

    def submit_update(self, id, name, model, memory, camera, input_window):
        query = "UPDATE records SET name=?, model=?, memory=?, camera=? WHERE id=?"
        params = (name, model, memory, camera, id)
        self.db.execute_query(query, params)

        input_window.destroy()

    def delete_record(self):
        input_window = tk.Toplevel(self.window)

        id_label = tk.Label(input_window, text='ID')
        id_entry = tk.Entry(input_window)
        id_label.grid(row=0, column=0)
        id_entry.grid(row=0, column=1)

        submit_button = tk.Button(input_window, text='Delete Record',
                                  command=lambda: self.submit_delete(id_entry.get(), input_window))
        submit_button.grid(row=1, column=0, columnspan=2)

    def submit_delete(self, id, input_window):
        # Delete the record from the database
        query = "DELETE FROM records WHERE id=?"
        params = (id,)
        self.db.execute_query(query, params)

        # Close the input window
        input_window.destroy()

        # Refresh the data displayed in the GUI (optional)
        self.show_all_records()

    def search_records(self):
        # Create a new window for input
        input_window = tk.Toplevel(self.window)

        # Create a label and entry widget for the search query
        query_label = tk.Label(input_window, text='Search Query (write name or model of phone)')
        query_entry = tk.Entry(input_window)
        query_label.grid(row=0, column=0)
        query_entry.grid(row=0, column=1)

        # Create a button to submit the input
        submit_button = tk.Button(input_window, text='Search',
                                  command=lambda: self.submit_search(query_entry.get(), input_window))
        submit_button.grid(row=1, column=0, columnspan=2)

    def submit_search(self, query, input_window):
        # Search for records in the database
        search_query = "SELECT * FROM records WHERE name LIKE ? OR model LIKE ?"
        params = (f"%{query}%", f"%{query}%")
        results = self.db.execute_query(search_query, params)

        # Create a new window to display the results
        results_window = tk.Toplevel(self.window)
        results_window.title('Search Results')

        # Create a listbox widget to display the results
        results_listbox = tk.Listbox(results_window, width=50)
        results_listbox.pack()

        # Add each result to the listbox widget
        for record in results:
            result_string = f"ID: {record[0]}, Name: {record[1]}, Model: {record[2]}, Camera: {record[3]}, Memory: {record[4]}"
            results_listbox.insert(tk.END, result_string)

        # Close the input window
        input_window.destroy()

    def sort_records(self):
        # Create a new window for input
        input_window = tk.Toplevel(self.window)

        # Create a dropdown menu to select the column to sort by
        column_label = tk.Label(input_window, text='Sort by:')
        column_var = tk.StringVar(input_window)
        column_choices = ['id', 'name', 'model', 'memory', 'camera']
        column_dropdown = tk.OptionMenu(input_window, column_var, *column_choices)
        column_dropdown.config(width=10)
        column_label.grid(row=0, column=0)
        column_dropdown.grid(row=0, column=1)

        # Create a button to submit the input
        submit_button = tk.Button(input_window, text='Sort Records',
                                  command=lambda: self.submit_sort(column_var.get()))
        submit_button.grid(row=1, column=0, columnspan=2)

    def submit_sort(self, column):
        if column == 'memory':
            query = "SELECT * FROM records"
            results = self.db.execute_query(query)

            memory_regex = r'(\d+)GB'
            results = [(row[0], row[1], row[2], int(re.findall(memory_regex, row[3])[0]), row[4]) for row in results]

            results = sorted(results, key=lambda x: x[3])

            results = [(row[0], row[1], row[2], f"{row[3]}GB", row[4]) for row in results]
        elif column == 'camera':
            pass
            query = "SELECT * FROM records"
            results = self.db.execute_query(query)

            memory_regex = r'(\d+)MP'
            results = [(row[0], row[1], row[2], row[3], int(re.findall(memory_regex, row[4])[0])) for row in results]

            results = sorted(results, key=lambda x: x[4])

            results = [(row[0], row[1], row[2], row[3], f"{row[4]}MP") for row in results]
        else:
            query = f"SELECT * FROM records ORDER BY {column}"
            results = self.db.execute_query(query)

        results_window = tk.Toplevel(self.window)

        columns = ("ID", "Name", "Model", "Memory", "Camera")
        table = ttk.Treeview(results_window, columns=columns, show="headings")
        for col in columns:
            table.heading(col, text=col)
        table.pack(fill="both", expand=True)

        for row in results:
            table.insert("", "end", values=row)

        # Close the results window when the user is done viewing the results
        close_button = tk.Button(results_window, text="Close", command=results_window.destroy)
        close_button.pack()

    def create_printable_document(self):
        # Get all records from the database
        query = "SELECT * FROM records"
        results = self.db.execute_query(query)

        # Create a file and write records to it
        with open('records.txt', 'w') as f:
            for record in results:
                f.write(f"| {record[0]:<5} | {record[1]:<30} | {record[2]:<20} | {record[3]:<8} | {record[4]:<20} |\n")
                f.write("|-------|--------------------------------|----------------------|----------"
                        "|----------------------|\n")
        os.startfile('records.txt')

        subprocess.Popen(['print', 'records.txt'], shell=True)

    def show_all_records(self):
        # Retrieve all records from the database
        query = "SELECT * FROM records"
        records = self.db.execute_query(query)

        # Create a new window to display the records
        records_window = tk.Toplevel(self.window)
        records_window.title('All Records')

        # Create a Treeview widget to display the records
        tree = ttk.Treeview(records_window)
        tree['columns'] = ('Name', 'Model', 'Memory', 'Camera')
        tree.heading('#0', text='ID')
        tree.column('#0', width=50)
        tree.heading('Name', text='Name')
        tree.column('Name', width=150)
        tree.heading('Model', text='Model')
        tree.column('Model', width=50)
        tree.heading('Memory', text='Memory')
        tree.column('Memory', width=200)
        tree.heading('Camera', text='Camera')
        tree.column('Camera', width=200)

        # Add each record to the Treeview
        for record in records:
            tree.insert('', 'end', text=record[0], values=(record[1], record[2], record[3], record[4]))

        # Pack the Treeview
        tree.pack(fill='both', expand=True)
