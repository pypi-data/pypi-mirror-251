def time_quick(secs: float, /) -> str:
    """
    Convert seconds into minutes-seconds concise-look style
    - `secs`: in seconds (>= 0)
    - `quick(61.25)` -> `'1m1.2s'`
    """
    m, s = divmod(abs(secs), 60)
    return f'{int(m)}m{s:.1f}s'