from pathlib import Path
from hien_logger import get_formatted_logger


def test_logger():
    logger = get_formatted_logger("hien_logger")
    logger.info("Hello, World!")
    assert True


def test_logger_file():
    logger = get_formatted_logger("hien_logger", file_path="test.log")
    logger.info("Hello, World!")
    assert Path("test.log").exists()

    with open("test.log", "r") as f:
        assert "Hello, World!" in f.read()


def test_logger_with_folder():
    logger = get_formatted_logger("hien_logger", file_path="logs/test.log")
    logger.info("Hello, World!")
    assert Path("logs/test.log").exists()

    with open("logs/test.log", "r") as f:
        assert "Hello, World!" in f.read()


def test_global_log_file():
    logger = get_formatted_logger("hien_logger", global_file_log=True)

    logger.info("Hello, World!")
    assert Path("logs/global.log").exists()

    with open("logs/global.log", "r") as f:
        assert "Hello, World!" in f.read()
