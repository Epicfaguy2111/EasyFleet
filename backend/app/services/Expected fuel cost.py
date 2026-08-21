"""Simple fuel usage and trip cost calculator."""


def read_positive_float(prompt, allow_zero=False):
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            value = float(raw)
        except ValueError:
            print("Please enter a valid number.")
            continue

        if value < 0 or (value == 0 and not allow_zero):
            print("Please enter a value greater than 0.")
            continue

        return value


def calculate_fuel_usage(distance_km, fuel_use_per_100_km):
    litres_used = distance_km * (fuel_use_per_100_km / 100)
    return litres_used


def calculate_cost(litres_used, price_per_litre):
    return litres_used * price_per_litre


def main():
    print("=" * 45)
    print("FUEL USAGE AND COST CALCULATOR")
    print("=" * 45)

    price_per_litre = read_positive_float("Enter fuel price per litre: ")
    distance_km = read_positive_float("Enter distance to travel in km: ", allow_zero=True)
    fuel_use_per_100_km = read_positive_float("Enter fuel use per 100 km: ")

    litres_used = calculate_fuel_usage(distance_km, fuel_use_per_100_km)
    total_cost = calculate_cost(litres_used, price_per_litre)

    print("\nResults:")
    print(f"Fuel used: {litres_used:.2f} litres")
    print(f"Estimated cost: {total_cost:.2f}")


if __name__ == "__main__":
    main()