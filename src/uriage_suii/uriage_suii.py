#
# ライブラリをインポート
#

import pandas as pd
import numpy as np
import datetime as dt
import glob
import warnings
warnings.simplefilter('ignore')
import os
import sys


#
# 年月の更新用関数
#

def update_year_month(year_month, monthly_difference):
    """年月の指定した月数分増減させる
    
    year_monthをmonthly_diffenceの分だけ、月数を増減させる。
    増加させたい場合は正の値、減少させたい場合は負の値をmonthly_diffenceに指定する
    
    Parametars
    ----------
    year_month: str
        yyyymm形式の年月
    monthly_difference: integer
        year_monthからどれだけの月数を増減させたいかの値
    
    Returns
    ----------
    updated_year_month: str
        year_monthからmonthly_differenceの値分だけ増減させた値
        
    """
    
    if (int(year_month[-2:]) + monthly_difference) < 1:
        # 年が減少するパターン
        updated_year_month = f'{int(year_month[:4]) - 1}{str(int(year_month[-2:]) + monthly_difference + 12).zfill(2)}'
    elif (int(year_month[-2:]) + monthly_difference) > 12:
        # 年が増加するパターン
        updated_year_month = f'{int(year_month[:4]) + 1}{str(int(year_month[-2:]) + monthly_difference - 12).zfill(2)}'
    else:
        # 年が変わらないパターン
        updated_year_month = f'{int(year_month[:4])}{str(int(year_month[-2:]) + monthly_difference).zfill(2)}'
        
    return updated_year_month


#
# 売上月報を読み込んで、直近１２か月の売上推移を作成する
#

# 当月分を読み込んで、純売上額のみ残す
file_path = glob.glob('./売上レポート/商品別売上月報/*商品別売上月報.xlsx')
file_path.sort(reverse=True)
df = pd.DataFrame()
for i, file in enumerate(file_path):
    year_month = os.path.split(file)[1][:6]
    df_tmp = pd.read_excel(file, header=4, index_col=[1,2])
    df_tmp = df_tmp[['総売上額']]
    df_tmp = df_tmp.drop('<<総合計>>', axis=0)
    df_tmp = df_tmp.rename(columns={'総売上額': year_month})
    if i == 0:
        df = df_tmp.copy()
    else:
        df = df.merge(df_tmp, how='outer', left_index=True, right_index=True)
    df = df.fillna(value=0, axis=1)

# マージしやすいように、インデックスを振りなおす
df = df.reset_index(drop=False)
df = df.set_index('商品コード', drop=True)


#
# 商品台帳を読み込み、dfに結合して商品分類列を追加する
#

path_shohin_daicho = glob.glob('商品台帳.xlsx')
df_shohin_daicho = pd.read_excel(path_shohin_daicho[0], header=4, index_col=1, dtype={'コード': 'str', '分類１':'str'})
df_shohin_daicho.index.name = '商品コード'
df_shohin_daicho = df_shohin_daicho.drop('Unnamed: 0', axis=1)
df = df.merge(df_shohin_daicho['分類１'], how='left', left_index=True, right_index=True)


#
# 各商品分類ごとにDataFrameを分ける
#

category_list = {'001':'自社商品（effe）', '002':'自社商品（眼鏡）', '003':'自社商品（雑貨）', '004':'自社商品（その他）',\
                 '101':'OEM（眼鏡）', '102':'OEM（眼鏡パーツ）', '103':'OEM（雑貨）', '104':'OEM（2次加工）', '105':'OEM（その他）',\
                 '201':'外注直（材料）', '202':'外注直（型）', '203':'外注直（2次加工）', '204':'外注直（その他）'}
df_cat = {}
for cat in category_list.keys():
    df_tmp = df.loc[df['分類１']==cat]
    df_tmp = df_tmp.drop('分類１', axis=1)
    if int(cat) < 100:
        df_tmp = df_tmp.sort_values(by='商品名', ascending=True)
    # 一番下に合計行を追加
    df_tmp.loc['99999999999999'] = df_tmp.sum()
    df_tmp.loc['99999999999999', '商品名'] = '合計'
    df_cat[cat] = df_tmp


#
# 各商品分類ごとにExcel出力
#

with pd.ExcelWriter('売上金額推移.xlsx') as writer:
    for cat in category_list.keys():
        df_cat[cat].to_excel(writer, sheet_name=f'{cat}_{category_list[cat]}')


#
# 自社商品の数量の推移を作成
#


# 再度、売上月報を読み込み、売上数量のみを取得する
for i, file in enumerate(file_path):
    year_month = os.path.split(file)[1][:6]
    df_tmp = pd.read_excel(file, header=4, index_col=[1,2])
    df_tmp = df_tmp[['純売上数']]
    df_tmp = df_tmp.drop('<<総合計>>', axis=0)
    df_tmp = df_tmp.rename(columns={'純売上数': year_month})
    if i == 0:
        df = df_tmp.copy()
    else:
        df = df.merge(df_tmp, how='outer', left_index=True, right_index=True)
    df = df.fillna(value=0, axis=1)


# マージしやすいように、インデックスを振りなおす
df = df.reset_index(drop=False)
df = df.set_index('商品コード', drop=True)

# 商品台帳を読み込み、dfに結合して商品分類列を追加する
df = df.merge(df_shohin_daicho['分類１'], how='left', left_index=True, right_index=True)


#
# 各商品分類ごとにDataFrameを分ける
#

df_cat = {}
for cat in category_list.keys():
    if int(cat) < 100:
        df_tmp = df.loc[df['分類１']==cat]
        df_tmp = df_tmp.drop('分類１', axis=1)
        if int(cat) < 100:
            df_tmp = df_tmp.sort_values(by='商品名', ascending=True)
        # 一番下に合計行を追加
        df_tmp.loc['99999999999999'] = df_tmp.sum()
        df_tmp.loc['99999999999999', '商品名'] = '合計'
        df_cat[cat] = df_tmp


#
# 各商品分類ごとにExcel出力
#

with pd.ExcelWriter('売上数量推移.xlsx') as writer:
    for cat in category_list.keys():
        if int(cat) < 100:
            df_cat[cat].to_excel(writer, sheet_name=f'{cat}_{category_list[cat]}')