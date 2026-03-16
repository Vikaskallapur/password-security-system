# gui/app.py

import tkinter as tk
from tkinter import ttk, messagebox

from core.owasp_rules import check_policy
from core.entropy import calculate_entropy, crack_time
from core.breach_check import check_breach
from core.reuse_detector import init_db, check_reuse, store_password
from core.attack_simulator import simulate_attack

init_db()


def analyze_password():
    password = password_entry.get()

    if not password:
        messagebox.showwarning("Input Error", "Please enter a password")
        return

    score, issues = check_policy(password)
    entropy = calculate_entropy(password)
    cpu, gpu = crack_time(entropy)
    breached, count = check_breach(password)
    reused = check_reuse(password)
    attack = simulate_attack(entropy)

    if score >= 4 and not breached and not reused:
        store_password(password)

    report = f"""
Password Security Report

OWASP Score       : {score} / 5
Issues            : {issues if issues else "None"}
Entropy           : {entropy:.2f} bits
Crack Time (CPU)  : {cpu:.2e} seconds
Crack Time (GPU)  : {gpu:.2e} seconds
Breached          : {breached} {"(" + str(count) + " times)" if breached else ""}
Reused            : {reused}
Attack Simulation : {attack}
"""

    result_box.config(state="normal")
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, report)
    result_box.config(state="disabled")

    # Color indicator
    if score >= 4 and not breached:
        status_label.config(text="✔ STRONG PASSWORD", foreground="green")
    elif score >= 3:
        status_label.config(text="⚠ MODERATE PASSWORD", foreground="orange")
    else:
        status_label.config(text="✖ WEAK PASSWORD", foreground="red")


def launch_gui():
    global password_entry, result_box, status_label

    root = tk.Tk()
    root.title("Password Security System")
    root.geometry("700x520")
    root.resizable(False, False)

    style = ttk.Style(root)
    style.theme_use("clam")

    title = ttk.Label(
        root,
        text="🔐 Password Security Analyzer",
        font=("Helvetica", 18, "bold")
    )
    title.pack(pady=10)

    frame = ttk.Frame(root)
    frame.pack(pady=10)

    ttk.Label(frame, text="Enter Password:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5)
    password_entry = ttk.Entry(frame, width=40, show="*")
    password_entry.grid(row=0, column=1, padx=5, pady=5)

    analyze_btn = ttk.Button(
        root,
        text="Analyze Password",
        command=analyze_password
    )
    analyze_btn.pack(pady=10)

    status_label = ttk.Label(
        root,
        text="",
        font=("Helvetica", 12, "bold")
    )
    status_label.pack(pady=5)

    result_box = tk.Text(
        root,
        height=16,
        width=85,
        state="disabled",
        font=("Courier", 10)
    )
    result_box.pack(padx=10, pady=10)

    root.mainloop()
