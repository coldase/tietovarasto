from tkinter import *
from tkinter import filedialog

class Tarvike:
	def __init__(self, tyyppi, paino):
		self.tyyppi = tyyppi
		self.paino = paino
		self.tunniste = id(self)

class Tietovarasto:
	def __init__(self):
		self.root = Tk()
		self.root.geometry("400x250+300+300")
		self.root.title("Tietovarastonäyttö")
		self.storage = []

	def buttons(self):
		self.add_new_btn = Button(self.root, text="Uusi varasto", command=lambda:self.storage_window("new"))
		self.open_btn = Button(self.root, text="Avaa varasto", command=self.open_file)
		self.add_new_btn.place(x=150,y=150, width=100)
		self.open_btn.place(x=150,y=180, width=100)

	def main_labels(self):
		self.myname = Label(self.root, text="By Jari-Pekka Vihiniemi")
		self.main_header = Label(self.root, text="Tietovarasto")
		self.main_header.config(font=('Helvetica',44))
		self.myname.config(font=('Helvetica',10))
		self.main_header.place(x=40, y=20)
		self.myname.place(x=130, y=90)

	def open_file(self):
		self.storage = []
		try:
			self.myfile =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
			with open(self.myfile, 'r') as file:
				for x in file.readlines():
					try:
						r_id, r_tyyppi, r_paino = x.split("|")
						self.storage.append(Tarvike(r_tyyppi, r_paino))
					except:
						pass
			self.storage_window()
		except:
			pass

	def save_to_file(self):
		try:
			self.myfile =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
			with open(self.myfile, "a") as file:
				for item in self.storage:
					file.write(f'{item.tunniste}|{item.tyyppi}|{item.paino}\n')
		except:
			pass

	def search_window(self):
		self.search_root = Toplevel(self.root)
		self.search_root.geometry("185x60+300+300")

		self.search_header = Label(self.search_root, text="Etsi tyyppiä")
		self.search_entry = Entry(self.search_root)
		self.s_btn = Button(self.search_root, text="Hae", command=self.search_by_name)

		self.search_header.place(x=5, y=10)
		self.search_entry.place(x=5, y=30)
		self.s_btn.place(x=140, y=30, height=20, width=40)

	def search_by_name(self):
		self.newlist = []		
		self.search_name = self.search_entry.get()
		for x in self.storage:
			if x.tyyppi == self.search_name:
				self.newlist.append(x)

		self.search_root.destroy()
		self.new_storage_window.destroy()
		self.storage_window("find")

	def storage_window(self, status=None):
		if status == "new":
			self.storage = []
		if status == "find":
			self.storage = self.newlist

		self.new_storage_window = Toplevel(self.root)
		self.new_storage_window.geometry("300x300+300+300")

		self.add_new_btn = Button(self.new_storage_window, text="Lisää", command=self.open_new_window)
		self.keskiarvo_btn = Button(self.new_storage_window, text="Keskiarvo", command=self.laske_keskiarvo)
		self.find_btn = Button(self.new_storage_window, text="Etsi", command=self.search_window)
		self.header_label = Label(self.new_storage_window, text="ID  |  Tyyppi  |  Paino")
		self.delete_btn = Button(self.new_storage_window, text="Poista", command=self.delete_by_id)
		self.save_btn = Button(self.new_storage_window, text="Tallenna", command=self.save_to_file)
		self.ka_label = Label(self.new_storage_window, text="")


		self.header_label.place(x=65, y=10)
		self.find_btn.place(x=230, y=40, height=25, width=60)
		self.keskiarvo_btn.place(x=230, y=70, height=25, width=60)
		self.add_new_btn.place(x=230, y=100, height=25, width=60)
		self.delete_btn.place(x=230, y=130, height=25, width=60)
		self.save_btn.place(x=230, y=160, height=25, width=60)
		self.ka_label.place(x=230, y=235)
		self.list_items()

	def list_items(self):
		self.new_box = Listbox(self.new_storage_window)
		for i, item in enumerate(self.storage):
			self.new_box.insert(i, f'{item.tunniste} | {item.tyyppi} | {item.paino}kg')
		self.new_box.place(x=20,y=40, width=200, height=230)

	def delete_by_id(self):
		self.sel = self.new_box.curselection()
		for index in self.sel[::-1]:
			self.storage.pop(index)
			self.new_box.delete(index)

	def add_window(self):
		self.new_window = Toplevel(self.root)
		self.new_window.geometry("200x150+300+300")

		self.type_label = Label(self.new_window, text="Anna tyyppi")
		self.type_entry = Entry(self.new_window)
		self.weight_label = Label(self.new_window, text="Anna paino")
		self.weight_entry = Entry(self.new_window)
		self.submit_btn = Button(self.new_window, text="Lisää", command=self.add_items)

		self.type_label.place(x=38, y=20)
		self.type_entry.place(x=40, y=40)
		self.weight_label.place(x=38, y=60)
		self.weight_entry.place(x=40, y=80)
		self.submit_btn.place(x=40, y=110)

	def laske_keskiarvo(self):
		try:
			total = 0
			for item in self.storage:
				total += int(item.paino)
			self.ka_label.config(text=f'Keskiarvo:\n{round(total/len(self.storage), 2)}kg')
		except:
			self.ka_label.config(text=" Error!!!")

	def add_items(self):
		new_type = self.type_entry.get()
		new_weight = self.weight_entry.get()
		new_item = Tarvike(new_type, new_weight)
		self.storage.append(new_item)
		self.new_window.destroy()
		print(f'Tyyppi: {new_type}, Paino: {new_weight} added')
		self.new_storage_window.destroy()
		self.storage_window()

	def open_new_window(self):
		self.add_window()

	def run(self):
		self.buttons()
		self.main_labels()
		self.root.mainloop()

app = Tietovarasto()

if __name__ == "__main__":
	app.run()
