import os
from enum import Enum
#from typing import IO


def print_separator_line():
    terminal_width = os.get_terminal_size().columns
    print('─' * terminal_width)


def get_task_name(task_line: str):
    task_name = task_line.strip().split(']')[1][1:]
    task_name = task_name.split('(')[0].strip()
    return task_name


def print_project_name(project_name: str):
    print("Project: " + file_name.split('.')[0], end='\n\n')


def remove_empty_lines(file):
    lines = []
    for line in file:
        if line.strip() != '':
            lines.append(line)
    file.seek(0)
    return lines


def get_block_lengths(file):
        lines = remove_empty_lines(file)
        block_lenghts = []
        task_line_count: int = 1

        for i, line in enumerate(lines):
            if line.startswith('-'):
                for j in range(len(lines) - i):
                    if (i + j + 1) < len(lines) and not lines[i + j + 1].startswith('-'):
                        j += 1
                        task_line_count += 1
                    else:
                        block_lenghts.append(task_line_count)
                        task_line_count = 1
                        break
        return block_lenghts


def print_line_tree_lines(line: str, block_lengths: int, block_index: int):
    tab_num: int = line.split('-')[0].count('    ')
    for i in range(tab_num * branch_width_mult):
        if i == 0 and block_line_index == block_lengths[block_index] - 1:
            print(' └', end='')
        elif i == 0:
            print(' ├', end='')
        else:
            print('─', end='')
    print(' ', end='')


def print_checkbox(status):
    if status == Status.DONE:
        print('[✓]', end=' ');
    else:
        print('[ ]', end=' ');


def strikethrough_text(text):
    return ("\x1B[9m" + text + "\x1B[0m")


def print_task(name: str, status):
    if (status == Status.DONE):
        print(strikethrough_text(name))
    else:
        print(name)


def validate_task_line(line: str):
    if line.strip() != '':
        return True
    else:
        return False


def print_whitespace(number: int):
    for i in range(column_tasks_width):
        print(' ', end='')



class Status(Enum):
    NOT_STARTED = 0
    DONE = 1

# CONFIGS
file_name = 'general.md'

branch_width_mult: int = 4
column_tasks_width = 40
column_priority_width = 20
column_due_width = 40


if __name__ == '__main__':
    #TODO: Implement priorities with symbols and color codes?
    #char = chr(int('f06a', 16))
    #text = 'hello'
    #color_code = 31
    #print(f"\033[{color_code}m{char}\033[0m")

    print_project_name(file_name)
    print('Tasks', end='')
    print_whitespace(40)
    print('Priority', end='')
    print_whitespace(20)
    print('Due', end='')
    print(end='\n')
    print_separator_line()


    with open(file_name, 'r') as file:
        block_lengths = get_block_lengths(file)
        block_index: int = -1
        block_line_index: int = 0

        for index, line in enumerate(file):
            in_subtasks = False

            # Print branch lines
            if line.startswith('-'):
                block_index += 1
                block_line_index = 0
                if in_subtasks:
                    in_subtasks = False
                print(end = '\n')

            elif line.startswith(' '):
                in_subtasks = True
                block_line_index += 1
                print_line_tree_lines(line, block_lengths, block_index)


            is_valid_task_line = validate_task_line(line)
            if is_valid_task_line:
                if line.split('[')[1][0] == 'x':
                    status = Status.DONE
                else:
                    status = Status.NOT_STARTED
                print_checkbox(status)
                task_name: str = get_task_name(line)
                print_task(task_name, status)
