from typing import Union


def _get_price_for_renting(number_of_players: Union[str, int], duration_in_hours: float) -> int:
    price_per_hour = 500 + 100 * int(number_of_players)
    total_price = price_per_hour * duration_in_hours
    return int(total_price)
