"""Check file names against Cancer Data Service (CDS) conventions."""

import re


class CdsFileNameChecker:
    """CDS File Name Checker."""

    pattern = re.compile(r"^[a-zA-Z0-9._-]+$")

    def is_file_name_valid(self, file_name: str):
        """Determine if file name is valid, as per CDS conventions."""
        return self.pattern.match(file_name) is not None
