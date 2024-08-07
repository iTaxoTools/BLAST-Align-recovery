from __future__ import annotations

from pathlib import Path
from typing import Literal, NamedTuple

import pytest

from core import blastn_parse

TEST_DATA_DIR = Path(__file__).parent / Path(__file__).stem

class BlastnParseTest(NamedTuple):
    input_path: Path | str
    blast_result_path: Path | str
    output_path: Path | str
    database_name: str
    expected_output: str

    def validate(self, tmp_path: Path) -> None:
       input_path = TEST_DATA_DIR / self.input_path
       blast_result_path = TEST_DATA_DIR / self.blast_result_path
       output_path = tmp_path / self.output_path
       database_name = self.database_name
       expected_output = TEST_DATA_DIR / self.expected_output
       blastn_parse(
            str(input_path),
            str(blast_result_path),
            str(output_path),
            str(database_name)
        )

       assert output_path.exists()

       # Verify that the output matches the expected output
       with open(output_path, 'r') as output_file:
           output_data = output_file.read()

       with open(expected_output, 'r') as expected_file:
           expected_data = expected_file.read()

       assert output_data == expected_data
       print(f"Output matches expected output.")


# New blast tests
blastn_parse_tests = [
    BlastnParseTest(
       "Salamandra_testqueryfile.fas",
        "Salamandra_testqueryfile.out",
        "Salamandra_blastmatchesadded.out",
        "salamandra_db",
        "Salamandra_testqueryfile_expected.fas"
    ),
]

@pytest.mark.parametrize("test", blastn_parse_tests)
def test_museoscript(test: BlastnParseTest, tmp_path: Path) -> None:
    test.validate(TEST_DATA_DIR)