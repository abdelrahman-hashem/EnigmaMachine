# constants & global variables

alphabet_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

rotor1list = ['E', 'K', 'M', 'F', 'L', 'G', 'D', 'Q', 'V', 'Z', 'N', 'T', 'O', 'W', 'Y',
              'H', 'X', 'U', 'S', 'P', 'A', 'I', 'B', 'R', 'C', 'J']

rotor2list = ['A', 'J', 'D', 'K', 'S', 'I', 'R', 'U', 'X', 'B', 'L', 'H', 'W', 'T', 'M',
              'C', 'Q', 'G', 'Z', 'N', 'P', 'Y', 'F', 'V', 'O', 'E']

rotor3list = ['B', 'D', 'F', 'H', 'J', 'L', 'C', 'P', 'R', 'T', 'X', 'V', 'Z', 'N', 'Y',
              'E', 'I', 'W', 'G', 'A', 'K', 'M', 'U', 'S', 'Q', 'O']

rotor4list = ['E', 'S', 'O', 'V', 'P', 'Z', 'J', 'A', 'Y', 'Q', 'U', 'I', 'R', 'H', 'X', 'L', 'N',
              'F', 'T', 'G', 'K', 'D', 'C', 'M', 'W', 'B']

rotor5list = ['V', 'Z', 'B', 'R', 'G', 'I', 'T', 'Y', 'U', 'P', 'S', 'D', 'N', 'H', 'L',
              'X', 'A', 'W', 'M', 'J', 'Q', 'O', 'F', 'E', 'C', 'K']

rotors_choices_list = [rotor1list, rotor2list, rotor3list, rotor4list, rotor5list]
slow_rotor = medium_rotor = fast_rotor = rotors_choices_list[0]
rotor_input = [1, 2, 3]

fast_rotor_shifted = []
medium_rotor_shifted = []
slow_rotor_shifted = []

reflectorB_list = ['Y', 'R', 'U', 'H', 'Q', 'S', 'L', 'D', 'P', 'X', 'N',
                   'G', 'O', 'K', 'M', 'I', 'E', 'B', 'F', 'Z', 'C', 'W', 'V', 'J', 'A', 'T']

plugboard_dict = {'A': 'S', 'S': 'A', 'O': 'K', 'K': 'O', 'P': 'Y', 'Y': 'P', 'C': 'B', 'B': 'C', 'F': 'R', 'R': 'F',
                  'V': 'Q', 'Q': 'V', 'D': 'Z', 'Z': 'D', 'M': 'U', 'U': 'M', 'G': 'J', 'J': 'G', 'E': 'N', 'N': 'E'}

reverse = False
count_fast = 0
count_medium = 0
shift_fast = 0
shift_medium = 0
shift_slow = 0
final_msg = []


# ---------------------------------------------------------------------


def shift_one_step(lis: list):
    # this function performs the shift by one step that happens every letter
    lis.append(lis[0])
    del lis[0]
    return lis


def rotor_setting(a, b, c):
    # this function is basically the ring settings, it takes the ring settings for each rotor
    # and adjust the rotors based on these settings
    global slow_rotor, slow_rotor_shifted, medium_rotor, medium_rotor_shifted, fast_rotor, fast_rotor_shifted, \
        shift_fast, shift_medium, shift_slow, rotors_choices_list

    for _ in range(a - 1):
        slow_rotor = shift_one_step(slow_rotor)
    slow_rotor_shifted = slow_rotor
    slow_rotor = rotors_choices_list[int(rotor_input[0])]

    for _ in range(b - 1):
        medium_rotor = shift_one_step(medium_rotor)
    medium_rotor_shifted = medium_rotor
    medium_rotor = rotors_choices_list[int(rotor_input[1])]

    for _ in range(c - 1):
        fast_rotor = shift_one_step(fast_rotor)
    fast_rotor_shifted = fast_rotor
    fast_rotor = rotors_choices_list[int(rotor_input[2])]


def shift():
    # this function rotates the rotors and changes the  shift, fast rotor always rotates no matter what so it is done
    # automatically, the rest will be shifted based on the if conditions that the previous one rotated
    global count_fast, count_medium, shift_fast, shift_medium, shift_slow, slow_rotor_shifted, \
        medium_rotor_shifted, fast_rotor_shifted
    fast_rotor_shifted = shift_one_step(fast_rotor_shifted)
    count_fast += 1
    shift_fast += 1
    if not shift_fast % 26:
        count_fast = 0
        shift_medium += 1
        if not shift_medium % 26:
            shift_medium = 0
            shift_slow += 1
            if not shift_slow % 26:
                shift_slow = 0

    if count_fast % 26 == 0:
        medium_rotor_shifted = shift_one_step(medium_rotor_shifted)

    if count_medium % 26 == 0 and count_medium != 0:
        slow_rotor_shifted = shift_one_step(slow_rotor_shifted)


def reflector(msg):
    # this function takes a message and reflects each letter based on the reflector B settings
    global reflectorB_list
    reflected_message = []

    for char in msg:
        if char in alphabet_list:
            changed_letter = reflectorB_list[alphabet_list.index(char)]
            reflected_message.append(changed_letter)
    rotor1(reflected_message)


# the 3 following functions are the ones responsible for encrypting the letter by each rotor and then pass it to the
# next step based on the REVERSED boolean
def rotor1(msg):
    global reverse, slow_rotor, slow_rotor_shifted
    rotor1_output = []

    if not reverse:
        for char in msg:
            if char in alphabet_list:
                changed_letter = slow_rotor_shifted[alphabet_list.index(char)]
                rotor1_output.append(changed_letter)

        reverse = True
        reflector(rotor1_output)
    else:
        for char in msg:
            if char in alphabet_list:
                changed_letter = alphabet_list[slow_rotor_shifted.index(char)]
                rotor1_output.append(changed_letter)
        rotor2(rotor1_output)


def rotor2(msg):
    global reverse, medium_rotor, medium_rotor_shifted
    rotor2_output = []

    if not reverse:
        for char in msg:

            if char in alphabet_list:
                changed_letter = medium_rotor_shifted[alphabet_list.index(char)]
                rotor2_output.append(changed_letter)

        rotor1(rotor2_output)
    else:
        for char in msg:

            if char in alphabet_list:
                changed_letter = alphabet_list[medium_rotor_shifted.index(char)]
                rotor2_output.append(changed_letter)
        rotor3(rotor2_output)


def rotor3(msg):
    # this function takes the message then sends it letter by letter to the rest of the rotors
    global reverse, fast_rotor, fast_rotor_shifted
    rotor3_output = []

    if not reverse:
        for char in msg:
            test = []
            if char in alphabet_list:
                changed_letter = fast_rotor_shifted[alphabet_list.index(char)]
                rotor3_output.append(changed_letter)
                test.append(rotor3_output[-1])
                rotor2(test)
                shift()

    else:
        for char in msg:

            if char in alphabet_list:
                changed_letter = alphabet_list[fast_rotor_shifted.index(char)]
                rotor3_output.append(changed_letter)
                # shift(), letter still has to come back through same config
        plugboard(rotor3_output)


def plugboard(msg):
    # switch the letters through the plugboard dictionary in case they are there, otherwise, add the same letter
    global reverse, final_msg, plugboard_dict
    plugboard_switched_message = []

    for char in msg:

        if char in alphabet_list:

            if char in plugboard_dict.keys():
                char = plugboard_dict[char]

            plugboard_switched_message.append(char)

    if not reverse:
        rotor3(plugboard_switched_message)
    else:
        final_msg.append(plugboard_switched_message)
        reverse = False


# main loop for encode:
def encode():
    global final_msg, count_fast, count_medium, rotors_choices_list, slow_rotor, medium_rotor, fast_rotor
    rotor_choice = list(input("enter rotor numbers to use in the following order 'slow medium fast' without spaces: "))
    fast_rotor = rotors_choices_list[int(rotor_choice[2]) - 1]
    medium_rotor = rotors_choices_list[int(rotor_choice[1]) - 1]
    slow_rotor = rotors_choices_list[int(rotor_choice[0]) - 1]
    rotor_input = (
        input("enter ring settings in the following order 'slow, medium, fast' seperated by commas: ")).split(",")
    user_input = input("Enter text to encode: ").upper().replace(" ", "X")
    rotor_setting(int(rotor_input[0].strip()), int(rotor_input[1].strip()), int(rotor_input[2].strip()))
    plugboard(user_input)
    fnl_msg_string = ''.join([letter[0] for letter in final_msg])
    print("final message", fnl_msg_string)

    final_msg = []
    count_fast = count_medium = 0


# call encode function to initiate the program
encode()
