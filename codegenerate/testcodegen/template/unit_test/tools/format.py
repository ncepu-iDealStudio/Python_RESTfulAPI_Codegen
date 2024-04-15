import json


def center_text(text, total_length=127, fill_char='='):
    """将文本居中并用指定字符填充左右两侧，以达到总长度为指定长度的效果。

    Args:
        text (str): 要居中显示的文本。
        total_length (int, optional): 居中后的总长度，默认为 127。
        fill_char (str, optional): 用于填充左右两侧的字符，默认为 '='。

    Returns:
        str: 居中后的字符串。
    """
    return (' ' + text + ' ').center(total_length, fill_char)


def format_dict_to_json_output(data_dict, indent=4):
    if isinstance(data_dict, dict):
        res = json.dumps(data_dict, indent=indent)
    else:
        res = str(data_dict)
    return res
