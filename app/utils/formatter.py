"""Utility functions for string formatting."""


def format_error(e: Exception, title: str = "Error") -> str:
    """
    Format an exception into a nicely indented, multi-line error block.

    Example output:

        Error:
            <exception message line 1>
            <exception message line 2>

    Args:
        e (Exception): Exception to format.
        title (str, optional): Title to display before the error message. Defaults to "Error".

    Returns:
        str: Formatted, multi-line error string.
    """
    msg = str(e).replace("\n", "\n    ")

    return f"\n    {title}:\n    {msg}"
