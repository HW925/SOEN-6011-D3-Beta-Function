"""Accessible Tkinter interface for the Beta function calculator."""

import tkinter as tk
from tkinter import ttk

from beta_core import (
    InputValidationError,
    NumericRangeError,
    beta_function,
    is_finite,
)


def parse_positive_real(raw_value, field_name):
    """Convert GUI text to a finite positive float with a helpful error."""
    cleaned = raw_value.strip()
    if cleaned == "":
        raise InputValidationError(f"{field_name} is required.")

    try:
        value = float(cleaned)
    except ValueError as error:
        raise InputValidationError(
            f"{field_name} must be a real number, such as 2.5 or 1e-3."
        ) from error

    if not is_finite(value):
        raise InputValidationError(f"{field_name} must be finite.")
    if value <= 0.0:
        raise InputValidationError(f"{field_name} must be greater than zero.")
    return value


class BetaCalculatorApp:
    """Tkinter GUI for repeated Beta function calculations."""

    def __init__(self, root):
        self.root = root
        self.root.title("Beta Function Calculator")
        self.root.geometry("760x560")
        self.root.minsize(680, 500)

        self.x_text = tk.StringVar()
        self.y_text = tk.StringVar()
        self.result_text = tk.StringVar(value="Enter two positive real values.")
        self.status_text = tk.StringVar(value="Ready")

        self._configure_style()
        self._build_interface()
        self._bind_keyboard_actions()
        self.x_entry.focus_set()

    def _configure_style(self):
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 22, "bold"))
        style.configure("Subtitle.TLabel", font=("Arial", 11))
        style.configure("Result.TLabel", font=("Arial", 15, "bold"))
        style.configure("Error.TLabel", foreground="#9b1c1c")
        style.configure("Success.TLabel", foreground="#146c43")
        style.configure("TButton", padding=(12, 7))

    def _bind_keyboard_actions(self):
        self.root.bind("<Return>", self.calculate)
        self.root.bind("<Escape>", self.clear)
        self.root.bind("<Alt-x>", lambda _event: self.x_entry.focus_set())
        self.root.bind("<Alt-y>", lambda _event: self.y_entry.focus_set())

    def _build_interface(self):
        main_frame = ttk.Frame(self.root, padding=24)
        main_frame.pack(fill="both", expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)

        ttk.Label(
            main_frame,
            text="Beta Function Calculator",
            style="Title.TLabel",
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            main_frame,
            text="Compute B(x, y) for finite positive real inputs.",
            style="Subtitle.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(2, 18))

        input_frame = ttk.LabelFrame(main_frame, text="Inputs", padding=16)
        input_frame.grid(row=2, column=0, sticky="ew")
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)

        ttk.Label(input_frame, text="x (Alt+X)").grid(
            row=0,
            column=0,
            sticky="w",
        )
        self.x_entry = ttk.Entry(
            input_frame,
            textvariable=self.x_text,
            width=22,
        )
        self.x_entry.grid(row=0, column=1, sticky="ew", padx=(8, 18))

        ttk.Label(input_frame, text="y (Alt+Y)").grid(
            row=0,
            column=2,
            sticky="w",
        )
        self.y_entry = ttk.Entry(
            input_frame,
            textvariable=self.y_text,
            width=22,
        )
        self.y_entry.grid(row=0, column=3, sticky="ew", padx=(8, 0))

        button_frame = ttk.Frame(input_frame)
        button_frame.grid(
            row=1,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(14, 0),
        )
        ttk.Button(
            button_frame,
            text="Calculate",
            command=self.calculate,
        ).pack(side="left")
        ttk.Button(
            button_frame,
            text="Swap x and y",
            command=self.swap_inputs,
        ).pack(side="left", padx=8)
        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear,
        ).pack(side="left")

        result_frame = ttk.LabelFrame(
            main_frame,
            text="Result and status",
            padding=16,
        )
        result_frame.grid(row=3, column=0, sticky="ew", pady=14)
        ttk.Label(
            result_frame,
            textvariable=self.result_text,
            style="Result.TLabel",
        ).pack(anchor="w")
        self.status_label = ttk.Label(
            result_frame,
            textvariable=self.status_text,
        )
        self.status_label.pack(anchor="w", pady=(5, 0))

        history_frame = ttk.LabelFrame(
            main_frame,
            text="Calculation history",
            padding=10,
        )
        history_frame.grid(row=4, column=0, sticky="nsew")
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)

        self.history = ttk.Treeview(
            history_frame,
            columns=("x", "y", "result"),
            show="headings",
            height=7,
        )
        self.history.heading("x", text="x")
        self.history.heading("y", text="y")
        self.history.heading("result", text="B(x, y)")
        self.history.column("x", width=120, anchor="e")
        self.history.column("y", width=120, anchor="e")
        self.history.column("result", width=300, anchor="e")
        self.history.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            history_frame,
            orient="vertical",
            command=self.history.yview,
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.history.configure(yscrollcommand=scrollbar.set)

        ttk.Label(
            main_frame,
            text="Enter: calculate    Esc: clear    Alt+X / Alt+Y: focus input",
        ).grid(row=5, column=0, sticky="e", pady=(10, 0))

    def calculate(self, event=None):
        """Validate inputs, compute the result, and recover from errors."""
        del event
        try:
            x_value = parse_positive_real(self.x_text.get(), "x")
            y_value = parse_positive_real(self.y_text.get(), "y")
            result = beta_function(x_value, y_value)
        except InputValidationError as error:
            self.result_text.set("Input could not be accepted.")
            self.status_text.set(str(error))
            self.status_label.configure(style="Error.TLabel")
            return
        except NumericRangeError as error:
            self.result_text.set("Result is outside the supported range.")
            self.status_text.set(str(error))
            self.status_label.configure(style="Error.TLabel")
            return
        formatted_result = f"{result:.12g}"
        self.result_text.set(
            f"B({x_value:.12g}, {y_value:.12g}) = {formatted_result}"
        )
        self.status_text.set("Calculation completed.")
        self.status_label.configure(style="Success.TLabel")
        self.history.insert(
            "",
            0,
            values=(
                f"{x_value:.12g}",
                f"{y_value:.12g}",
                formatted_result,
            ),
        )

    def swap_inputs(self):
        """Exchange x and y to make symmetry easy to inspect."""
        first = self.x_text.get()
        self.x_text.set(self.y_text.get())
        self.y_text.set(first)
        self.status_text.set("Inputs swapped.")
        self.status_label.configure(style="TLabel")

    def clear(self, event=None):
        """Clear current inputs and messages without closing the application."""
        del event
        self.x_text.set("")
        self.y_text.set("")
        self.result_text.set("Enter two positive real values.")
        self.status_text.set("Ready")
        self.status_label.configure(style="TLabel")
        self.x_entry.focus_set()


def main():
    """Launch the standalone graphical application."""
    root = tk.Tk()
    BetaCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
