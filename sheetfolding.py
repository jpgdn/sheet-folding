# Optimal sheet folding

def main():
    print("Optimal sheet folding")
    drawer = (23, 55)
    my_folds = [2, 3]
    sheet_folder = SheetFolder(drawer, my_folds, verbose=True)
    print(sheet_folder)
    sheet = (200, 140)
    sheet_folder.fold(sheet)


class SheetFolder:
    def __init__(self, drawer: tuple[float, float], my_folds: list, verbose=False):
        """
        Optimal sheet folding
        :param drawer: Length and width of drawer
        :param my_folds: Folds to explore (list of primes)
        """
        self.drawer = drawer
        self.primes = list(my_folds)
        self.verbose = verbose

    def __str__(self):
        return f"Drawer: {self.drawer}  Folds: {self.primes}"

    def fold(self, sheet: tuple[float, float]):
        """
        Optimal sheet folding
        :param sheet: Length and width of sheet
        """
        factors = [0, 0]

        # Fold option 1
        best_paths = []  # Fold paths for length and width
        min_layers = 1   # Total number of layers of folded sheet
        for i in range(2):  # Fold each side of the sheet
            factors[i], path = self._fold1d_(sheet[i], self.drawer[i], self.verbose)
            best_paths.append(path)
            min_layers *= factors[i]
        best_factors = list(factors)

        # Fold option 2: Rotate drawer 90 degrees
        paths = []
        layers = 1
        for i in range(2):  # Fold the two sides of the sheet
            factors[i], path = self._fold1d_(sheet[i], self.drawer[i - 1], self.verbose)
            paths.append(path)
            layers *= factors[i]
        if layers < min_layers:
            # Option 2 was better
            min_layers = layers
            best_paths = list(paths)
            best_factors = list(factors)

        folded_sheet = [sheet[i] / best_factors[i] for i in range(2)]
        for i in range(2):
            print(f'Fold {sheet[i]:1.1f} --> {best_paths[i]} --> ' +
                  f'{folded_sheet[i]:1.1f} ({best_factors[i]} layers)')
        spill = 1 - (folded_sheet[0] * folded_sheet[1]) / (self.drawer[0] * self.drawer[1])
        print(f'{min_layers} layers, spill {spill:1.1%}')

        return

    def _fold1d_(self, s: float, d: float, verbose: bool = False) -> tuple[float, list]:
        """
        Recursive folding of one side of the sheet
        :param s: Length of sheet
        :param d: Length of drawer
        :param verbose: Print tracing information
        :return: Optimal fold factor, fold path
        """
        target = s / d  # Used as a constant in fold1d_body()

        def fold1d_body(factor: int, children: list, cur_path: list = None, indent: int = 0
                        ) -> tuple[int, list]:
            indent += 4
            best_path = cur_path
            best_factor = factor
            if verbose:
                print(f"{indent * ' '}Visiting node: {cur_path} Factor: {factor} {'***' if factor > target else ''}")

            if factor < target:
                # Sheet is too large - fold by visiting child nodes
                for i in range(len(children)):
                    c = children[i]
                    child_path = cur_path + [c]
                    n, child_path = fold1d_body(factor * c, children[i:], child_path, indent)
                    if i == 0 or n < best_factor:  # Smallest fold factor so far
                        best_factor = n
                        best_path = child_path
                if verbose:
                    print(f"{indent * ' '}Best factor from this node: {best_factor}" +
                          f" Path: {best_path}")
            return best_factor, best_path

        if verbose:
            print(f"Target: {target:1.2f}")
        return fold1d_body(1, self.primes, [])


if __name__ == '__main__':
    main()
