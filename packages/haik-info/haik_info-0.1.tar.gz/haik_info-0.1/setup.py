from pykakasi import kakasi
from setuptools import setup, find_packages
import json
# 関数のラップ


def haik_info(user_haiku):
    """
    与えられた俳句のリストを分析し、季語、読み、俳句のタイプ、各行の音節数を識別します。

    Args:
        haiku (list of str): 分析する俳句。音節ごとの配列。

    Returns:
        dict: 分析結果を含む辞書。以下のキーを持ちます:
            - kigo (list of str): 季語のリスト。季語が見つからない場合は空のリスト。
            - yomi (list of str): 各行の読みのリスト。
            - type (str): 俳句のタイプ（例: 'haiku', 'senryu', 'tanka'）。
            - len (list of int): 各行の音節数のリスト。

    Example:
        >>> user_haiku = ["古池", "蛙飛び込む", "水の音"]
        >>> result = haik_info(user_haiku)
        >>> print(result)
    """
    # JSONデータを読み込む
    with open('kigo.json', 'r', encoding='utf-8') as f:
        kigo_data = json.load(f)

    # 俳句を入力として受け取り、含まれている季語のリストを返す関数を定義

    # Kakasiの初期化
    kakasi_instance = kakasi()

    def hiragana(text):

        kakasi_instance.setMode('J', 'H')
        conv = kakasi_instance.getConverter()
        if type(text) is str:
            return conv.do(text)
        else:

            return_lists = []
            for i in text:
                return_lists.append(conv.do(i))
            return return_lists

    def check_len(text):
        shi_type = ""
        if len(text) == 5:
            shi_type = "tanka"
            shi_len1 = int(len(hiragana(text[0]))-5)
            shi_len2 = int(len(hiragana(text[1]))-7)
            shi_len3 = int(len(hiragana(text[2]))-5)
            shi_len4 = int(len(hiragana(text[3]))-7)
            shi_len5 = int(len(hiragana(text[4]))-7)
            return shi_type, [shi_len1, shi_len2, shi_len3, shi_len4, shi_len5]
        elif len(text) == 3:
            shi_len1 = int(len(hiragana(text[0]))-5)
            shi_len2 = int(len(hiragana(text[1]))-7)
            shi_len3 = int(len(hiragana(text[2]))-5)
            if check_kigo("".join(text), kigo_data) == True:
                shi_type = "haiku"
            else:
                shi_type = "senryu"
            return shi_type, [shi_len1, shi_len2, shi_len3]
        else:
            shi_type = "jiyu_ritsu_haiku"
            return shi_type, ["IT IS FREEDOM."]

    def find_kigo(haiku, kigo_list):
        found_kigo = set()  # 重複を削除するためにセットを使用
        for kigo_entry in kigo_list:
            kigo = kigo_entry['kigo']
            readings = kigo_entry['readings']
            for reading in readings:
                if kigo in haiku or reading in haiku:
                    found_kigo.add(kigo)
                    break  # 一度見つかったら中止
        if list(found_kigo):
            return list(found_kigo)
        else:
            return False

    def check_kigo(haiku, kigo_list):
        found_kigo = set()  # 重複を削除するためにセットを使用
        for kigo_entry in kigo_list:
            kigo = kigo_entry['kigo']
            readings = kigo_entry['readings']
            for reading in readings:
                if kigo in haiku or reading in haiku:
                    found_kigo.add(kigo)
                    break  # 一度見つかったら中止
        if list(found_kigo):
            return True
        else:
            False

    # ユーザーから俳句を入力として受け取り、含まれている季語の配列を表示
    types, lens = check_len(user_haiku)
    found_kigo = {
        "kigo": find_kigo(''.join(user_haiku), kigo_data),
        "yomi": hiragana(user_haiku),
        "type": types,
        "len": lens
    }
    return found_kigo


# setup.py の基本的な内容
setup(
    name='haik_info',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pykakasi'
    ],
    python_requires='>=3.6',
)
