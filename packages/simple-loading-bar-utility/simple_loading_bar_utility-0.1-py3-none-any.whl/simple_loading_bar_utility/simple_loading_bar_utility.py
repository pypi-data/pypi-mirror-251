def loading_bar(i, total, length=50, show_percentage=True, show_iterations=True):
    """
    Prints a customizable loading bar to the console with error handling and optional indicators.
    
    Args:
        i (int): Current iteration.
        total (int): Total iterations.
        length (int): Length of the loading bar (default is 50).
        show_percentage (bool): Flag to show or hide percentage (default is True).
        show_iterations (bool): Flag to show or hide iterations completed (default is True).
        
    Raises:
        ValueError: If inputs are not integers, 'i' is out of range, 'total' is zero, 'length' is invalid, or if
                    'show_percentage' or 'show_iterations' are not boolean.
    """
    # Validate inputs
    if not all(isinstance(arg, int) for arg in [i, total, length]):
        raise ValueError("Arguments 'i', 'total', and 'length' must be integers.")
    
    if not all(isinstance(arg, bool) for arg in [show_percentage, show_iterations]):
        raise ValueError("'show_percentage' and 'show_iterations' must be boolean.")

    if i < 0 or i >= total:
        raise ValueError("'i' must be in the range from 0 to 'total - 1'.")

    if total <= 0:
        raise ValueError("'total' must be a positive integer.")

    if length <= 0:
        raise ValueError("'length' must be a positive integer.")

    # Calculate percentage and bar length
    percent = (i + 1) / total * 100
    filled_length = int(length * (i + 1) // total)
    bar = '█' * filled_length + '-' * (length - filled_length)

    # Construct the output string
    output = f"\r[{bar}]"
    if show_iterations:
        output += f" {i + 1}/{total}"
    if show_percentage:
        output += f" ({percent:.2f}%)"

    # Print the loading bar
    print(output, end="")