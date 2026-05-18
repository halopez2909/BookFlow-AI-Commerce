from typing import List
from app.domain.entities import NormalizedRecord
from app.domain.normalizers import TitleNormalizer, AuthorNormalizer, ISBNValidator, ISSNValidator
from app.domain.duplicate_detector import DuplicateDetector
from app.domain.repositories import NormalizedRecordRepository
from app.domain.schemas import EnrichmentResultInput


class NormalizationPipeline:
    def __init__(self):
        self.title_normalizer = TitleNormalizer()
        self.author_normalizer = AuthorNormalizer()
        self.isbn_validator = ISBNValidator()
        self.issn_validator = ISSNValidator()

    def run(self, input_data: EnrichmentResultInput, duplicate_detector: DuplicateDetector) -> NormalizedRecord:
        normalized_title = self.title_normalizer.normalize(input_data.title)
        normalized_author = self.author_normalizer.normalize(input_data.author)
        isbn_valid = self.isbn_validator.validate(input_data.isbn)
        issn_valid = self.issn_validator.validate(input_data.issn)
        is_duplicate, duplicate_of_id = duplicate_detector.detect(input_data.isbn)

        return NormalizedRecord.create(
            enrichment_result_id=input_data.enrichment_result_id,
            normalized_title=normalized_title,
            normalized_author=normalized_author,
            normalized_isbn=input_data.isbn,
            isbn_valid=isbn_valid,
            issn_valid=issn_valid,
            is_duplicate=is_duplicate,
            duplicate_of_id=duplicate_of_id,
        )


class NormalizeRecord:
    def __init__(self, repository: NormalizedRecordRepository, duplicate_detector: DuplicateDetector):
        self.repository = repository
        self.duplicate_detector = duplicate_detector
        self.pipeline = NormalizationPipeline()

    def execute(self, input_data: EnrichmentResultInput) -> NormalizedRecord:
        record = self.pipeline.run(input_data, self.duplicate_detector)
        return self.repository.save(record)


class NormalizeBatch:
    def __init__(self, repository: NormalizedRecordRepository, duplicate_detector: DuplicateDetector):
        self.repository = repository
        self.duplicate_detector = duplicate_detector
        self.pipeline = NormalizationPipeline()

    def execute(self, inputs: List[EnrichmentResultInput]) -> List[NormalizedRecord]:
        results = []
        for input_data in inputs:
            record = self.pipeline.run(input_data, self.duplicate_detector)
            saved = self.repository.save(record)
            results.append(saved)
        return results


class GetRecords:
    def __init__(self, repository: NormalizedRecordRepository):
        self.repository = repository

    def execute(self) -> List[NormalizedRecord]:
        return self.repository.find_all()
