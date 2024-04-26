# coding: utf-8

# ModManagerのプロファイルフォルダにあるmodlist.txtの並び順を
# ON・OFFを変えずに基準ファイルに基づいて並び変えるツール

# iniの内容
# [general]
# reference_profile = yu    基準となるプロファイル
# target_ptofiles = lilith,test,merge   並び変えたいプロファイル、カンマ区切り複数可
# mo_profile_path = C:\Data\DL2\Python\modlist\profiles\    プロファイルフォルダのパス
# ;mo_modlist_replace = True    modlist.txtを直接書き換えるならTrueで
# mo_modlist_name_in = modlist.txt  一応ファイル名
# mo_modlist_name_out = _modlist.txt    直接書き換えない場合のリネーム

import os
import sys
import pandas as pd
import configparser
import tkinter as tk
from tkinter import messagebox
# import errno

# ファイルの存在チェック
def checkFileExists(target_file):
    if os.path.exists(target_file) == False :
        messagebox.showinfo('エラー','参照先プロファイルにmodlist.txtがありません\n' + target_file)
        sys.exit()

# ini読み込み configparserクラスを使用
ini = configparser.ConfigParser()
ini_path = './modlist2.ini'

# if not os.path.exists(ini_path):
    # raise ← Exceptionを発生
    # raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), ini_path)

ini.read(ini_path, 'UTF-8')

reference_profile = ini.get('general', 'reference_profile') # ソートの元となるプロファイル名
target_profiles = ini.get('general', 'target_ptofiles') # （これはリスト）ソートしたいプロファイル名
mo_profile_path = ini.get('general', 'mo_profile_path') # MOが管理しているプロファイルのパス
in_name = ini.get('general', 'mo_modlist_name_in') # 入力するファイル名、基本は modlist.txt から変えない事
out_name = ini.get('general', 'mo_modlist_name_out') # 出力するファイル名、元ファイルとは変更する事（_modlist.txt など）
# out_replace = ini.get('general', 'mo_modlist_replace')

# reference_filepathの作成
reference_filename = os.path.join(mo_profile_path, reference_profile, in_name)
checkFileExists(reference_filename)

# プロファイル名の数だけループ
for target_profile in target_profiles.split(','):
    # 入力ファイルパスの作成
    target_filename = os.path.join(mo_profile_path, target_profile, in_name)
    # 入力ファイルの存在チェック
    checkFileExists(target_filename)

    # 出力ファイルパスの作成
    output_filename = os.path.join(mo_profile_path, target_profile, out_name)

    # messagebox.showinfo('確認', 'ソート定義' + reference_filename + '\n' + 'ソート対象' + target_filename)

    # 対象ファイル内容を辞書形式に格納
    # （要素にキーでアクセスする、要はhash配列）
    tf_dic = dict() # 辞書型初期化

    # withでopenする場合、処理が終わると自動でファイルを閉じてくれる
    # ファイルハンドラを定義する -> tf
    with open(target_filename, encoding='UTF-8') as tf:
        # ファイルハンドラはイテレータ？なのでforで読み返す
        for line in tf :
            # +No Stretching and Distant Decal Fix
            # ↑の文字列を、文字列添字＋先頭記号を要素として格納する -> [No Stretching and Distant Decal Fix]+
            # 辞書型の初期化は{}で囲む
            # line[1:] ← 2文字目以降全て
            # line[:1] ← 最初から2文字目まで
            # rstrip 右端の空白を削除
            tf_dic.update({line[1:].rstrip() : line[:1]})

    # リスト形式でソート参照先ファイルを読み込み
    # インデックスでアクセスするので普通の配列で良い
    rf_list = list()
    with open(reference_filename, encoding='UTF-8') as rf:
        for line in rf :
            # [modname][flag][0] という辞書リストを作成
            rf_list.append([line[1:].rstrip(), line[:1], '0'])

    # 出力用リスト
    # ソート参照先ファイルからmodname,flag,
    # ターゲットファイルからmodnameで探し、+か-を返す。存在しなければ'!'を返す
    out_list = list()
    for rf_data in rf_list :
        # [modname][flag][]
        out_list.append([rf_data[0], rf_data[1], tf_dic.get(rf_data[0],'!')])

    # ファイルを出力
    # messagebox.showinfo('出力します', output_filename)
    with open(output_filename, 'w', encoding='UTF-8') as of:
        for i in out_list:
            out_line = str(i[2]) + str(i[0]) + "\n"
            of.write(out_line)

