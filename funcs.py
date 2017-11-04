def _chunks(s, n):
    """Produce `n`-character chunks from `s`."""
    for start in range(0, len(s), n):
        yield s[start:start+n]

def chunks(s, n):
    return list(_chunks(s, n))
