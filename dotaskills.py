import tkinter
import tkinter.messagebox
import customtkinter
import os
import sys
import sqlite3

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

cleaner = None

from sys import platform
if platform == "linux" or platform == "linux2":
	cleaner = "clear"
elif platform == "darwin":
	cleaner = "clear"
elif platform == "win32":
	cleaner = "cls"

class App(customtkinter.CTk):
	def __init__(self):
		super().__init__()

		self.title("Инвентаризация имущества")
		self.geometry(f"{1100}x{580}")

		self.grid_columnconfigure(1, weight=1)
		self.grid_columnconfigure((2, 3), weight=0)
		self.grid_rowconfigure((0, 1, 2), weight=1)

		conn = sqlite3.connect('inventorytest.db')
		c = conn.cursor()
		c.execute('''CREATE TABLE IF NOT EXISTS inventory
					(name text, quantity integer)''')
		conn.commit()
		conn.close()

		# Боковая панель
		self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
		self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
		self.sidebar_frame.grid_rowconfigure(4, weight=1)
		
		# Название программы
		self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="INVENTORY", font=customtkinter.CTkFont(size=20, weight="bold"))
		self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

		# Временная кнопка перезагрузки программы для удобства
		self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Restart", command=self.sidebar_button_event)
		self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
		
		# Настройка темы приложения
		self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Тема приложения:", anchor="w")
		self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
		self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
		self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
		
		# Настройка маштаба приложения
		self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Маштаб приложения:", anchor="w")
		self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
		self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
		self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

		state_text_box = "normal"
		# Основное текстовое поле программы
		self.textbox = customtkinter.CTkTextbox(self, width=250, state=state_text_box)
		self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

		# Поле с кнопками и выбором между добавлением предмета и заметками
		self.tabview = customtkinter.CTkTabview(self, width=250)
		self.tabview.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
		self.tabview.add("Add Items")
		self.tabview.add("Add Mark")
		self.tabview.tab("Add Items").grid_columnconfigure(0, weight=1)
		self.tabview.tab("Add Mark").grid_columnconfigure(0, weight=1)

		# Кнопки для tabview
		self.label_for_add_items_name = customtkinter.CTkLabel(self.tabview.tab("Add Items"), text="Название предмета", anchor="w")
		self.label_for_add_items_name.grid(row=2, column=0, padx=20, pady=(5,5))
		self.entry_name_item = customtkinter.CTkEntry(self.tabview.tab("Add Items"), placeholder_text="Название")
		self.entry_name_item.grid(row=3, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky="nsew")
		self.label_for_add_items_num = customtkinter.CTkLabel(self.tabview.tab("Add Items"), text="Количество", anchor="w")
		self.label_for_add_items_num.grid(row=4, column=0, padx=20, pady=(5,5))
		self.entry_number_item = customtkinter.CTkEntry(self.tabview.tab("Add Items"), placeholder_text="Количество")
		self.entry_number_item.grid(row=5, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky="nsew")
		self.add_items_button = customtkinter.CTkButton(self.tabview.tab("Add Items"), text="Добавить предмет", command=self.add_items_event)
		self.add_items_button.grid(row=6, column=0, padx=20, pady=(30,10))
		self.show_items_button = customtkinter.CTkButton(self.tabview.tab("Add Items"), text="Просмотреть базу", command=self.show_items_event)
		self.show_items_button.grid(row=7, column=0, padx=20, pady=(10,10))
		self.delete_items_button = customtkinter.CTkButton(self.tabview.tab("Add Items"), text="Удалить предмет", command=self.delete_items_event)
		self.delete_items_button.grid(row=8, column=0, padx=20, pady=(10,10))

		# Дефолтные настройки приложения
		self.appearance_mode_optionemenu.set("Dark")
		self.scaling_optionemenu.set("100%")

	def add_items_event(self):
		name = self.entry_name_item.get()
		quantity = self.entry_number_item.get()
		if name == "":
			tkinter.messagebox.showerror("Ошибка", "Введите название предмета")
			return
		if quantity == "":
			tkinter.messagebox.showerror("Ошибка", "Введите количество предметов")
			return
		try:
			quantity = int(quantity)
		except ValueError:
			tkinter.messagebox.showerror("Ошибка", "Количество предметов должно быть целым числом")
			return
		conn = sqlite3.connect('inventorytest.db')
		c = conn.cursor()
		c.execute("INSERT INTO inventory (name, quantity) VALUES (?, ?)", (name, quantity))
		conn.commit()
		conn.close()
		self.entry_name_item.delete(0, "end")
		self.entry_number_item.delete(0, "end")
		tkinter.messagebox.showinfo("Уведомление", f"Предмет '{name}' успешно добавлен в базу данных")

	def show_items_event(self):
		conn = sqlite3.connect('inventorytest.db')
		c = conn.cursor()
		c.execute("SELECT * FROM inventory")
		rows = c.fetchall()
		conn.close()
		self.textbox.delete("1.0", "end")
		for row in rows:
			self.textbox.insert("end", f"{row[0]}: {row[1]}\n")

	def delete_items_event(self):
		item_name = self.entry_name_item.get()
		conn = sqlite3.connect('inventorytest.db')
		c = conn.cursor()
		c.execute(f"DELETE FROM inventory WHERE name='{item_name}'")
		conn.commit()
		conn.close()
		tkinter.messagebox.showinfo(title="Успешно", message=f"Предмет '{item_name}' удален из базы данных.")

	def change_appearance_mode_event(self, new_appearance_mode: str):
		customtkinter.set_appearance_mode(new_appearance_mode)

	def change_scaling_event(self, new_scaling: str):
		new_scaling_float = int(new_scaling.replace("%", "")) / 100
		customtkinter.set_widget_scaling(new_scaling_float)

	def sidebar_button_event(self):
		os.system(cleaner)
		print("Restart programm")
		os.execl(sys.executable, sys.executable, *sys.argv)

if __name__ == "__main__":
	app = App()
	app.mainloop()