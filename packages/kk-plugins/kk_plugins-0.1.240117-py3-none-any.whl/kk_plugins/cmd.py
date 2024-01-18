import subprocess


def run_cmd(cmd: str) -> [int, str]:
    """
    执行命令
    :param cmd: 运行的命令
    :return: 状态值和输出
    """
    try:
        # 执行curl命令并捕获输出和错误
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return [0, str(result.stdout)]
    except subprocess.CalledProcessError as e:
        # 输出错误信息和返回码
        return [e.returncode, str(e.output.decode('utf-8'))]
