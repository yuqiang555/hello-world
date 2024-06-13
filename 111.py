import streamlit as st
import pandas as pd
import random

# 从Excel文件中读取笑话
def load_jokes_from_excel(file_path):
    # 读取Excel文件，假设只有一个列，且没有列名
    df = pd.read_excel(file_path, header=None)
    # 将DataFrame的每一行作为一个笑话
    jokes = df.iloc[:, 0].tolist()
    return jokes

# 假设您的Excel文件路径是 "D:\liulanqi\Dataset4JokeSet.xlsx"
# 使用原始字符串来避免转义字符的问题
jokes_excel_path = r"D:\liulanqi\Dataset4JokeSet.xlsx"

# 从Excel文件中加载笑话
jokes = load_jokes_from_excel(jokes_excel_path)

# 缓存计算用户满意度的函数
@st.cache_data
def calculate_satisfaction_score(ratings):
    return sum(ratings) / len(ratings)

# 主函数
def main():
    st.title("笑话评分系统")

    # 上传Excel文件
    uploaded_file = st.file_uploader("上传包含笑话的Excel文件", type="xlsx")

    if uploaded_file is not None:
        # 从Excel文件中加载笑话
        jokes = load_jokes_from_excel(uploaded_file)
        
        # 随机选择三个笑话
        selected_jokes = random.sample(jokes, 3)

        # 创建一个表单来评分前三个笑话
        with st.form("joke_rating_form"):
            # 用户对三个笑话进行评分
            ratings = []
            for i, joke in enumerate(selected_jokes):
                ratings.append(st.slider(f"{joke} 的评分:", 0, 5, key=f"{joke}_{i}"))

            # 提交按钮
            submit_button = st.form_submit_button("提交评分")

        # 根据评分推荐五个笑话
        if submit_button:
            recommended_jokes = random.sample(jokes, 5)

            # 创建另一个表单来评分后五个笑话
            with st.form("recommended_jokes_form"):
                # 用户对五个推荐的笑话进行评分
                recommended_ratings = []
                for i, joke in enumerate(recommended_jokes):
                    recommended_ratings.append(st.slider(f"{joke} 的评分:", 0, 5, key=f"{joke}_{i}"))

                # 提交按钮
                submit_recommended_button = st.form_submit_button("提交评分")

            # 计算用户满意度
            if submit_recommended_button:
                if all(recommended_ratings):  # 确保所有评分都已填写
                    satisfaction_score = calculate_satisfaction_score(recommended_ratings)
                    # 创建一个DataFrame来显示评分
                    ratings_df = pd.DataFrame({
                        "笑话": recommended_jokes,
                        "评分": recommended_ratings
                    })
                    # 显示评分表格
                    st.dataframe(ratings_df)
                    # 显示综合评分
                    st.write(f"用户满意度评分: {satisfaction_score:.2f}/5")

if __name__ == "__main__":
    main()