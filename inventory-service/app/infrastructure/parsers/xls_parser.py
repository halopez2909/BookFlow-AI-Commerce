import io
import pandas as pd
from typing import List
from app.infrastructure.parsers.base_parser import FileParser


class XLSParser(FileParser):

    def parse(self, file_bytes: bytes) -> List[dict]:
        df = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")
        df = df.where(pd.notnull(df), None)
        return df.to_dict(orient="records")
