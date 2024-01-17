class Calculator:
    """A simple calculator class."""

    def __init__(self) -> None:
        """Initialize the calculator with memory set to 0."""
        self.memory: float = 0

    def add(self, x: float) -> None:
        """
        Add a number to the memory.

        Args:
            x (float): The number to be added.
        """
        self.memory += x

    def subtract(self, x: float) -> None:
        """
        Subtract a number from the memory.

        Args:
            x (float): The number to be subtracted.
        """
        self.memory -= x

    def multiply(self, x: float) -> None:
        """
        Multiply the memory by a given number.

        Args:
            x (float): The number to multiply the memory by.
        """
        self.memory *= x

    def divide(self, x: float) -> None:
        """
        Divide the memory by a given number.

        Args:
            x (float): The number to divide the memory by.

        Raises:
            ValueError: If the divisor is 0.
        """
        if x != 0:
            self.memory /= x
        else:
            raise ValueError("Cannot divide by zero.")

    def root(self, n: float) -> None:
        """
        Take the nth root of the number in memory.

        Args:
            n (float): The root to be taken.

        Raises:
            ValueError: If the memory is a negative number.
        """
        if self.memory >= 0:
            self.memory **= (1 / n)
        else:
            raise ValueError("Cannot calculate the root of a negative number.")

    def reset(self) -> None:
        """Reset the memory to 0."""
        self.memory = 0
