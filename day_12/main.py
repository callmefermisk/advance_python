import asyncio, time

# Simulates a store that replies after some seconds
async def get_price(store, seconds, price):
    await asyncio.sleep(seconds)

    if price is None:
        raise Exception("the price is none")

    return price

async def main():
    # Start the timer
    start_time = time.perf_counter()

    store_names = ["barber", "bakery", "restaurant"]

    # Run all three stores at the same time
    result = await asyncio.gather(
        get_price("barber", 2, 120),
        get_price("bakery", 1, 20),
        get_price("restaurant", 2, None),  # fails on purpose
        return_exceptions=True,
    )

    # Total time
    end_time = time.perf_counter()
    print(f"total time is {end_time - start_time:.1f} seconds")

    # Print each result
    for i, item in enumerate(result):
        if isinstance(item, Exception):
            print(f"{store_names[i]} error: {item}")
        else:
            print(f"{store_names[i]} price: {item}")

    # Find the lowest successful price
    prices = []
    for item in result:
        if not isinstance(item, Exception):
            prices.append(item)

    if prices:
        print("lowest price:", min(prices))
    else:
        print("no successful prices")

# Entry point for a .py file
asyncio.run(main())