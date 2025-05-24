from random import uniform


class DummyStrategy:
    def generate_signal(self) -> str:
        # Random fake logic
        price = round(uniform(10000, 10500), 2)
        print(f"[DUMMY STRATEGY] Price: ${price}")
        return "buy" if price < 10200 else "hold"
