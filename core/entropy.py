import math

def calculate_entropy(password: str):
    charset = 0

    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(not c.isalnum() for c in password):
        charset += 32

    entropy = len(password) * math.log2(charset) if charset else 0
    return round(entropy, 2)

def crack_time(entropy_bits):
    cpu_speed = 1e6      # guesses/sec
    gpu_speed = 1e9

    cpu_time = (2 ** entropy_bits) / cpu_speed
    gpu_time = (2 ** entropy_bits) / gpu_speed

    return round(cpu_time, 2), round(gpu_time, 2)
