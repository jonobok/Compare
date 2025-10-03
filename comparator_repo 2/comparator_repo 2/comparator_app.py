# comparator_app.py
import re
import tkinter as tk
from tkinter import ttk, messagebox

APP_TITLE = "Comparator"
HELP_TEXT = (
    "Enter any two numbers (accepts $ and commas). Output format:\n"
    "(increased by $X or Y%)  or  (decreased by $X or Y%)  or  (no change)\n"
    "• Dollar change: rounded to nearest whole dollar (no cents)\n"
    "• Percent change: rounded to nearest whole percent\n"
    "• If the reference value is 0, percent shows as —%\n"
)

MONEY_RE = re.compile(r"[$,\s]")

def strip_money(s: str) -> str:
    return MONEY_RE.sub("", s or "")

def to_number(s: str):
    if s is None:
        return float("nan")
    s = s.strip()
    if s == "":
        return float("nan")
    try:
        return float(s)
    except Exception:
        return float("nan")

def fmt_no_cents(n: float) -> str:
    n = round(abs(n))
    return f"${n:,.0f}"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("540x280")
        self.minsize(520, 260)

        root = ttk.Frame(self, padding=16)
        root.pack(fill="both", expand=True)

        head = ttk.Frame(root)
        head.pack(fill="x", pady=(0, 8))
        ttk.Label(head, text=APP_TITLE, font=("Segoe UI", 16, "bold")).pack(side="left")
        ttk.Button(head, text="Help", command=self.show_help).pack(side="right")

        box_outer = tk.Frame(root, background="#A7F3D0")
        box_inner = tk.Frame(box_outer, background="#ECFDF5")
        box_outer.pack(fill="x")
        box_inner.pack(fill="both", padx=2, pady=2)
        box = ttk.Frame(box_inner, padding=12)
        box.pack(fill="x")

        self.var_base = tk.StringVar()
        self.var_current = tk.StringVar()

        grid = ttk.Frame(box)
        grid.pack(fill="x")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        ttk.Label(grid, text="Reference (old)").grid(row=0, column=0, sticky="w", pady=(0,4))
        ttk.Label(grid, text="New (current)").grid(row=0, column=1, sticky="w", pady=(0,4))

        self.ent_base = ttk.Entry(grid, textvariable=self.var_base)
        self.ent_current = ttk.Entry(grid, textvariable=self.var_current)
        self.ent_base.grid(row=1, column=0, sticky="ew", padx=(0,8))
        self.ent_current.grid(row=1, column=1, sticky="ew", padx=(8,0))

        out_row = ttk.Frame(root)
        out_row.pack(fill="x", pady=12)
        self.lbl_out = ttk.Label(
            out_row,
            text="(your result will appear here)",
            font=("Consolas", 11),
            background="#F9FAFB"
        )
        self.lbl_out.pack(side="left", padx=(0,10), fill="x", expand=True)

        self.btn_copy = ttk.Button(out_row, text="Copy", command=self.copy_line, state="disabled")
        self.btn_copy.pack(side="left")

        foot = ttk.Label(
            root,
            text="Rounding: $ to whole dollars • % to whole percent • If reference = 0 → —%",
            foreground="#6B7280"
        )
        foot.pack(anchor="w", pady=(4,0))

        self.var_base.trace_add("write", self.update_line)
        self.var_current.trace_add("write", self.update_line)
        self.ent_base.focus_set()

    def show_help(self):
        messagebox.showinfo(APP_TITLE, HELP_TEXT)

    def compute_line(self):
        base_raw = strip_money(self.var_base.get())
        current_raw = strip_money(self.var_current.get())
        base_num = to_number(base_raw)
        current_num = to_number(current_raw)
        if any(x != x for x in (base_num, current_num)):
            return ""
        diff = current_num - base_num
        abs_diff_rounded = round(abs(diff))
        if base_num == 0:
            pct_str = "—%"
        else:
            pct = round((diff / base_num) * 100)
            pct_str = f"{pct}%"
        if diff > 0:
            return f"(increased by {fmt_no_cents(abs_diff_rounded)} or {pct_str})"
        elif diff < 0:
            return f"(decreased by {fmt_no_cents(abs_diff_rounded)} or {pct_str})"
        else:
            return "(no change)"

    def update_line(self, *args):
        line = self.compute_line()
        if line:
            self.lbl_out.config(text=line, background="#ECFDF5")
            self.btn_copy.config(state="normal")
        else:
            self.lbl_out.config(text="(your result will appear here)", background="#F9FAFB")
            self.btn_copy.config(state="disabled")

    def copy_line(self):
        line = self.lbl_out.cget("text")
        if not line or "appear here" in line:
            return
        try:
            self.clipboard_clear()
            self.clipboard_append(line)
        except Exception:
            pass

if __name__ == "__main__":
    App().mainloop()
