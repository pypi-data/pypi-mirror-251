def rcut(input_str:str, unwanted:str, check:bool=False) -> str:
    """
    right-cut (rcut). Trim the ending characters `unwanted` from the given `input_str`.
    - `input_str`: the input string
    - `unwanted`: the characters to be trimmed from the ending (see examples below to learn more)
    - `check`: if `True`, raise an exception (see below) if `input_str` does not end with `unwanted`
    - `ValueError` if `unwanted` is an empty string
    - `AssertionError` if `input_str` doesn't end with `unwanted` when `check` is `True`
    - `rcut('foo12', '12')` -> `'foo'`
    - `rcut('hi mom 123', ' 123')` -> `'hi mom'`
    - `rcut('hi mom', 'cool')` -> `'hi mom'`
    - the reason using `rcut` and not `rstrip` is because `'hi 12123'.rstrip('123')` will be `'hi '`
    """
    if unwanted == '': raise ValueError("rcut: `unwanted` shouldn't be an empty string.")
    if input_str.endswith(unwanted):
        return input_str[:-len(unwanted)]
    else:
        if check:
            raise AssertionError("rcut: the given `input_str` does not end with `unwanted`.")
        return input_str