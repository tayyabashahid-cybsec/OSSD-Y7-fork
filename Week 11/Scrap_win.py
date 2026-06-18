import csv
import urllib.request
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox


def store_as_csv(records, destination):
    with open(destination, mode='w', newline='', encoding='utf-8') as doc:
        col_writer = csv.DictWriter(doc, fieldnames=['vehicle', 'cost'])
        col_writer.writeheader()
        col_writer.writerows(records)


def pull_vehicle_data(brand_name):
    req = urllib.request.Request(
        f"https://www.pakwheels.com/new-cars/pricelist/{brand_name}",
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            )
        }
    )
    try:
        with urllib.request.urlopen(req) as webpage:
            raw_html = webpage.read().decode('utf-8')
    except Exception:
        messagebox.showerror("Error", "Website not responding")
        return []

    dom = BeautifulSoup(raw_html, 'html.parser')
    all_rows = dom.select('table tr')
    collected = []
    for tr in all_rows:
        cells = tr.select('td')
        if len(cells) >= 2:
            collected.append({
                'vehicle': cells[0].get_text(strip=True),
                'cost': cells[1].get_text(strip=True)
            })
    return collected


def on_search():
    chosen = picker.get()
    if chosen == "Select Manufacturer":
        messagebox.showwarning("Warning", "Please select a manufacturer")
        return
    output_area.delete(1.0, tk.END)
    output_area.insert(tk.END, "Loading...\n")
    win.update()
    vehicles = pull_vehicle_data(chosen.lower())
    output_area.delete(1.0, tk.END)
    if not vehicles:
        output_area.insert(tk.END, "No Data Found")
        return
    for idx, v in enumerate(vehicles, start=1):
        output_area.insert(
            tk.END,
            f"#{idx}  {v['vehicle']}\n"
            f"    Price : {v['cost']}\n"
            f"{'─'*50}\n"
        )


def on_save():
    chosen = picker.get()
    if chosen == "Select Manufacturer":
        messagebox.showwarning("Warning", "Please select a manufacturer")
        return
    vehicles = pull_vehicle_data(chosen.lower())
    if not vehicles:
        return
    dest = f"{chosen.lower()}_data.csv"
    store_as_csv(vehicles, dest)
    messagebox.showinfo("Saved", f"{dest} saved successfully")

win = tk.Tk()
win.title("Car Price Scraper Pro")
win.geometry("850x600")
win.config(bg="#2d2d44")

tk.Label(
    win, text="PakWheels Price Finder",
    font=("Trebuchet MS", 22, "bold"),
    bg="#2d2d44", fg="#f9c74f"
).pack(pady=15)

tk.Label(
    win, text="Search & Export Car Prices",
    font=("Trebuchet MS", 10),
    bg="#2d2d44", fg="#c9c9e0"
).pack(pady=(0, 10))

wrapper = tk.Frame(win, bg="#3a3a5c", bd=0)
wrapper.pack(padx=20, pady=5, fill="both", expand=True)

left_panel = tk.Frame(wrapper, bg="#3a3a5c", width=200)
left_panel.pack(side="left", fill="y", padx=15, pady=15)
left_panel.pack_propagate(False)

tk.Label(
    left_panel, text="Select Brand",
    font=("Trebuchet MS", 11, "bold"),
    bg="#3a3a5c", fg="#f9c74f"
).pack(pady=(10, 5))

cb_style = ttk.Style()
cb_style.theme_use("clam")
cb_style.configure(
    "TCombobox",
    fieldbackground="#2d2d44",
    background="#2d2d44",
    foreground="white",
    padding=6
)

picker = ttk.Combobox(
    left_panel,
    values=["Select Manufacturer", "kia", "honda",
            "toyota", "suzuki", "hyundai"],
    font=("Trebuchet MS", 10),
    width=18, state="readonly"
)
picker.current(0)
picker.pack(pady=8)

tk.Button(
    left_panel, text="Search Prices",
    command=on_search,
    bg="#f9c74f", fg="#2d2d44",
    activebackground="#e0b03a",
    activeforeground="#2d2d44",
    font=("Trebuchet MS", 10, "bold"),
    relief="flat", cursor="hand2",
    width=16, pady=10
).pack(pady=(20, 8))

tk.Button(
    left_panel, text="Export CSV",
    command=on_save,
    bg="#4cc9f0", fg="#2d2d44",
    activebackground="#3ab5da",
    activeforeground="#2d2d44",
    font=("Trebuchet MS", 10, "bold"),
    relief="flat", cursor="hand2",
    width=16, pady=10
).pack(pady=8)

tk.Frame(wrapper, bg="#f9c74f", width=2).pack(
    side="left", fill="y", pady=15
)

right_panel = tk.Frame(wrapper, bg="#3a3a5c")
right_panel.pack(side="left", fill="both", expand=True,
                 padx=10, pady=15)

tk.Label(
    right_panel, text="Results",
    font=("Trebuchet MS", 11, "bold"),
    bg="#3a3a5c", fg="#f9c74f"
).pack(anchor="w", pady=(0, 5))

out_frame = tk.Frame(right_panel, bg="#3a3a5c")
out_frame.pack(fill="both", expand=True)

y_bar = tk.Scrollbar(out_frame)
y_bar.pack(side="right", fill="y")

output_area = tk.Text(
    out_frame,
    bg="#2d2d44", fg="#e2e2e2",
    insertbackground="white",
    font=("Courier New", 11),
    relief="flat", padx=12, pady=12,
    yscrollcommand=y_bar.set,
    selectbackground="#f9c74f",
    selectforeground="#2d2d44"
)
output_area.pack(fill="both", expand=True)
y_bar.config(command=output_area.yview)

tk.Label(
    win,
    text="Data sourced from PakWheels.com",
    font=("Trebuchet MS", 8),
    bg="#2d2d44", fg="#c9c9e0"
).pack(pady=6)

win.mainloop()