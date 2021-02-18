import re


def main(data, line_separator):
    current_story_number = 0
    file_data = filter(None, data.split(line_separator))
    json_data = {}
    for line_number, line_data in enumerate(file_data):
        code_block_data_split_with_space = re.search(r"\[([A-Za-z0-9_=`?@#$%^&*()+|/.,;'{}:<>\" ]+)\]", line_data).group(1).lstrip()
        code_split_to_get_action_number=code_block_data_split_with_space.split("'")
        if code_split_to_get_action_number[0].isnumeric():
            print(line_number, line_data.replace('['+code_block_data_split_with_space+']',''))
