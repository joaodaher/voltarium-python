"""CCEE consumer unit code generation with valid check digits.

The consumer unit code (código da unidade consumidora) follows ANEEL
Resolution 1095/2024. It consists of 15 digits:

    N15 N14 N13 N12 N11 N10 N9 N8 N7 N6 N5 N4 N3 N2 N1
    |----- 10 sequential digits -----| |-- 3 --| |2 chk|

- N15–N6: 10-digit sequential number assigned by the distributor
- N5–N3 : 3-digit distributor code (assigned by ANEEL)
- N2–N1 : 2 check digits (modulo-11, per Annex II)
"""


def generate_consumer_unit_code(base: str) -> str:
    """Generate a valid 15-digit CCEE consumer unit code.

    Args:
        base: Up to 13 digits used as the base (zero-padded on the left).
              Typically built from a utility agent code + a unique suffix,
              e.g. ``f"{utility.agent_code}{suffix}"``.

    Returns:
        A 15-character numeric string with two valid check digits appended.
    """
    base13 = base.zfill(13)[:13]
    digits = [int(d) for d in base13]

    # N2 – first check digit (weights applied to N15…N3)
    weights_n2 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 10, 9, 8]
    remainder = sum(d * w for d, w in zip(digits, weights_n2, strict=True)) % 11
    n2 = 0 if remainder < 2 else 11 - remainder

    # N1 – second check digit (weights applied to N15…N2, includes N2)
    digits_14 = [*digits, n2]
    weights_n1 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 10, 9, 8]
    remainder = sum(d * w for d, w in zip(digits_14, weights_n1, strict=True)) % 11
    n1 = 0 if remainder < 2 else 11 - remainder

    return base13 + str(n2) + str(n1)
