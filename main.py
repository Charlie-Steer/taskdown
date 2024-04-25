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


def get_block_lengths(lines: str):
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


def get_branch_str(lines: str, line_index: int):

    line = lines[line_index]
    lines_len = len(lines)
    tab_num = 0

    # Determine indentation level of task
    if (line.split('-')[0].endswith(' ')):
        tab_num: int = line.split('-')[0].count('    ')
    elif (line.split('-')[0].endswith('\t')):
        tab_num: int = line.split('-')[0].count('\t')

    # Populate branch string
    branch_str: str = ""
    next_line_exists = line_index + 1 < lines_len
    for i in range(tab_num * branch_width_mult):
        if i == 0 and (not next_line_exists or lines[line_index + 1].startswith('-')):
            branch_str += "  └"
        elif i == 0:
            branch_str += "  ├"
        else:
            branch_str += "─"
    branch_str += " "
    return branch_str


def get_checkbox(status):
    checkbox_str = '[ ]'
    if status == Status.DONE:
        checkbox_str = '[✓]'
    else:
        checkbox_str = '[ ]'
    return checkbox_str


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


def add_whitespace(number: int):
    whitespace_str = ''
    for i in range(number):
        whitespace_str += ' '
    return whitespace_str

def set_status(line: str):
    status_char = line.split('[')[1][0]
    if status_char == 'x' or status_char == 'X':
        return Status.DONE
    else:
        return Status.NOT_STARTED

# def get_branch_str():
#     block_index: int = -1
#     block_line_index: int = 0
#     in_subtasks = False
#
#     # Print branch lines
#     if line.startswith('-'):
#         block_index += 1
#         block_line_index = 0
#         if in_subtasks:
#             in_subtasks = False
#         print(end = '\n')
#
#     elif line.startswith(' ') or line.startswith('\t'):
#         in_subtasks = True
#         block_line_index += 1
#
#     return get_line_tree_chars(line, block_lengths, block_index, block_line_index)


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
    add_whitespace(40)
    print('Priority', end='')
    add_whitespace(20)
    print('Due', end='')
    print(end='\n')
    print_separator_line()


    with open(file_name, 'r') as file:

        lines = remove_empty_lines(file)

        for index, line in enumerate(lines):

            is_valid_task_line = validate_task_line(line)
            if is_valid_task_line:
                clean_line = ''
                status = set_status(line)

                branch_str = get_branch_str(lines, index)
                clean_line += branch_str
                checkbox_and_task_name_str = ''
                checkbox_and_task_name_str += get_checkbox(status)
                checkbox_and_task_name_str += ' '
                task_name: str = get_task_name(line)
                checkbox_and_task_name_str += task_name

                if (status == Status.DONE):
                    clean_line += strikethrough_text(checkbox_and_task_name_str)
                else:
                    clean_line += checkbox_and_task_name_str


                checkbox_len = 4
                branch_len = len(branch_str)
                text_field_width = branch_len + checkbox_len + len(task_name)
                field_whitespace_len = tasks_column_width - text_field_width
                clean_line += add_whitespace(field_whitespace_len)
                clean_line += '|'

                print(clean_line)


