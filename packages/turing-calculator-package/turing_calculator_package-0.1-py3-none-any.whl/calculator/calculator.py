class Calculator:
    def __init__(self) -> None:
        self.memory: float = 0

    def add(self, x: float) -> None:
        """Addition operation."""
        self.memory += x

    def subtract(self, x: float) -> None:
        """Subtraction operation."""
        self.memory -= x

    def multiply(self, x: float) -> None:
        """Multiplication operation."""
        self.memory *= x

    def divide(self, x: float) -> None:
        """Division operation."""
        if x != 0:
            self.memory /= x
        else:
            raise ValueError("Cannot divide by zero.")

    def root(self, n: float) -> None:
        """Take (n) root of the number."""
        if self.memory >= 0:
            self.memory **= (1/n)
        else:
            raise ValueError("Cannot calculate the root of a negative number.")

    def reset(self) -> None:
        """Reset memory to 0."""
        self.memory = 0
