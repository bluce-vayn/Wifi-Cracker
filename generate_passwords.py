import itertools
import string
import os


def generate_numeric_passwords(output_file='numeric_passwords.txt'):
    """
    生成由0-9组成的所有8-11位密码，并保存到指定文件中。
    """
    # 获取当前脚本的目录，将文件保存在同一位置
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, output_file)

    # 0-9的数字字符集
    chars = string.digits

    # 定义密码的长度范围
    min_len = 8
    max_len = 8

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            print(f"正在生成密码字典到文件：{output_path}")

            total_passwords = 0

            # 循环生成不同长度的密码
            for length in range(min_len, max_len + 1):
                print(f"开始生成所有 {length} 位的密码...")

                # 使用 itertools.product 生成所有组合
                # repeat=length 表示生成长度为length的组合
                # 例如，对于 length=8，会生成 10**8 = 1亿个组合
                for combination in itertools.product(chars, repeat=length):
                    # 将组合（元组）连接成一个字符串
                    password = ''.join(combination)
                    f.write(password + '\n')
                    total_passwords += 1

            print(f"\n密码字典生成完毕！")
            print(f"总共生成了 {total_passwords:,} 个密码。")

    except Exception as e:
        print(f"生成密码字典时发生错误: {e}")


if __name__ == "__main__":
    generate_numeric_passwords()