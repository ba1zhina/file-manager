import psutil
import os
import json
import xml.etree.ElementTree as ET
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox


def show_disk_info():
    info = ""
    partitions = psutil.disk_partitions()
    
    for partition in partitions:
        info += f"Имя устройства: {partition.device}\n"
        info += f"Точка монтирования: {partition.mountpoint}\n"
        info += f"Тип файловой системы: {partition.fstype}\n"
        
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            info += f"Размер диска: {usage.total / (1024 ** 3):.2f} GB\n"
            info += f"Свободное место: {usage.free / (1024 ** 3):.2f} GB\n"
            info += f"Используемое место: {usage.used / (1024 ** 3):.2f} GB\n"
            info += f"Процент использования: {usage.percent}%\n"
        except PermissionError:
            info += "Недостаточно прав для получения информации о диске.\n"
        
        info += "-" * 40 + "\n"
    
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, info)


def create_file():
    user_input = user_input_entry.get()
    if not user_input:
        messagebox.showerror("Ошибка", "Введите строку для записи в файл!")
        return
    
    file_name = "example.txt"
    with open(file_name, "w") as file:
        file.write(user_input)
    
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Файл {file_name} успешно создан и запись выполнена.\n")
    
    with open(file_name, "r") as file:
        content = file.read()
        output_text.insert(tk.END, f"Содержимое файла:\n{content}\n")
    
    os.remove(file_name)
    output_text.insert(tk.END, f"Файл {file_name} успешно удалён.\n")



def create_json():
    name = name_entry.get()
    age = age_entry.get()
    city = city_entry.get()
    
    if not name or not age or not city:
        messagebox.showerror("Ошибка", "Введите все поля!")
        return
    
    file_name = "data.json"
    
    data = {
        "name": name,
        "age": age,
        "city": city
    }
    
    with open(file_name, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"JSON файл {file_name} успешно создан.\n")
    
    with open(file_name, "r", encoding="utf-8") as json_file:
        content = json.load(json_file)
        output_text.insert(tk.END, json.dumps(content, ensure_ascii=False, indent=4) + "\n")
    
    os.remove(file_name)
    output_text.insert(tk.END, f"Файл {file_name} успешно удалён.\n")


def create_xml():
    name = name_entry.get()
    age = age_entry.get()
    city = city_entry.get()
    
    if not name or not age or not city:
        messagebox.showerror("Ошибка", "Введите все поля!")
        return
    
    file_name = "data.xml"
    
    if not os.path.exists(file_name):
        root = ET.Element("users") 
        tree = ET.ElementTree(root)
        with open(file_name, "wb") as xml_file:
            tree.write(xml_file)
    
    tree = ET.parse(file_name)
    root = tree.getroot()
    
    user = ET.Element("user")
    name_elem = ET.SubElement(user, "name")
    name_elem.text = name
    age_elem = ET.SubElement(user, "age")
    age_elem.text = age
    city_elem = ET.SubElement(user, "city")
    city_elem.text = city
    
    root.append(user)
    
    with open(file_name, "wb") as xml_file:
        tree.write(xml_file)
    
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"XML файл {file_name} успешно создан.\n")
    
    tree = ET.parse(file_name)
    root = tree.getroot()
    for user in root:
        name = user.find("name").text
        age = user.find("age").text
        city = user.find("city").text
        output_text.insert(tk.END, f"Имя: {name}, Возраст: {age}, Город: {city}\n")
    
    os.remove(file_name)
    output_text.insert(tk.END, f"Файл {file_name} успешно удалён.\n")


def create_zip():
    file_to_add = filedialog.askopenfilename()
    if not file_to_add:
        messagebox.showerror("Ошибка", "Выберите файл для архивации!")
        return
    
    zip_filename = "my_archive.zip"
    
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        zip_file.write(file_to_add, os.path.basename(file_to_add))
    
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Архив {zip_filename} успешно создан и файл добавлен.\n")
    
    size = os.path.getsize(zip_filename)
    output_text.insert(tk.END, f"Размер архива {zip_filename}: {size} байт\n")
    
    extraction_folder = "extracted_files"
    os.makedirs(extraction_folder, exist_ok=True)
    
    with zipfile.ZipFile(zip_filename, 'r') as zip_file:
        zip_file.extractall(extraction_folder)
    
    output_text.insert(tk.END, f"Архив {zip_filename} разархивирован в {extraction_folder}\n")
    
    os.remove(file_to_add)
    os.remove(zip_filename)
    output_text.insert(tk.END, f"Файл и архив успешно удалены.\n")


root = tk.Tk()
root.title("Файловый менеджер")
root.geometry("600x600")

output_text = tk.Text(root, height=20, width=70)
output_text.pack(pady=10)

frame1 = tk.Frame(root)
frame1.pack()

tk.Label(frame1, text="Строка для записи в файл:").pack(side=tk.LEFT)
user_input_entry = tk.Entry(frame1)
user_input_entry.pack(side=tk.LEFT, padx=5)

frame2 = tk.Frame(root)
frame2.pack(pady=5)

tk.Label(frame2, text="Имя:").pack(side=tk.LEFT)
name_entry = tk.Entry(frame2)
name_entry.pack(side=tk.LEFT, padx=5)

tk.Label(frame2, text="Возраст:").pack(side=tk.LEFT)
age_entry = tk.Entry(frame2)
age_entry.pack(side=tk.LEFT, padx=5)

tk.Label(frame2, text="Город:").pack(side=tk.LEFT)
city_entry = tk.Entry(frame2)
city_entry.pack(side=tk.LEFT, padx=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Информация о дисках", command=show_disk_info).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Создать файл", command=create_file).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Создать JSON", command=create_json).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Создать XML", command=create_xml).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Создать ZIP", command=create_zip).pack(side=tk.LEFT, padx=5)

root.mainloop()
