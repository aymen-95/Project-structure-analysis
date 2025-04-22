import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path

def analyze_structure(folder_path):
    folder_path = Path(folder_path)
    result = ""

    files = [f.name for f in folder_path.glob("*")]
    file_set = set(files)

    if "pubspec.yaml" in file_set:
        project_type = "Flutter"
    elif "composer.json" in file_set:
        project_type = "PHP (Laravel)"
    elif "package.json" in file_set:
        project_type = "Node.js"
    else:
        project_type = "غير معروف"

    folders = [f.name for f in folder_path.iterdir() if f.is_dir()]
    if set(["lib", "routes", "models", "controllers"]).intersection(folders):
        structure_type = "تنظيم حديث (Modules / MVC)"
    else:
        structure_type = "تنظيم عادي"

    result += f"🔰 نوع المشروع: {project_type}\n"
    result += f"📂 طريقة التنظيم: {structure_type}\n\n"
    result += "📁 الهيكل التنظيمي:\n"

    # عرض الهيكل التنظيمي
    def walk_dir(dir_path, indent=0):
        tree = ""
        for item in sorted(Path(dir_path).iterdir()):
            tree += "  " * indent + f"📄 {item.name}\n" if item.is_file() else "  " * indent + f"📁 {item.name}/\n"
            if item.is_dir():
                tree += walk_dir(item, indent + 1)
        return tree

    result += walk_dir(folder_path)
    return result

def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)

def analyze_and_display():
    path = folder_path.get()
    if not path:
        messagebox.showerror("خطأ", "الرجاء اختيار مجلد أولًا.")
        return
    output = analyze_structure(path)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, output)

def save_to_file():
    content = result_text.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("تنبيه", "لا يوجد محتوى لحفظه.")
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
        title="اختر اسم ومكان حفظ الملف"
    )
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("تم الحفظ", f"✅ تم حفظ الملف بنجاح في:\n{file_path}")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء الحفظ:\n{e}")

root = tk.Tk()
root.title("تحليل هيكل المشاريع")
root.geometry("700x650")

folder_path = tk.StringVar()

tk.Label(root, text="مسار المجلد:").pack(pady=5)
tk.Entry(root, textvariable=folder_path, width=80).pack(pady=5)
tk.Button(root, text="اختيار مجلد", command=browse_folder).pack()

tk.Button(root, text="تحليل المجلد", command=analyze_and_display, bg="#4CAF50", fg="white").pack(pady=10)

result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=85, height=25)
result_text.pack(pady=10)

tk.Button(root, text=" حفظ إلى ملف", command=save_to_file, bg="#2196F3", fg="white").pack(pady=10)

root.mainloop()