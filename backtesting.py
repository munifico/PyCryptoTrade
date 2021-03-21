import pybithumb
import numpy as np

FEE = 0.0032


def get_ror(k=0.8):

    df = pybithumb.get_ohlcv("BTC")
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    df['ror'] = np.where(
        df['high'] > df['target'],
        df['close'] / df['target'] - FEE,
        1
    )
# df = df['2020']  2020년의 수익률을 알아보기 위한 코드

    # 거래일 마다의 기간 수익률
    df['hpr'] = df['ror'].cumprod()
    
    df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
    MDD = df['dd'].max()
    print(MDD)
    return df


# for k in np.arange(0.1, 1.0, 0.1):
#     ror = get_ror(k)
#     print(f'k={k} 일때, 수익률 {ror}')


df = get_ror()
df.to_excel("btc.xlsx")