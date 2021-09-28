from datetime import timedelta

import pandas as pd
import numpy as np

if __name__ == "__main__":
    df = pd.read_csv('Trello-天助定-统计.csv',
                     header=0, sep=',')
    # print(df)
    # print(df.dtypes)
    i = 0
    for col_name in df:
        if col_name.startswith("雨琦") or col_name.startswith("耿鑫") \
                or col_name.startswith("何文俊") or col_name.startswith("hui") \
                or col_name.startswith("闫雪") or col_name.startswith("韩亚莉"):
            print('找到一个名字:{}, 第{}列'.format(col_name, i))
            break
        i += 1

    df_slice = df.iloc[:, i:]
    print(df_slice)

    # df_slice = pd.to_timedelta(df_slice)
    # print(df_slice.dtypes)

    for col_name in df_slice:
        if col_name == 'Card':
            continue
        print(col_name)
        df[col_name] = pd.to_timedelta(df_slice[col_name])
        df[col_name] = df[col_name].map(lambda x: x.total_seconds() / 3600 / 8)
        print(df[col_name].dtypes)
        # df[col_name].astype(pd.Timedelta)

    print('---------------')
    sum_series = df.sum()
    print(sum_series)

    # print(df)
