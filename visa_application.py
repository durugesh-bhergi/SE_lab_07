import math


def parse_application(text):
    """
    Parses visa type and number of entries from a 'visa:entries' formatted string.
    Hardened against: None, non-strings, missing colons, multiple colons,
    empty visa names, invalid non-integer entries, and negative entries.
    Returns:
        tuple (str, int) if valid, or None if invalid.
    """
    if not text or not isinstance(text, str):
        return None
    if ":" not in text:
        return None
    parts = text.split(":")
    if len(parts) != 2:
        return None
    visa, entries = parts[0].strip(), parts[1].strip()
    if not visa:
        return None
    try:
        val = int(entries)
        if val < 0:
            return None
        return visa.title(), val
    except (ValueError, TypeError):
        return None


def processing_average(days_csv):
    """
    Computes the integer average of processing days from a comma-separated string.
    Hardened against: None, non-strings, empty strings, missing elements (e.g. '1,,3'),
    non-integer tokens, negative numbers, and ZeroDivisionError.
    Returns:
        int representing the integer average, or 0 if no valid entries exist.
    """
    if not days_csv or not isinstance(days_csv, str):
        return 0
    values = []
    for r in days_csv.split(","):
        clean = r.strip()
        if not clean:
            continue
        try:
            v = int(clean)
            if v >= 0:
                values.append(v)
        except (ValueError, TypeError):
            continue
    if not values:
        return 0
    return sum(values) // len(values)


def payable_fee(text):
    """
    Calculates total payable fee applying 18% tax (1.18x) and subtracting discount.
    Format: 'fee|discount'
    Hardened against: None, non-strings, missing pipes, multiple pipes,
    non-numeric tokens, NaN/Inf, negative values, and overflows.
    Returns:
        float representing payable fee, minimum 0.0.
    """
    if not text or not isinstance(text, str):
        return 0.0
    if "|" not in text:
        return 0.0
    parts = text.split("|")
    if len(parts) != 2:
        return 0.0
    try:
        fee_str, discount_str = parts[0].strip(), parts[1].strip()
        fee = float(fee_str)
        discount = float(discount_str)
        if math.isnan(fee) or math.isinf(fee) or math.isnan(discount) or math.isinf(discount):
            return 0.0
        if fee < 0 or discount < 0:
            return 0.0
        total = fee * 1.18 - discount
        return max(float(total), 0.0)
    except (ValueError, TypeError, OverflowError):
        return 0.0


def main():
    print("==== Running parse_application ====")
    user_input = input("Enter visa type:entries (e.g. tourist:2): ")
    result = parse_application(user_input)
    print("Visa Type and Entries:", result)

    print("\n==== Running processing_average ====")
    user_input = input("Enter processing days as CSV (e.g. 5,10,21): ")
    result = processing_average(user_input)
    print("Average Processing Days:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 6000|500): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result)


if __name__ == "__main__":
    main()
