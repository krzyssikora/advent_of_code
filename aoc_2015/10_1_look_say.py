def look_and_say_once(my_string):
    my_list = list(my_string)
    return_string = ""
    string_list = list()
    new_string = ""
    previous = ""
    for elt in my_list:
        if elt != previous:
            if new_string != "":
                string_list.append(new_string)
            new_string = elt
        else:
            new_string += elt
        previous = elt
    string_list.append(new_string)
    for elt in string_list:
        return_string += str(len(elt)) + elt[0]
    return return_string


def look_and_say_many(my_string, many):
    if many == 0:
        return my_string
    else:
        return look_and_say_many(look_and_say_once(my_string), many - 1)


if __name__ == "__main__":
    initial_string = "1321131112"
    print(len(look_and_say_many(initial_string, 50)))
