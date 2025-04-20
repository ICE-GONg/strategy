import streamlit as st
import random
import pandas as pd
import numpy as np

# 设置页面配置
st.set_page_config(
    page_title="博弈游戏模拟器",
    page_icon="🎮",
    layout="wide"
)

# 添加自定义CSS样式
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .game-stats {
        padding: 1rem;
        background-color: #f0f2f6;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 标题和介绍
st.title("🎮 博弈游戏模拟器")
st.markdown("""
    欢迎来到博弈游戏模拟器！在这里，你可以体验不同策略之间的对抗和合作。
    通过调整参数和选择策略，观察不同决策的结果。
""")

# 侧边栏设置
with st.sidebar:
    st.header("游戏设置")
    game_mode = st.selectbox(
        "选择游戏模式",
        ["基础模式 - 囚徒困境", "进阶模式 - 公共品博弈", "专家模式 - 多人博弈"]
    )
    
    num_players = st.slider("玩家数量", 2, 4, 2)
    num_rounds = st.slider("回合数", 1, 10, 5)
    
    st.divider()
    st.subheader("策略设置")
    
    if game_mode == "基础模式 - 囚徒困境":
        strategies = {
            f"玩家{i+1}": st.selectbox(
                f"玩家{i+1}策略",
                ["合作", "背叛", "以牙还牙", "随机"],
                key=f"strategy_{i}"
            ) for i in range(num_players)
        }

# 游戏逻辑
def play_prisoners_dilemma(strategies, rounds):
    scores = {player: 0 for player in strategies.keys()}
    history = []
    
    for round in range(rounds):
        round_choices = {}
        for player, strategy in strategies.items():
            if strategy == "合作":
                choice = "合作"
            elif strategy == "背叛":
                choice = "背叛"
            elif strategy == "以牙还牙":
                if round == 0:
                    choice = "合作"
                else:
                    # 模仿上一轮对手的选择
                    opponent = "玩家2" if player == "玩家1" else "玩家1"
                    choice = history[-1][opponent]
            else:  # 随机
                choice = random.choice(["合作", "背叛"])
            round_choices[player] = choice
        
        # 计算得分
        for p1 in strategies.keys():
            for p2 in strategies.keys():
                if p1 >= p2:
                    continue
                if round_choices[p1] == "合作" and round_choices[p2] == "合作":
                    scores[p1] += 3
                    scores[p2] += 3
                elif round_choices[p1] == "背叛" and round_choices[p2] == "合作":
                    scores[p1] += 5
                    scores[p2] += 0
                elif round_choices[p1] == "合作" and round_choices[p2] == "背叛":
                    scores[p1] += 0
                    scores[p2] += 5
                else:  # 都背叛
                    scores[p1] += 1
                    scores[p2] += 1
        
        history.append(round_choices)
    
    return scores, history

# 主游戏界面
if st.button("开始游戏", type="primary"):
    if game_mode == "基础模式 - 囚徒困境":
        scores, history = play_prisoners_dilemma(strategies, num_rounds)
        
        # 显示游戏结果
        st.subheader("🎯 游戏结果")
        
        # 显示每轮的选择
        st.write("##### 每轮选择记录")
        rounds_df = pd.DataFrame(history)
        st.dataframe(rounds_df, use_container_width=True)
        
        # 显示最终得分
        st.write("##### 最终得分")
        scores_df = pd.DataFrame([scores]).T
        scores_df.columns = ["得分"]
        st.dataframe(scores_df, use_container_width=True)
        
        # 可视化得分
        st.bar_chart(scores_df)
        
        # 游戏分析
        st.subheader("🔍 游戏分析")
        max_score = max(scores.values())
        winners = [player for player, score in scores.items() if score == max_score]
        
        st.write(f"**获胜者:** {', '.join(winners)}")
        st.write(f"**最高得分:** {max_score}")
        
        # 策略分析
        cooperation_rates = {}
        for player in strategies.keys():
            coop_count = sum(1 for round in history if round[player] == "合作")
            cooperation_rates[player] = coop_count / num_rounds * 100
            
        st.write("##### 合作率分析")
        for player, rate in cooperation_rates.items():
            st.write(f"{player}的合作率: {rate:.1f}%")
            
    else:
        st.info("其他游戏模式正在开发中，敬请期待！")

# 添加游戏说明
with st.expander("📖 游戏规则说明"):
    st.markdown("""
    ### 囚徒困境规则
    - 每个玩家可以选择**合作**或**背叛**
    - 如果双方都选择合作，各得3分
    - 如果双方都选择背叛，各得1分
    - 如果一方合作一方背叛，背叛者得5分，合作者得0分
    
    ### 策略说明
    - **合作**: 始终选择合作
    - **背叛**: 始终选择背叛
    - **以牙还牙**: 第一轮合作，之后模仿对手上一轮的选择
    - **随机**: 随机选择合作或背叛
    """) 