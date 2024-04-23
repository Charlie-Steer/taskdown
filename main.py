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


def print_line_tree_chars(line: str, block_lengths: int, block_index: int):
    branch_string: str = " "
    branch_len = 0

    if (line.split('-')[0].startswith(' ')):
        tab_num: int = line.split('-')[0].count('    ')
    elif (line.split('-')[0].startswith('\t')):
        tab_num: int = line.split('-')[0].count('\t')
    else:
        return
    for i in range(tab_num * branch_width_mult):
        if i == 0 and block_line_index == block_lengths[block_index] - 1:
            branch_string += "└"
            #print(' └', end='')
        elif i == 0:
            branch_string += "├"
            #print(' ├', end='')
        else:
            branch_string += "─"
            #print('─', end='')
    branch_string += " "
    print(branch_string, end="")

    branch_len = len(branch_string)
    return branch_len


def print_checkbox(status):
    if status == Status.DONE:
        print('[✓]', end=' ');
    else:
        print('[ ]', end=' ');
    return 4


def strikethrough_text(text):
    return ("\x1B[9m" + text + "\x1B[0m")


def print_task(name: str, status):
    if (status == Status.DONE):
        print(strikethrough_text(name),  end="")
    else:
        print(name, end="")
    return name


def validate_task_line(line: str):
    if line.strip().startswith('- '):
        return True
    else:
        return False


def print_whitespace(number: int, end=''):
    for i in range(number):
        print(' ', end='')
    print(end=end)



class Status(Enum):
    NOT_STARTED = 0
    DONE = 1

# CONFIGS
file_name = 'test.md'

branch_width_mult: int = 4
tasks_column_width = 40
priority_column_width = 20
due_column_width = 40


if __name__ == '__main__':
    #TODO: Implement priorities with symbols and color codes?
    #char = chr(int('f06a', 16))
    #text = 'hello'
    #color_code = 31
    #print(f"\033[{color_code}m{char}\033[0m")

    #TODO: Column titles are not considered in width
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
            text_field_width = 0
            branch_len = 0
            checkbox_len = 4

            # Print branch lines
            if line.startswith('-'):
                block_index += 1
                block_line_index = 0
                if in_subtasks:
                    in_subtasks = False
                print(end = '\n')

            elif line.startswith(' ') or line.startswith('\t'):
                in_subtasks = True
                block_line_index += 1
                branch_len = print_line_tree_chars(line, block_lengths, block_index)


            is_valid_task_line = validate_task_line(line)
            if is_valid_task_line:
                if line.split('[')[1][0] == 'x':
                    status = Status.DONE
                else:
                    status = Status.NOT_STARTED
                checkbox_len = print_checkbox(status)
                task_name: str = get_task_name(line)
                print_task(task_name, status)

                text_field_width = branch_len + checkbox_len + len(task_name)
                field_whitespace_len = tasks_column_width - text_field_width
                print_whitespace(field_whitespace_len, end='|')

                print(end="\n")


