"""
This is a solver for the book

Maze: Solve the World's Most Challenging Puzzle

by Christopher Manson.

My goal is to be able to tell the user which door to go through next without revealing the whole solution.

I want to be able to do the reverse journey as well.
"""
from typing import List, Deque
from collections import deque

children_of_room: dict[int, List[int]] = {}
"""
A dictionary that tracks what rooms can be accessed from the current room.

Room : [List_of_rooms_leading_from_here]
"""

parents_of_room: dict[int, List[int]] = {}
"""
A dictionary that tracks what rooms could lead to the current room.

Room : [List_of_rooms_leading_to_here]
"""
first_quest_solutions_from_start = list()
second_quest_solutions_from_start = list()
best_path_first_quest = [1, 26, 30, 42, 4, 29, 17, 45]
best_path_second_quest = [45, 23, 8, 12, 39, 4, 15, 37, 20, 1]
steps_from_goal: int


def main():
    setup()


def setup():
    add_room(1, [20, 26, 41, 21])
    add_room(2, [29, 22, 12])
    add_room(3, [18, 9, 33])  # upside down, might need to check
    add_room(4, [44, 29, 15, 11, 16, 24, 43])
    add_room(5, [43, 22, 30, 20])
    add_room(6, [40])
    add_room(7, [33, 36, 16])
    add_room(8, [31, 6, 29, 12])
    add_room(9, [3, 18])
    add_room(10, [34, 41, 14])
    add_room(11, [40, 24])
    add_room(12, [2, 21, 8, 39])
    add_room(13, [27, 18, 25])
    add_room(14, [10, 43, 24])
    add_room(15, [30, 37, 3])
    add_room(16, [36, 7])
    add_room(17, [6, 45, 33])
    add_room(18, [13, 3])
    add_room(19, [31, 11])
    add_room(20, [5, 27, 1])
    add_room(21, [44, 24, 31])
    add_room(22, [43, 38])
    add_room(23, [28, 8, 45, 19])
    add_room(24, [])  # kill room
    add_room(25, [34, 13, 35])  # One room has a crown over a door???
    add_room(26, [30, 36, 38, 1])
    add_room(27, [13, 9])
    add_room(28, [23, 43, 45, 32])
    add_room(29, [8, 40, 35, 2, 17])
    add_room(30, [42, 34, 5, 15])
    add_room(31, [44, 19, 21])
    add_room(32, [11, 16, 28])
    add_room(33, [3, 35, 7])
    add_room(34, [10, 25])
    add_room(35, [33])
    add_room(36, [7, 16])
    add_room(37, [15, 10, 42, 20])
    add_room(38, [40, 22, 43])  # Why does this room have a slide? What are its parent rooms?
    add_room(39, [11, 4, 12])  # One room has a jester hat above a sealed off door
    add_room(40, [11, 6, 38])
    add_room(41, [1, 35, 10, 38])
    add_room(42, [22, 30, 4, 25, 37])
    add_room(43, [22, 38])
    add_room(44, [21, 18])
    add_room(45, [28, 17, 36, 19, 23])

    calculate_parents()

    global children_of_room
    global first_quest_solutions_from_start
    while True:
        x = find_path(1, 45, first_quest_solutions_from_start)
        if not x:
            break
        else:
            first_quest_solutions_from_start.append(x)
    first_quest_solutions_from_start = sorted(first_quest_solutions_from_start, key=len)

    """
    print("FIRST QUEST (" + str(len(first_quest_solutions_from_start)) + " solutions):")
    for x in first_quest_solutions_from_start:
        print_arr_of_int(x)
    """

    global parents_of_room
    global second_quest_solutions_from_start
    while True:
        x = find_path(45, 1, second_quest_solutions_from_start)
        if not x:
            break
        else:
            second_quest_solutions_from_start.append(x)
    second_quest_solutions_from_start = sorted(second_quest_solutions_from_start, key=len)

    """
    print("SECOND QUEST (" + str(len(second_quest_solutions_from_start)) + " solutions):")
    for x in second_quest_solutions_from_start:
        print_arr_of_int(x)
    """

    global steps_from_goal
    curr_room: int
    prev_room: List[int]
    best_guess: int
    while True:
        try:
            quest_num = int(input("\nAre you in:\n1. The first quest\n2. The return journey\n").strip())
            if quest_num != 1 and quest_num != 2:
                raise ValueError()

            if quest_num == 1:
                curr_room = 1
                prev_room = [1]
            else:
                curr_room = 45
                prev_room = [45]
            while True:
                print("\nYou are in room #" + str(curr_room))
                if children_of_room[curr_room] == []:
                    print("You entered a kill room and that was the end of you!")
                    exit(0)
                print("You can access rooms: ", end="")
                print_arr_of_int(children_of_room[curr_room])
                guess = int(
                    input(
                        "Guess what room you should go to next or type \"0\" for the answer or \"-1\" to go back: ").strip())
                if guess == -1:
                    if len(prev_room) == 1:
                        print("You cannot go any further back!")
                    else:
                        curr_room = prev_room[-1]
                        del prev_room[-1]
                    continue
                best_guess = find_next_step_in_shortest_route_from_my_pos(curr_room, quest_num)
                if guess == 0:
                    guess = best_guess
                    print("You guessed " + str(guess) + ".")
                if guess < 1 or guess > 45:
                    print("That room does not exist!")
                    continue
                if (quest_num == 1 and guess not in children_of_room[curr_room]) or (
                        quest_num == 2 and parents_of_room[curr_room]):
                    print("You cannot reach that room from here.")
                    continue
                if guess == best_guess:
                    print("That was the best choice!")
                else:
                    print("That was not the best choice.")
                print("You are now " + str(steps_from_goal) + " steps from your goal.")
                prev_room.append(curr_room)
                curr_room = guess

        except ValueError:
            print("That is not a valid input!")
        except TypeError:
            print("That is not a valid input!")


def find_path(start_room: int, goal_room: int, already_found_solutions: List[List[int]]):
    """

    :param start_room: The room you are starting from.
    :param goal_room: The room you are trying to get to.
    :param already_found_solutions: Optional, tracks a list of solutions already found.
    :return:
    """
    global children_of_room
    queue: deque[List[int]] = deque()
    queue.append([start_room])

    while queue:
        curr_path = queue.popleft()
        last_element = curr_path[-1]
        children_rooms = children_of_room[last_element]

        if goal_room in children_rooms:
            curr_path.append(goal_room)
            if curr_path not in already_found_solutions:
                return curr_path
            else:

                continue

        for room in children_rooms:
            if room not in curr_path:
                new_path = curr_path.copy()
                new_path.append(room)
                queue.append(new_path)

    return []


def add_room(room_num: int, children: List[int]) -> None:
    global children_of_room
    if room_num not in children_of_room.keys():
        children_of_room[room_num] = children


def calculate_parents():
    global children_of_room
    global parents_of_room

    for parent_room, children_rooms in children_of_room.items():
        for child_room in children_rooms:
            if parent_room not in parents_of_room.keys():
                parents_of_room[child_room] = [parent_room]
            else:
                parents_of_room[parent_room].append(child_room)


def print_parents_and_children_rooms():
    global children_of_room
    print("CHILDREN OF ROOMS:")
    print_dict_with_lists_for_values(children_of_room)

    global parents_of_room
    print("PARENTS OF ROOMS:")
    print_dict_with_lists_for_values(parents_of_room)


def print_dict_with_lists_for_values(d: dict):
    s = ""
    for key, val_list in d.items():
        s = s + "KEY: " + str(key) + "\t["
        for v in val_list:
            s = s + str(v) + ", "
        s = s.strip()
        s = s.rstrip(",")
        s = s + "]\n"
    print(s)


def print_arr_of_int(arr: List[int]):
    s = "["
    for x in arr:
        s = s + str(x) + ", "
    s = s.strip()
    s = s.rstrip(",")
    s = s + "]"
    print(s)


def find_next_step_in_shortest_route_from_my_pos(curr_room: int, quest_num: int) -> int:
    """
    :param curr_room: The room you are currently in
    :param quest_num: 1. If you are trying to find room #45, 2. if you are trying to find your way back to room #1.
    :return: The shortest path to victory OR an empty array if the player has reached a kill room.
    """
    if curr_room == 24:
        return -1

    global first_quest_solutions_from_start
    global second_quest_solutions_from_start

    possible_solutions_list = []
    solutions_with_curr_room: List[List[int]] = []
    if quest_num == 1:
        possible_solutions_list = first_quest_solutions_from_start
    elif quest_num == 2:
        possible_solutions_list = second_quest_solutions_from_start
    else:
        raise Exception("Invalid quest number selected in find_shortest_route_from_my_position()")

    # Find all possible solutions that have my current room in them.
    for solution in possible_solutions_list:
        if curr_room in solution:
            solutions_with_curr_room.append(solution)

    # If no solutions
    solutions = []
    if not solutions_with_curr_room:
        goal_room = 45 if quest_num == 1 else 1

        while True:
            x = find_path(curr_room, goal_room, solutions)
            if not x:
                break
            else:
                solutions.append(x)
        solutions_with_curr_room = sorted(solutions, key=len)
        print(
            "We found " + str(len(solutions_with_curr_room)) + " solutions and are choosing the best one to guide you.")

    best_route: List[int] = [100] * 50
    for solution in solutions_with_curr_room:
        curr_room_idx = solution.index(curr_room)
        steps_remaining = solution[curr_room_idx + 1:]
        if len(steps_remaining) < len(best_route):
            best_route = steps_remaining

    global steps_from_goal
    steps_from_goal = len(best_route) - 1
    return best_route[0]


if __name__ == '__main__':
    main();
