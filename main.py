import math
import random
import matplotlib.pyplot as plt
import copy

with open("input.txt", "r") as file:
    input = file.readline
    population_size: int = int(input())

    (left_limit, right_limit) = input().split()
    left_limit: float = float(left_limit)
    right_limit: float = float(right_limit)

    (a, b, c) = input().split()

    a: float = float(a)
    b: float = float(b)
    c: float = float(c)

    precision: int = int(input())
    cross_over_probability: float = float(input())
    mutation_probability: float = float(input())
    number_of_generations: int = int(input())

population: list[list[int]] = []


def f(x: float) -> float:
    global a, b, c
    global left_limit, right_limit
    if x > right_limit:
        return 0
    y = a * x ** 2 + b * x + c
    return y

max_point_y = f(-b/(2*a))
print(max_point_y)

#   Numarul de biti pe care se face codificarea
list_len: int = math.ceil(math.log2(right_limit - left_limit) + precision * math.log2(10))

d: float = (right_limit - left_limit) / (2**list_len)

sub_intervals: list[float] = []
for i in range(2**list_len + 1):
    sub_intervals.append(a + i * d)

def binSearch(x: float, v: list) -> int:
    st = 1
    dr = len(v) - 1

    while st <= dr:
        mij = (st + dr) // 2
        if v[mij] == x:
            return mij
        if v[mij] > x:
            dr = mij - 1
        else:
            st = mij + 1
    return dr

def codify_individual(individual: float) -> list[int]:
    global list_len
    individual_code = binSearch(individual, sub_intervals)
    individual_code = format(individual_code, f"0{list_len+2}b")
    return [int(x) for x in individual_code[2:]]

def decode_individual(individual: list[int]) -> float:
    global sub_intervals
    individual = int("".join([str(x) for x in individual]), 2)
    return sub_intervals[individual]

def generate_population():
    global population, population_size, left_limit, right_limit

    for _ in range(population_size):
        individ = random.uniform(left_limit, right_limit)
        population.append(codify_individual(individ))

val_maxim: list[float] = []
val_mediu: list[float] = []
with open("evolutie.txt", "w") as file:
    printt = print
    print = file.write

    generate_population()

    for generation in range(number_of_generations):
        print(f"Generatia {generation + 1}:\n")
        print("Populatia initiala:\n")
        sum: int = 0
        maxim = f(decode_individual(population[0]))
        fittest = copy.deepcopy(population[0])
        for i in range(population_size):
            x = decode_individual(population[i])
            if f(x) > maxim:
                fittest = copy.deepcopy(population[i])
                maxim = f(x)
            print(f"\t{i + 1}: {''.join([str(x) for x in population[i]])}\tx=\t{x}\tf(x)= {f(x)}\n")
            sum += f(x)

        roulete: list[float] = [0]
        print("\nProbabilitati selectie:\n")
        for i in range(population_size):
            x = decode_individual(population[i])
            probability = f(x) / sum
            roulete.append(roulete[i] + probability)
            print(f"cromozom\t{i + 1}: probabilitate {probability}\n")

        print("\nIntervale probabilitati selectie:\n")
        for prob in roulete:
            print(f"{prob}\n")

        print("\nDupa selectie:\n")
        new_population: list[list[int]] = []
        for _ in range(population_size-1):
            r = random.uniform(0, 1)
            individ = binSearch(r, roulete)
            new_population.append(population[individ])
            print(f"u={r} selectam cromozomul {individ+1}\n")

        print("\nDupa selectie:\n")
        for i in range(population_size-1):
            x = decode_individual(new_population[i])
            print(f"\t{i + 1}: {''.join([str(x) for x in population[i]])}\tx=\t{x}\tf(x)= {f(x)}\n")
        # print(f"\t{i}: {''.join([str(x) for x in fittest])}\tx=\t{decode_individual(fittest)}\tf(x)= {f(decode_individual(fittest))}\n")

        print(f"\nProbabilitatea de incrucisare {cross_over_probability}:\n")
        to_cross_over: list[(int, list[int])]= []
        for i in range(population_size-1):
            r = random.uniform(0, 1)
            print(f"\t{i + 1}: {''.join([str(x) for x in population[i]])}\tu={r}")
            if r < cross_over_probability:
                to_cross_over.append((i+1, new_population[i]))
                print(f"<{cross_over_probability} participa")
            print("\n")

        if len(to_cross_over) % 2 and len(to_cross_over) > 1:
            break_point = random.randint(1, list_len-1)
            temp = copy.deepcopy(to_cross_over[0][1][break_point:])
            to_cross_over[0][1][break_point:] = copy.deepcopy(to_cross_over[1][1][break_point:])
            to_cross_over[1][1][break_point:] = copy.deepcopy(to_cross_over[0][1][break_point:])
            to_cross_over[2][1][break_point:] = copy.deepcopy(temp)

        for i in range(0 + len(to_cross_over) % 2 * 3, len(to_cross_over), 2):
            break_point = random.randint(1, list_len-1)
            print(
                f"Recombinare dintre cromozomul {to_cross_over[i][0]} si cromozomul {to_cross_over[i + 1][0]} la pozitia {break_point}:\n")
            print(f"\t{''.join([str(x) for x in to_cross_over[i][1]])}\t")
            print(f"{''.join([str(x) for x in to_cross_over[i + 1][1]])}\n")
            temp = copy.deepcopy(to_cross_over[i][1][break_point:])
            to_cross_over[i][1][break_point:] = copy.deepcopy(to_cross_over[i+1][1][break_point:])
            to_cross_over[i+1][1][break_point:] = copy.deepcopy(temp)
            print("Rezultat:\n")
            print(f"\t{''.join([str(x) for x in to_cross_over[i][1]])}\t")
            print(f"{''.join([str(x) for x in to_cross_over[i + 1][1]])}\n")

        print("\nDupa incrucisare:\n")
        for i in range(population_size-1):
            x = decode_individual(new_population[i])
            print(f"\t{i + 1}: {''.join([str(x) for x in population[i]])}\tx=\t{x}\tf(x)= {f(x)}\n")

        print(f"\nProbabilitatea de mutatie pentru fiecare gena {mutation_probability}:\n")      #   pot aparea mai multe mutatii in acelasi cromozom
        print("Au fost modificate genele:\n")
        for i, individ in enumerate(new_population):
            r = random.uniform(0, 1)
            if r < mutation_probability:
                index = random.randint(0, list_len-1)
                print(f"\t{i+1}\n")

        print("\nDupa mutatie:\n")

        for i in range(population_size-1):
            x = decode_individual(new_population[i])
            print(f"\t{i + 1}: {''.join([str(x) for x in population[i]])}\tx=\t{x}\tf(x)= {f(x)}\n")

        new_population.append(fittest)

        print("Populatia finala:\n")
        for i in range(population_size):
            x = decode_individual(new_population[i])
            print(f"\t{i + 1}: {''.join([str(x) for x in population[i]])}\tx=\t{x}\tf(x)= {f(x)}\n")


        sum = 0
        population = new_population
        maxim = f(decode_individual(population[0]))
        for individ in population:
            x = decode_individual(individ)
            sum += f(x)
            if f(x) > maxim:
                maxim = f(x)
        val_maxim.append(maxim)

        val_mediu.append(sum/population_size)

        print("Evoluția maximului:\n")
        for i, val in enumerate(val_maxim):
            print(f"Generatia {i+1}: {val}\n")

    # epsilon is used to make the plot look better
    epsilon = (max_point_y - val_maxim[0])

    #plot the evolution of the maximum
    fig, axes = plt.subplots(nrows=3, ncols=1)

    # plt.ylim(val_maxim[0]-epsilon, max_point_y + epsilon)
    # plt.plot(val_maxim)
    # # plt.axhline(y=max_point_y, color='r', linestyle='-')
    # plt.xlabel("Generatia")
    # plt.ylabel("Valoarea maxima")
    #
    # #plot the evolution of the average
    # plt.ylim(val_mediu[0] -epsilon, max_point_y + epsilon)
    # plt.plot(val_mediu)
    # # plt.axhline(y=max_point_y, color='r', linestyle='-')
    # plt.xlabel("Generatia")
    # plt.ylabel("Valoarea medie")

    axes[0].plot(val_maxim)

    # axes[0].set_xlabel('Generatia')
    axes[0].set_ylabel('Val Max')

    axes[1].plot(val_mediu)

    # axes[1].set_xlabel('Generatia')
    axes[1].set_ylabel('Val Mean')

    axes[2].plot(val_maxim)
    axes[2].plot(val_mediu)

    axes[2].set_xlabel('Generatia')
    axes[2].set_ylabel('BOTH')

    # Adjust spacing between subplots
    plt.tight_layout()

    # Display the plot
    plt.show()
