def __round_hypo_retourned_value__(value):
    if (round(value, 3) >= round(6.0, 3)):
        return 0.02
    if (round(value, 3) >= round(5.0, 3)):
        return 0.025
    if (round(value, 3) < round(5.0, 3)):
        return 0.03


def __custom_range__(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step


def __rent_pourcentage_calculation__(first_hypo_value, second_hypo_value):
    min_value = min(first_hypo_value, second_hypo_value)
    max_value = max(first_hypo_value, second_hypo_value)
    step = 0.25
    rent_mortage_value = 0

    for i in __custom_range__(min_value, max_value, step):
        rent_mortage_value += __round_hypo_retourned_value__(i)
        print(rent_mortage_value)

    if (first_hypo_value == max_value):
        rent_mortage_value = -rent_mortage_value/(1 + rent_mortage_value)

    return round(rent_mortage_value * 100, 2)
