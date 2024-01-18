import pandas as pd
import streamlit as st
from scipy.optimize import minimize

def main():

    # データの作成
    data = {
        "食品": ["リンゴ", "バナナ", "トマト", "ブロッコリー", "鶏胸肉", "牛肉", "サーモン", "ブラウンライス", "パスタ",
                "キウイ", "オレンジ", "ヨーグルト", "アーモンド", "ハチミツ", "チーズ", "カレーライス", "トースト", "卵",
                "シリアル", "ミルク", "ホットドッグ", "ピザ", "フライドチキン", "ポテトチップス", "チョコレート", "ビール",
                "ワイン", "サラダ", "豆腐", "ステーキ"],
        "カロリー": [52, 96, 18, 34, 165, 250, 206, 112, 157,
                    41, 43, 59, 575, 304, 402, 541, 264, 68,
                    377, 42, 150, 285, 335, 152, 546, 154,
                    85, 152, 144, 679],
        "たんぱく質": [0.3, 1.1, 0.9, 2.8, 31, 27, 22, 2.6, 6.1,
                    0.8, 1.0, 3.5, 21, 0.3, 25, 6.8, 8.1, 5.5,
                    6.4, 3.4, 6.0, 12.0, 25.0, 2.0, 4.9, 1.6,
                    0.1, 1.8, 8, 57],
        "脂質": [0.2, 0.3, 0.2, 0.4, 3.6, 17, 13, 0.9, 1.1,
                0.4, 0.2, 0.4, 49, 0, 33, 30, 9.2, 4.8,
                5.0, 1.0, 5.0, 10.0, 15.0, 10.0, 31.0, 0,
                0, 0.1, 8, 48],
        "炭水化物": [14, 23, 3.9, 7, 0, 0, 0, 23, 30,
                10, 11, 4.7, 22, 82, 1.3, 75, 28, 0.6,
                82, 5.0, 2.0, 36.0, 0, 16.0, 59.3, 13,
                2.6, 3.0, 2, 0]
    }
    df = pd.DataFrame(data)


    # タイトル
    st.title('栄養成分情報')

    # データの表示
    st.write(df)

    # ユーザー入力
    food = st.selectbox('食品を選択してください', df['食品'].unique())
    desired_calories = st.number_input('目標カロリーを入力してください', min_value=0.0, max_value=5000.0, value=2000.0)
    desired_protein = st.number_input('目標たんぱく質量（g）を入力してください', min_value=0.0, max_value=500.0, value=50.0)

    # 選択した食品の栄養成分を表示
    selected_food = df[df['食品'] == food]
    st.write(selected_food)

    # 最適化
    def objective(x):
        # 脂質と炭水化物の摂取量を最小化
        return selected_food['脂質'].values[0] * x[0] + selected_food['炭水化物'].values[0] * x[1]

    def constraint1(x):
        # カロリーの制約
        return selected_food['カロリー'].values[0] * x[0] + selected_food['カロリー'].values[0] * x[1] - desired_calories

    def constraint2(x):
        # たんぱく質の制約
        return selected_food['たんぱく質'].values[0] * x[0] + selected_food['たんぱく質'].values[0] * x[1] - desired_protein

    cons = [{'type':'eq', 'fun': constraint1},
            {'type':'eq', 'fun': constraint2}]
    x0 = [0, 0] # 初期値
    solution = minimize(objective, x0, constraints=cons)

    if solution.success:
        st.write(f"最適な摂取量: 脂質 {solution.x[0]}g, 炭水化物 {solution.x[1]}g")
    if not solution.success:
        st.write("最適解が見つかりませんでした。目標カロリーやたんぱく質量を変えて再度試してください。")

if __name__ =='__main__':
    main()
