from app.infrastructure.parsers.factory import FileParserFactory


def test_factory_returns_xls_parser():
    parser = FileParserFactory.get_parser("xlsx")
    assert parser is not None


def test_factory_returns_csv_parser():
    parser = FileParserFactory.get_parser("csv")
    assert parser is not None


def test_factory_raises_for_unsupported():
    try:
        FileParserFactory.get_parser("pdf")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
