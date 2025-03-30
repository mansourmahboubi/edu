class BSTNode:
    def __init__(self, value, right=None, left=None):
        self.value = value
        self.right = right
        self.left = left

    def insert(self, value):
        if value < self.value:
            if self.left is None:
                self.left = BSTNode(value)
            else:
                self.left.insert(value)
        else:
            if self.right is None:
                self.right = BSTNode(value)
            else:
                self.right.insert(value)

    def display(self) -> None:
        lines, *_ = self.display_aux()
        for line in lines:
            print(line)

    def display_aux(self):
        """
        Some external code


        Returns list of strings, width, height, and horizontal coordinate of the root.
        """
        # No child.
        if self.right is None and self.left is None:
            line = f"{self.value}"
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left.display_aux()  # type: ignore
            val_str = f"{self.value}"
            val_len = len(val_str)
            first_line = (x + 1) * " " + (n - x - 1) * "_" + val_str
            second_line = x * " " + "/" + (n - x - 1 + val_len) * " "
            shifted_lines = [
                line + val_len * " " for line in lines
            ]  # Shift all the lines we have already to the left
            return (
                [first_line, second_line] + shifted_lines,
                n + val_len,
                p + 2,
                n + val_len // 2,
            )

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right.display_aux()
            val_str = f"{self.value}"
            val_len = len(val_str)
            first_line = val_str + x * "_" + (n - x) * " "
            second_line = (val_len + x) * " " + "\\" + (n - x - 1) * " "
            shifted_lines = [
                val_len * " " + line for line in lines
            ]  # Shift all the lines we have already to the right
            return (
                [first_line, second_line] + shifted_lines,
                n + val_len,
                p + 2,
                val_len // 2,
            )

        # Two children.
        left, n, p, x = self.left.display_aux()
        right, m, q, y = self.right.display_aux()
        val_str = f"{self.value}"
        val_len = len(val_str)
        first_line = (
            (x + 1) * " " + (n - x - 1) * "_" + val_str + y * "_" + (m - y) * " "
        )
        second_line = (
            x * " " + "/" + (n - x - 1 + val_len + y) * " " + "\\" + (m - y - 1) * " "
        )
        if p < q:
            left += [n * " "] * (q - p)
        elif q < p:
            right += [m * " "] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [
            a + val_len * " " + b for a, b in zipped_lines
        ]
        return (
            lines,
            n + m + val_len,
            max(p, q) + 2,
            n + val_len // 2,
        )
