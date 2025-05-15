import os
import json
from PySide6.QtWidgets import QTableWidgetItem
from core.utils import get_data_dir

DATA_DIR = get_data_dir()
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

def load_history_initial(table):
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump([], f, indent=4)
    else:
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
                for entry in history:
                    row = table.rowCount()
                    table.insertRow(row)
                    table.setItem(row, 0, QTableWidgetItem(entry.get("url", "")))
        except:
            pass

def save_history(table):
    history = []
    for r in range(table.rowCount()):
        url = table.item(r,0).text() if table.item(r,0) else ""
        history.append({"url": url})
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def add_history_entry(table, url, enabled=True):
    if not enabled:
        return
    row = table.rowCount()
    table.insertRow(row)
    table.setItem(row, 0, QTableWidgetItem(url))
    save_history(table)

def delete_selected_history(table, log_callback):
    selected_rows = set()
    for it in table.selectedItems():
        selected_rows.add(it.row())
    for r in sorted(selected_rows, reverse=True):
        table.removeRow(r)
    log_callback(f"Deleted {len(selected_rows)} history entries.")
    save_history(table)

def delete_all_history(table, confirm, log_callback):
    ans = confirm()
    if ans:
        table.setRowCount(0)
        log_callback("All history deleted.")
        save_history(table)

def search_history(table, txt):
    txt = txt.lower()
    for r in range(table.rowCount()):
        hide = True
        for c in range(table.columnCount()):
            it = table.item(r, c)
            if it and txt in it.text().lower():
                hide = False
                break
        table.setRowHidden(r, hide)

def export_history(file_path):
    """Export history data to a JSON file"""
    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
        with open(file_path, "w") as f:
            json.dump(history, f, indent=4)
        return True
    except Exception as e:
        return False
