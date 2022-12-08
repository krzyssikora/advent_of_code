import sys
import os


def get_data_lines(my_file):
    with open(my_file) as f:
        lines = f.readlines()
    return [line.strip('\n').strip() for line in lines]


def display_disc(disc, level=0):
    for name, value in disc.items():
        if name in {'parent', 'name'}:
            continue
        name = name[:name.rfind('_')]
        if isinstance(value, int):
            print('   ' * level + f'{name}: {value}')
        else:
            print('   ' * level + f'{name}: ')
            display_disc(value, level + 1)


def get_unique_name(name, names):
    number_of_times_name_used = names.get(name, 0)
    names[name] = number_of_times_name_used + 1
    name = f'{name}_{number_of_times_name_used}'
    return name, names


def get_files(current_dir, lines, current_line_idx, names):
    while True:
        if current_line_idx >= len(lines):
            break
        elements = lines[current_line_idx].split()
        if elements[0] == '$':
            break
        first, name = elements
        name, names = get_unique_name(name, names)
        if first.isdigit():
            current_dir[name] = int(first)
        current_line_idx += 1

    return current_line_idx, current_dir, names


def crawl_disc(lines):
    current_dir = {
        'parent': None,
        'name': '/'
    }
    names = dict()

    current_line_idx = 1
    while True:
        if current_line_idx >= len(lines):
            break
        elements = lines[current_line_idx].split()
        if elements[0] != '$':
            current_line_idx, current_dir, names = get_files(current_dir, lines, current_line_idx, names)
        else:
            # now we start from $ followed by ls or cd
            if elements[1] == 'ls':
                current_line_idx += 1
            else:
                # cd to elements[2]
                new_dir_name = elements[2]
                if new_dir_name == '..':
                    current_dir = current_dir['parent']
                else:
                    new_dir_name, names = get_unique_name(new_dir_name, names)
                    new_dir = {
                        'parent': current_dir,
                        'name': new_dir_name
                    }
                    current_dir[new_dir_name] = new_dir
                    current_dir = new_dir
                current_line_idx += 1

    while current_dir['parent']:
        current_dir = current_dir['parent']

    return current_dir


def get_total_size(disk, total_size=None, folder_name='/'):
    if not total_size:
        total_size = dict()
    for k, v in disk.items():
        if k in {'parent', 'name'}:
            continue
        elif isinstance(v, int):
            total_size[folder_name] = total_size.get(folder_name, 0) + v
        else:
            total_size, size = get_total_size(v, total_size, k)
            total_size[folder_name] = total_size.get(folder_name, 0) + size
    return total_size, total_size[folder_name]


def get_sum_of_sizes_of_smaller_folders(total_size):
    total = 0
    for k, v in total_size.items():
        if v <= 100000:
            total += v
    return total


def get_size_of_folder_to_delete(folder_sizes):
    total_space = 70000000
    space_needed_for_updates = 30000000
    space_taken = folder_sizes['/']
    free_space = total_space - space_taken
    space_that_needs_to_be_freed = space_needed_for_updates - free_space
    sizes_of_folders_that_can_be_deleted = list()
    for name, size in folder_sizes.items():
        if size >= space_that_needs_to_be_freed:
            sizes_of_folders_that_can_be_deleted.append(size)
    return min(sizes_of_folders_that_can_be_deleted)


def main(my_file):
    lines = get_data_lines(my_file)

    root = crawl_disc(lines)
    display_disc(root)
    total_size, size = get_total_size(root)
    print("part 1:", get_sum_of_sizes_of_smaller_folders(total_size))
    print("part 2:", get_size_of_folder_to_delete(total_size))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = f'{os.path.basename(__file__)[:2]}_input.txt'
    main(filename)
    # 804214 too low
