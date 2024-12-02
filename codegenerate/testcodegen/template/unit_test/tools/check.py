import re


def check_url(url):
    """
    判断字符串是否符合以下条件：
    1. 不以'/'结尾
    2. 不以'/数字'结尾

    参数：
    - s: 要验证的字符串

    返回：
    - 如果符合条件返回 True，否则返回 False

    正则表达式说明：
    ^            匹配字符串的开始
    (?!.*/\\d*$)  使用否定预查来确保字符串不以'/数字'结尾。
                 (?! ...): 否定预查，确保接下来的内容不匹配括号内的模式。
                 .*        匹配任意字符
                 /         匹配斜杠
                 \\d*       匹配零个或多个数字
                 $         匹配字符串的结束
    .*[^/]       匹配任意字符后面跟着不是斜杠的字符。这确保了字符串不以斜杠结尾。
    $            匹配字符串的结束
    """
    pattern = r"^(?!.*\/\d*$).*[^\/]$"
    if not re.match(pattern, url):
        raise ValueError(f"Invalid URL: {url}")


if __name__ == '__main__':
    try:
        check_url('/api')
        check_url('1234')
        # check_url('/api/1234')
        # check_url('/api/')
        # check_url('/api/')
    except Exception as e:
        print(e)
