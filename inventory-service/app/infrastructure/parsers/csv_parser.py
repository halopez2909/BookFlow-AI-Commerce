import io
import pandas as pd
from typing import List
from app.infrastructure.parsers.base_parser import FileParser


class CSVParser(FileParser):

    def parse(self, file_bytes: bytes) -> List[dict]:
        df = pd.read_csv(io.BytesIO(file_bytes))
        df = df.where(pd.notnull(df), None)
        return df.to_dict(orient="records")
