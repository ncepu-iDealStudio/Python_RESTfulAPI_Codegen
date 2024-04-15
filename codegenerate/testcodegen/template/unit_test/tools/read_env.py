def read_env(env_path) -> dict:
    """
        1. 格式key=value
        2. 支持#注释
    :param: .env文件路径
    :return: 环境变量字典
    """
    env_dict = {}
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.replace(" ", "").split('=')
                env_dict[key] = value.strip()
    return env_dict


def write_env(env_path, token) -> dict:
    """
    向.env文件写入内容
    """

    # 读取 .env 文件内容
    with open(env_path, "r") as f:
        lines = f.readlines()

    # 修改环境变量
    for i, line in enumerate(lines):
        if line.startswith("token="):
            lines[i] = "token=" + token + "\n"
            break

    # 将修改后的内容写回文件
    with open(env_path, "w") as f:
        f.writelines(lines)
