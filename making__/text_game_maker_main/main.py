import re
import sys
import os
import time
from art import *
import changeSceneToJson

fn = 'gameTrialData.tgm'

game_starts = False
fore_color_hex='#ffffff'
back_color_hex='#ff0000'

scene_starts= False
text_font = 'wetletter'

typing_time = 0.05

string_to_send=''
already_added_to_string = False

line_separator = '<``Separator``>'


os.system('CLS')


valid_hex = '0123456789ABCDEF'.__contains__


def clean_hex(data):
    return ''.join(filter(valid_hex, data.upper()))


def print_color(text, end='\n',fore_color=fore_color_hex,back_color=back_color_hex):
    """print in a hex defined color"""
    back_hex_int = int(clean_hex(fore_color), 16)
    fore_hex_int = int(clean_hex(back_color), 16)
    text = text+end
    for character in text:
        sys.stdout.write("\x1B[48;2;{};{};{}m\x1B[38;2;{};{};{}m{}\x1B[0m".format(fore_hex_int >> 16, fore_hex_int >> 8 & 0xFF,
                                                                      fore_hex_int & 0xFF, back_hex_int >> 16,
                                                                      back_hex_int >> 8 & 0xFF, back_hex_int & 0xFF,
                                                                      character))

        sys.stdout.flush()
        time.sleep(typing_time)


def error_sender(error_sentence, error_line,line_num):
    print_color('[Error]', end='')
    print_color(' '+error_sentence, fore_color='#ffff00',back_color='#000000')
    print(' ' * (len(str(line_num)) + 4), end='')
    print_color('▼', fore_color='#ff0000',back_color='#000000')
    print_color('------------', fore_color='#ff0000',back_color='#000000')
    print(str(line_num) + ' : ' + error_line)
    print_color('------------', fore_color='#ff0000',back_color='#000000')
    print('')
    sys.exit()

# print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')

with open(fn) as file:
    for i, ln in enumerate(file.readlines()):
        function_name = ''
        code_right_now = ''
        ln = ln.replace("\n", "").replace('\r', '')
        ln = ln.lstrip()
        if ln.startswith('['):
            already_added_to_string = False
            code_block_data_split_with_space = re.search(r"\[([A-Za-z0-9_=`?@#$%^&*()+|/.,;'{}:<>\" ]+)\]", ln).group(1).lstrip()
            # print(code_block_data_split_with_space)
            # print(code_block_data_split_with_space)
            all_code_data_in_code_block = code_block_data_split_with_space.split(' ')
            for code_data in all_code_data_in_code_block:
                code_data = code_data.lower()

                if (code_data == 'game'):
                    if (game_starts != True):
                        game_starts = True
                        print('Hello Game')
                    else:
                        error_sender('Game is Already Started', ln, i)
                elif (game_starts == True):
                    if(code_data == 'scene'):
                        if (scene_starts == False):
                            scene_starts = True
                        else:
                            error_sender('End Previous Scene To Start New',ln,i)

                        print('Scene')
                    elif(code_data == '/scene'):
                        if scene_starts == True:
                            scene_starts = False
                            changeSceneToJson.main(string_to_send,line_separator)
                            string_to_send = ''
                        else:
                            error_sender('Scene started without starting it', ln, i)
                    elif code_data[:9] == 'textcolor':
                        color_data=code_data.split('_')[1].strip("'")
                        fore_color_hex = '#'+color_data
                    elif(code_data == 'title'):
                        if len(all_code_data_in_code_block) >= 2:
                            for function_data in all_code_data_in_code_block:
                                if function_data.lstrip()[:5] == 'font_':
                                    text_font = function_data.lstrip()[5:]

                        text_inside_function_name = ln.replace('[' + code_block_data_split_with_space + ']', '')
                        if text_inside_function_name[0] == ' ':
                            text_inside_function_name = text_inside_function_name[1:]

                        tprint(text_inside_function_name, font=text_font)
                    elif(code_data[:5]=='font_'):
                        text_font = code_data.lstrip()[5:]
                    elif scene_starts == True:
                        if already_added_to_string:
                            continue
                        else:
                            string_to_send= string_to_send+str(ln)+line_separator
                            already_added_to_string = True
                else:
                    error_sender('[Game] tag missing on top', ln, i)

print(string_to_send)