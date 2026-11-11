
def clean_pan(pan):
    """
    Removes spaces from a PAN and converts it to uppercase.
    Returns an empty string for invalid input.
    """
    if not isinstance(pan, str):
        return ""

    return pan.strip().replace(" ", "").upper()


def parse_amount(text):
    """
    Converts an amount such as 'Rs 12,50,000' into an integer.
    Returns None for invalid input.
    """
    if not isinstance(text, str):
        return None

    text = text.strip()

    if not text:
        return None

    text = text.replace("Rs", "").replace("rs", "")
    text = text.replace(",", "").replace(" ", "").strip()

    if not text.isdigit():
        return None

    return int(text)


def parse_tax_slab(line):
    """
    Parses 'LOW-HIGH:RATE' into a (low, high, rate) tuple.
    Returns None for invalid input.
    """
    if not isinstance(line, str):
        return None

    try:
        limits, rate = line.split(":")
        low, high = limits.split("-")

        low = int(low.strip())
        high = int(high.strip())
        rate = int(rate.strip())

        if low < 0 or high < 0 or rate < 0:
            return None

        if low > high:
            return None

        return low, high, rate

    except (ValueError, AttributeError):
        return None


def main():
    print("==== Running clean_pan ====")
    value = input("Enter a PAN (e.g. abcde 1234f): ")
    print("Cleaned PAN:", clean_pan(value))

    print("\n==== Running parse_amount ====")
    value = input("Enter an amount (e.g. Rs 12,50,000): ")
    result = parse_amount(value)
    print("Amount in rupees:", result)

    print("\n==== Running parse_tax_slab ====")
    value = input("Enter a tax slab as LOW-HIGH:RATE (e.g. 250000-500000:5): ")
    result = parse_tax_slab(value)
    print("Tax slab (low, high, rate):", result)


if __name__ == "__main__":
    main()
