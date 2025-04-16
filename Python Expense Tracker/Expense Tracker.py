import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
import csv
from datetime import datetime

class ExpenseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("1300x600")
        self.expenses = []
        self.displayed_expenses = []
        self.categories = ["Comida", "Transporte", "Utilidades", "Entretenimiento", "Otro"]
        self.load_expenses()
        self.create_widgets()

    def create_widgets(self):
        # Encabezado
        tk.Label(self, text="Expenses", font=("Helvetica", 20, "bold")).pack(pady=10)

        # Marco de entrada
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        # Campos de entrada
        tk.Label(input_frame, text="Monto:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5)
        self.amount_entry = tk.Entry(input_frame, width=15, font=("Helvetica", 12))
        self.amount_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Descripción:", font=("Helvetica", 12)).grid(row=0, column=2, padx=5)
        self.desc_entry = tk.Entry(input_frame, width=20, font=("Helvetica", 12))
        self.desc_entry.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Categoría:", font=("Helvetica", 12)).grid(row=0, column=4, padx=5)
        self.category_combobox = ttk.Combobox(input_frame, values=self.categories, width=15, font=("Helvetica", 12))
        self.category_combobox.grid(row=0, column=5, padx=5)
        self.category_combobox.set(self.categories[0])

        tk.Label(input_frame, text="Fecha (YYYY-MM-DD):", font=("Helvetica", 12)).grid(row=0, column=6, padx=5)
        self.date_entry = tk.Entry(input_frame, width=15, font=("Helvetica", 12))
        self.date_entry.grid(row=0, column=7, padx=5)

        # Botones de acciones
        tk.Button(input_frame, text="Añadir Gasto", command=self.add_expense).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(input_frame, text="Editar Gasto", command=self.edit_expense).grid(row=1, column=2, columnspan=2, pady=10)
        tk.Button(input_frame, text="Eliminar Gasto", command=self.delete_expense).grid(row=1, column=4, columnspan=2, pady=10)
        tk.Button(input_frame, text="Guardar Gastos", command=self.save_expenses).grid(row=1, column=6, columnspan=2, pady=10)

        # Búsqueda
        tk.Label(input_frame, text="Buscar:", font=("Helvetica", 12)).grid(row=2, column=0, padx=5)
        self.search_entry = tk.Entry(input_frame, width=20, font=("Helvetica", 12))
        self.search_entry.grid(row=2, column=1, columnspan=2, padx=5)
        tk.Button(input_frame, text="Buscar", command=self.search_expenses).grid(row=2, column=3, pady=10)

        # Filtro por mes
        tk.Label(input_frame, text="Mes:", font=("Helvetica", 12)).grid(row=2, column=4, padx=5)
        self.month_combobox = ttk.Combobox(input_frame, values=[str(i).zfill(2) for i in range(1, 13)], width=5, font=("Helvetica", 12))
        self.month_combobox.grid(row=2, column=5, padx=5)
        self.month_combobox.set("01")

        tk.Label(input_frame, text="Año:", font=("Helvetica", 12)).grid(row=2, column=6, padx=5)
        self.year_combobox = ttk.Combobox(input_frame, values=[str(i) for i in range(2020, 2026)], width=7, font=("Helvetica", 12))
        self.year_combobox.grid(row=2, column=7, padx=5)
        self.year_combobox.set("2023")

        tk.Button(input_frame, text="Filtrar por Mes", command=self.filter_by_month).grid(row=3, column=4, columnspan=2, pady=10)
        tk.Button(input_frame, text="Mostrar Todos", command=self.show_all).grid(row=3, column=6, columnspan=2, pady=10)

        # Marco de lista
        list_frame = tk.Frame(self)
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Listbox con scrollbar
        self.expense_listbox = tk.Listbox(list_frame, width=70, height=15, font=("Helvetica", 12))
        self.expense_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.expense_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.expense_listbox.yview)

        # Total
        self.total_label = tk.Label(self, text="Total Gastos: USD 0.00", font=("Helvetica", 12))
        self.total_label.pack(pady=10)

        # Inicializar lista
        self.show_all()

    def load_expenses(self):
        try:
            with open("expenses.csv", "r", newline="") as file:
                reader = csv.DictReader(file)
                self.expenses = [{"date": row["Fecha"], "amount": float(row["Monto"]),
                                 "description": row["Descripción"], "category": row["Categoría"]}
                                for row in reader]
        except FileNotFoundError:
            self.expenses = []

    def save_expenses(self):
        with open("expenses.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Fecha", "Monto", "Descripción", "Categoría"])
            writer.writeheader()
            for expense in self.expenses:
                writer.writerow({"Fecha": expense["date"], "Monto": expense["amount"],
                                "Descripción": expense["description"], "Categoría": expense["category"]})

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            description = self.desc_entry.get().strip()
            category = self.category_combobox.get()
            date = self.date_entry.get().strip()
            if not description or not date:
                messagebox.showerror("Error", "Descripción y fecha son obligatorios")
                return
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Fecha debe estar en formato YYYY-MM-DD")
                return
            expense = {"date": date, "amount": amount, "description": description, "category": category}
            self.expenses.append(expense)
            self.show_all()
            self.clear_entries()
            self.save_expenses()
        except ValueError:
            messagebox.showerror("Error", "Monto debe ser un número válido")

    def edit_expense(self):
        try:
            index = self.expense_listbox.curselection()[0]
            expense = self.displayed_expenses[index]
            amount = simpledialog.askfloat("Editar", "Nuevo monto:", initialvalue=expense["amount"])
            description = simpledialog.askstring("Editar", "Nueva descripción:", initialvalue=expense["description"])
            category = simpledialog.askstring("Editar", "Nueva categoría:", initialvalue=expense["category"])
            date = simpledialog.askstring("Editar", "Nueva fecha (YYYY-MM-DD):", initialvalue=expense["date"])
            if amount and description and date and category:
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    original_index = self.expenses.index(expense)
                    self.expenses[original_index] = {"date": date, "amount": amount,
                                                    "description": description, "category": category}
                    self.show_all()
                    self.save_expenses()
                except ValueError:
                    messagebox.showerror("Error", "Fecha debe estar en formato YYYY-MM-DD")
        except IndexError:
            messagebox.showerror("Error", "Selecciona un gasto para editar")

    def delete_expense(self):
        try:
            index = self.expense_listbox.curselection()[0]
            expense = self.displayed_expenses[index]
            if messagebox.askyesno("Confirmar", "¿Eliminar este gasto?"):
                self.expenses.remove(expense)
                self.show_all()
                self.save_expenses()
        except IndexError:
            messagebox.showerror("Error", "Selecciona un gasto para eliminar")

    def search_expenses(self):
        term = self.search_entry.get().strip().lower()
        if term:
            self.displayed_expenses = [exp for exp in self.expenses if term in exp["description"].lower()]
        else:
            self.displayed_expenses = sorted(self.expenses, key=lambda x: x["date"])
        self.refresh_list()

    def filter_by_month(self):
        month = self.month_combobox.get()
        year = self.year_combobox.get()
        self.displayed_expenses = [exp for exp in self.expenses
                                 if exp["date"].split("-")[0] == year and exp["date"].split("-")[1] == month]
        self.refresh_list()

    def show_all(self):
        self.displayed_expenses = sorted(self.expenses, key=lambda x: x["date"])
        self.refresh_list()

    def refresh_list(self):
        self.expense_listbox.delete(0, tk.END)
        total = 0
        for exp in self.displayed_expenses:
            display_text = f"{exp['date']} | {exp['category']} | {exp['description']} | USD {exp['amount']:.2f}"
            self.expense_listbox.insert(tk.END, display_text)
            total += exp['amount']
        self.total_label.config(text=f"Total Gastos: USD {total:.2f}")

    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.category_combobox.set(self.categories[0])
        self.date_entry.delete(0, tk.END)

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()
