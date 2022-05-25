class Numerical:
    def __int__(self):
        raise Exception("Called non-overridden method __int__ of pure Numerical class."
                        "Method __int__ should be overridden in derived classes.")
