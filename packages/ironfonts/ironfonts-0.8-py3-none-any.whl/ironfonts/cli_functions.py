#==============================================================#
#   Section:
#   IMPORTS & CONSTANTS
#==============================================================#
import pyperclip

NORMAL_EM = 2048    # Em-size for most fonts.
NORMAL_INCREMENT = round(NORMAL_EM/48, 2)

OLD_EM = 1000       # An older conventional em-size, I think.
OLD_INCREMENT = round(OLD_EM/48, 2) # I have not verified this to work.

IRON_EM = 360       # Em-size for my high-res fonts, after 2023-06.
IRON_INCREMENT = round(IRON_EM/48, 2)
# - I have found the above value (1/48th the em-size) to be the
#   smallest increment I can adjust by without effecting the
#   fuzziness of the lines I'm moving.

#==============================================================#
#   Section:
#   TESTER-FUNCTIONS
#==============================================================#
def adjust_position_tester( ):
    adjust_position(97)
    adjust_position(62)
    adjust_position(999)
    adjust_position(-80)
    adjust_position(15)
    adjust_position(0)

#==============================================================#
#   Section:
#   INFRASTRUCTURAL FUNCTIONS
#==============================================================#
def percentage_change(initial_value, new_value):
    initial = initial_value
    new = new_value
    percentage_change = 100 * ((new - initial) / initial)
    return percentage_change


# - Below: Rounds to the closest multiple of original_value (x).
def round_x(original_value, round_to):
    original = original_value
    round_to = float(round_to)

    remainder = original % round_to
    base = original // round_to
    if remainder >= round_to / 2:
        base = base + 1
    rounded_value = round(base * round_to)
    return rounded_value


def round_iron(original_value, iron_increment=IRON_INCREMENT):
    original = original_value

    rounded_value = round_x(original, iron_increment)
    return rounded_value


def round_normal(original_value, normal_increment=NORMAL_INCREMENT):
    original = original_value

    rounded_value = round_x(original, normal_increment)
    return rounded_value


def round_old(original_value, old_increment=OLD_INCREMENT):
    original = original_value

    rounded_value = round_x(original, old_increment)
    return rounded_value


#==============================================================#
#   Section:
#   CLI FUNCTIONS
#==============================================================#
def adjust_position(current_offset_from_sharp):
    current_offset = current_offset_from_sharp
    desired_offset = round_iron(current_offset)
    necessary_change = desired_offset - current_offset
    pyperclip.copy(str(necessary_change))
    print("Desired Offset: " + str(desired_offset))
    print("Necessary Change: ±" + str(abs(necessary_change)))


def bear(scale_factor, left_bearing, right_bearing):
    factor = scale_factor
    left = left_bearing
    right = right_bearing
    print(str(round_iron(left*factor)) + ", " + str(round_iron(right*factor)))


def bear75(left_bearing, right_bearing):
    left = left_bearing
    right = right_bearing
    print(str(round_iron(left*0.75)) + ", " + str(round_iron(right*0.75)))


def bear88(left_bearing, right_bearing):
    left = left_bearing
    right = right_bearing
    print(str(round_iron(left*0.88)) + ", " + str(round_iron(right*0.88)))


def fit(desired_measure, current_measure):
    desired = desired_measure
    current = current_measure
    scale_factor = 0.0
    relative_difference = 100 * ((desired - current) / current)
    scale_factor = 100 + (relative_difference)
    print(str(round(scale_factor, 4)))


def fix_position(current_bearing, standard_bearing=34):
    standard_position = standard_bearing
    current_position = current_bearing
    current_offset = current_position - standard_position
    desired_offset = round_iron(current_offset)
    necessary_change = desired_offset - current_offset
    pyperclip.copy(str(necessary_change))
    print("Desired Position: " + str(desired_offset + standard_position))
    print("Necessary Change: ±" + str(abs(necessary_change)))


def multiscale(changes, measures):
    changes = changes
    measures = measures
    counter = 0
    while counter < len(changes):
        scaleby(changes[counter], measures[counter])
        counter += 1


def push(change, current_measure):
    current = current_measure
    try:
        desired = current + change
        movement = abs(change/2)
        rel_dif = percentage_change(current, desired)
        scale_factor = 100 + (rel_dif)
        # print(str(round(scale_factor, 3)) + " (±"+str(movement)+")")
        print(f"{scale_factor:.3f} (±{movement})")
    except TypeError:   # Intended to handle lists input for the current_measure argument.
        for measure in current:
            push(change, measure)


def scaleby(change, current_measure):
    current = current_measure
    try:
        desired = current + change
        rel_dif = percentage_change(current, desired)
        scale_factor = 100 + rel_dif
        print(str(round(scale_factor, 3)))
    except TypeError:
        for measure in current:
            scaleby(change, measure)


# - duopush() is retired 'cause I don't actually use it.
# def duopush(change, current_measure_1, current_measure_2=0):
#     change = change
#     current_1 = current_measure_1
#     current_2_checker = current_measure_2
#     if check_whether(current_2_checker, 0):
#         current_2 = current_1 + 408
#     else:
#         current_2 = current_2_checker
#     push(change, current_1)
#     push(change, rcurrent_2)


# - multipush() is obsoleted after I made push() able to handle lists.
# def multipush(change, current_measure_list):
#     change = change
#     measures = current_measure_list
#
#     for x in measures:
#         push(change, x)

