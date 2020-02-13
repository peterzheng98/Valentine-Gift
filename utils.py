from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import config
import table_content


def DES_add_to_16(text: str) -> bytes:
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


def DES_encrypt(src: str) -> bytes:
    key = config.des_key.encode('utf-8')
    mode = AES.MODE_ECB
    text = DES_add_to_16(src)
    cryptos = AES.new(key, mode)
    cipher_text = cryptos.encrypt(text)
    return b2a_hex(cipher_text)


def DES_decrypt(text: bytes) -> str:
    key = config.des_key.encode('utf-8')
    mode = AES.MODE_ECB
    cryptor = AES.new(key, mode)
    plain_text = cryptor.decrypt(a2b_hex(text))
    return bytes.decode(plain_text).rstrip('\0')


def dispatch_final_stage_status(encrypted: str) -> tuple:
    try:
        status_string = DES_decrypt(encrypted.encode('utf-8'))
        print(status_string)
    except:
        return -1, -1

    acc_num, operation = status_string.split('/')
    acc_num = int(acc_num)
    print('{}->{}'.format(acc_num, operation))
    if acc_num != config.total_rounds:
        last_round = operation.index('0')
        print(operation, '->', last_round)
        if last_round != acc_num:
            return -1, -1  # internal error
        return acc_num, [int(i) for i in operation]
    else:
        if '0' not in operation:
            return 99, 99  # all finished


def render_table_internal(m: int, n: int,
                          word_list: list,
                          orange_list: list,
                          blue_list: list) -> list:
    """
    Generate the corresponding tables
    :param m: rows of the sheet
    :param n: column of the sheet
    :param word_list: declare the word_list, [word:str, pos_x:int, pos_y:int] for each element.
    :param orange_list: declare the orange area, (pos_x, pos_y) for each element.
    :param blue_list: declare the blue area, (pos_x, pos_y) for each element.
    :return: the html string of the table.
    """
    orange_list_set = set(orange_list)
    blue_list_set = set(blue_list)
    word_list_set = set([(i[1], i[2]) for i in word_list])
    word_list_idx = [(i[1], i[2]) for i in word_list]
    html_list = []
    for i in range(m):
        col_list = []
        for j in range(n):
            sub_dict = {}
            attr_label = []
            if (i, j) in orange_list_set:
                attr_label.append('#FFD700')
            elif (i, j) in blue_list_set:
                attr_label.append('#87CEEB')
            else:
                attr_label.append('#FFFFFF')
            if (i, j) in word_list_set:
                w = table_content.word_list[word_list_idx.index((i, j))][0]
            else:
                w = ' '
            sub_dict['attr_label'] = ' '.join(attr_label)
            sub_dict['content'] = w

            col_list.append(sub_dict)
        html_list.append(col_list)
    return html_list


def render_table(idx: int) -> list:
    idx = idx - 1
    total_word_count_before = sum([len(i[1]) for i in table_content.question_answer[0:idx]])
    total_word_count_after = sum([len(i[1]) for i in table_content.question_answer[0:idx+1]])
    print('before:{}->{}'.format(total_word_count_before, total_word_count_after))
    internal_blue_list = table_content.blue_list_prefix[0:total_word_count_before]
    internal_orange_list = table_content.orange_list_prefix[total_word_count_before:total_word_count_after]
    internal_word_list = table_content.word_list[0:total_word_count_before]
    return render_table_internal(
        m=table_content.table_size[0],
        n=table_content.table_size[1],
        word_list=internal_word_list,
        orange_list=internal_orange_list,
        blue_list=internal_blue_list
    )


def fetch_question(idx: int) -> dict:
    idx = idx - 1
    return {
        'length': len(table_content.question_answer[idx][1]),
        'label': table_content.question_answer[idx][0],
        'ident': idx
    }