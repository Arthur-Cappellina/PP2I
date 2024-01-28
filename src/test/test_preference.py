import modules.accueil as accueil
import string 
import random
import matplotlib.pyplot as plt
import time as time

def test_same():
    (data1, data2) = ({'fruits': 1, 'légumes': 1}, {'fruits': 1, 'légumes': 1})
    assert accueil.get_score_from_type(data1, data2, 2) == 1

def test_different():
    (data1, data2) = ({'fruits': 2}, {'légumes': 5})
    assert accueil.get_score_from_type(data1, data2, 2) == 0

def test_vide():
    (data1, data2) = ({}, {'légumes': 5})
    assert accueil.get_score_from_type(data1, data2, 2) == 0

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def get_random(iterations, p=2): 
    data1 = {}
    data2 = {}
    sum = 0
    for _ in range(iterations):
        ran_s = get_random_string(p)
        ran_size = random.randint(1,50)
        if ran_s not in data1:
            data1[ran_s] = ran_size
        sum += ran_size
        ran_s = get_random_string(p)
        ran_size = random.randint(1,50)
        if ran_s not in data2:
            data2[ran_s] = ran_size
    return (data1, data2, sum)

def test_random():
    (data1, data2, sum) = get_random(900)
    assert accueil.get_score_from_type(data1, data2, sum) >= 0 and accueil.get_score_from_type(data1, data2, sum) <= 1

def performance():
    times = []
    iterations = []
    for i in range(1, 300000, 30000):
        (data1, data2, sum) = get_random(i,50)
        start = time.time()
        accueil.get_score_from_type(data1, data2, sum)
        end = time.time()
        times.append(end - start)
        iterations.append(i)
    plt.plot(iterations, times)
    plt.show()

performance()
