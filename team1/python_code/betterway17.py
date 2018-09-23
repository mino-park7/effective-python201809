def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * float(value) / total
        result.append(percent)
    return result

visits = [15, 34, 53, 25, 17, 194]
percentages = normalize(visits)
print(percentages)



def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)


it = read_visits('./my_numbers.txt')
percentages = normalize(it)
print(percentages)


it2 = read_visits('./my_numbers.txt')
print(list(it2))
print(list(it2))


def normalize_copy(numbers):
    numbers = list(numbers)
    total = float(sum(numbers))
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

it3 = read_visits('./my_numbers.txt')
percentages = normalize_copy(it3)
print(percentages)
