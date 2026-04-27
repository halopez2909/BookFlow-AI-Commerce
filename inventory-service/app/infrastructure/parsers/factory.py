from app.infrastructure.parsers.base_parser import FileParser
from app.infrastructure.parsers.xls_parser import XLSParser
from app.infrastructure.parsers.csv_parser import CSVParser


class FileParserFactory:

    @staticmethod
    def get_parser(extension: str) -> FileParser:
        ext = extension.lower().strip(".")
        if ext in ("xls", "xlsx"):
            return XLSParser()
        elif ext == "csv":
            return CSVParser()
        raise ValueError(f"UNSUPPORTED_FORMAT:{extension}")
