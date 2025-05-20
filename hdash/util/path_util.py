"""Path Utility Class."""


class PathUtil:
    """Path Utility Class."""

    def truncate_path(self, path: str):
        """Truncate a path.

        For example, given:  em_level_1/008, return em_level_1.
        For example, given:  em_level_1/ohsu/008 return em_level_1/ohsu
        For example, given:  em_level_1 return ''
        """
        parts = path.split("/")
        parts = parts[0 : len(parts) - 1]
        new_path = str.join("/", parts)
        if len(new_path) > 0:
            return new_path + "/"
        return new_path
