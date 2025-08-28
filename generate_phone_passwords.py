import itertools
import string
import os


def generate_phone_passwords(output_file='phone_passwords.txt'):
    """
    生成特定手机号段的密码字典。
    """
    # 定义你想要生成的所有手机号段前缀
    # 这是中国大陆常见的部分号段，你可以根据需要添加或删除
    prefixes = [
        '130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
        '145', '147', '149',
        '150', '151', '152', '153', '155', '156', '157', '158', '159',
        '166',
        '170', '171', '173', '175', '176', '177', '178',
        '180', '181', '182', '183', '184', '185', '186', '187', '188', '189',
        '191', '198', '199'
    ]

    # 定义后八位的字符集
    suffix_chars = string.digits  # '0123456789'

    # 获取当前脚本的目录，将文件保存在同一位置
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, output_file)

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            print(f"正在生成密码字典到文件：{output_path}")

            total_passwords = 0
            num_prefixes = len(prefixes)

            # 生成后八位的所有组合 (10^8 = 1亿个)
            suffixes = itertools.product(suffix_chars, repeat=8)

            print(f"开始生成 {num_prefixes} 个号段的密码...")

            for prefix in prefixes:
                print(f"  - 正在生成号段 {prefix}...")

                # itertools.product 生成的是一个迭代器，不能重复使用
                # 所以我们不能在一个大循环中直接使用suffixes，而应该在外部生成一次
                # 并将每个前缀与它拼接

                # 重新生成一个后缀迭代器，确保每个前缀都能遍历完整的1亿个后缀
                suffixes_generator = itertools.product(suffix_chars, repeat=8)

                for suffix_tuple in suffixes_generator:
                    suffix = ''.join(suffix_tuple)
                    password = prefix + suffix
                    f.write(password + '\n')
                    total_passwords += 1

        print(f"\n密码字典生成完毕！")
        print(f"总共生成了 {total_passwords:,} 个密码。")

    except Exception as e:
        print(f"生成密码字典时发生错误: {e}")


if __name__ == "__main__":
    generate_phone_passwords()