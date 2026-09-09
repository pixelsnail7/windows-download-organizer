class Pencil:
    @classmethod
    def _perform_write(cls, file_name: str, text: str, mode: str) -> str:
        try:
            with open(file_name, mode, encoding="utf-8") as file:
                file.write(text)
            return "success"
        except OSError:
            return "failed"

    @classmethod
    def rewrite(cls, file_name: str = "example.txt", text: str = "Pencil.") -> str:
        return cls._perform_write(file_name, text, "w")

    @classmethod
    def add(cls, file_name: str = "example.txt", text: str = "Pencil.") -> str:
        return cls._perform_write(file_name, text, "a")

