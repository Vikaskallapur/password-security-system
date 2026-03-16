def simulate_attack(entropy_bits):
    gpu_speed = 1e9  # guesses/sec
    estimated_time = (2 ** entropy_bits) / gpu_speed

    if estimated_time < 60:
        return "Extremely weak (seconds)"
    elif estimated_time < 3600:
        return "Weak (minutes)"
    elif estimated_time < 86400:
        return "Moderate (hours)"
    else:
        return "Strong (days/years)"
