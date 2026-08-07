"""Launch a populated GUI state for the poster demonstration screenshot."""

import tkinter as tk

from beta_function_gui import BetaCalculatorApp


def main():
    """Show one known-value calculation in the real application."""
    root = tk.Tk()
    app = BetaCalculatorApp(root)
    app.x_text.set("2")
    app.y_text.set("3")
    app.calculate()
    root.mainloop()


if __name__ == "__main__":
    main()
