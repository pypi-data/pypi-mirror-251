import os
import subprocess

import requests


class Compresser:
    def __init__(self):
        self.__url = 'https://www.7-zip.org/a/7zr.exe'
        self.__filename = '7z.exe'
        if not os.path.exists(self.__filename):
            response = requests.get(self.__url)
            with open(self.__filename, 'wb') as f:
                f.write(response.content)

    def __run_cmd(self, cmd: str) -> [int, str]:
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
            return [int(e.returncode), str(e.output.decode('utf-8'))]

    def yasuo(self, input_file, output_file, password=None) -> [int, str]:
        """
        压缩文件
        :param input_file: 源文件地址
        :param output_file: 压缩文件地址
        :param password: [option] 设置密码
        :return:
        """
        command = f'{self.__filename} a -p{password} {output_file} {input_file}'
        if password:
            command = f'{self.__filename} a -p{password} {output_file} {input_file}'
        else:
            command = f'{self.__filename} a {output_file} {input_file}'
        result = self.__run_cmd(command)
        return result

    def jieya(self, input_file, output_file, password=None) -> [int, str]:
        """
        解压文件
        :param input_file: 源文件地址
        :param output_file: 解压文件目录
        :param password:
        :return:
        """
        command = f'{self.__filename} x -p{password} {input_file} -o{output_file}'
        if password:
            command = f'{self.__filename} x -p{password} {input_file} -o{output_file}'
        else:
            command = f'{self.__filename} x {input_file} -o{output_file}'
        result = self.__run_cmd(command)
        return result
