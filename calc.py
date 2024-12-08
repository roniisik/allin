def calc_deviation(data):
    expected_wins = sum(entry[0] for entry in data)
    actual_wins = 0
    for entry in data:
        if entry[1] == 'Win':
            actual_wins += 1
    
    deviation = actual_wins - expected_wins
    return round(deviation, 2)


def get_average_prob(data):
    if not data:
        return 0
    prob_sum = sum(entry[0] for entry in data)
    return prob_sum / len(data)
    
