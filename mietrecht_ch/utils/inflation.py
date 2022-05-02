def __round_inflation_number__(old_index_value, new_index_value, percentage_of_inflation_to_use = 100):
    number_not_rounded = (new_index_value - old_index_value) / \
        (old_index_value) * int(percentage_of_inflation_to_use)
    number_rounded = round(number_not_rounded, 2)
    return number_rounded