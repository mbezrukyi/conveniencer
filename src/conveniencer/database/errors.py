class NoDocumentError(ValueError):
    def __init__(self, desc: str = "No document was found."):
        super().__init__(desc)

        self._desc = desc

    def __str__(self):
        return f"NoDocumentError: {self._desc}"
