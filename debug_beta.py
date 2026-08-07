"""Small driver used only to demonstrate pdb on the Beta calculation."""

from beta_core import beta_function


def main():
    """Evaluate one known value while a debugger inspects the core."""
    result = beta_function(2.0, 3.0)
    print(f"B(2, 3) = {result:.15g}")


if __name__ == "__main__":
    main()
