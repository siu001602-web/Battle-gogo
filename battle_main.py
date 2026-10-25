import streamlit as st
import random

st.set_page_config(page_title="심리전 턴제 배틀", page_icon="⚔️", layout="centered")

# 세션 상태 초기화
if "initialized" not in st.session_state:
    st.session_state.max_hp = 5
    st.session_state.player_hp = 5
    st.session_state.ai_hp = 5
    st.session_state.turn = 1
    st.session_state.player_wait_turns = 0
    st.session_state.ai_wait_turns = 0
    st.session_state.player_consecutive = 0
    st.session_state.ai_consecutive = 0
    st.session_state.player_ultimate = 0
    st.session_state.ai_ultimate = 0
    st.session_state.player_counter_cooldown = 0
    st.session_state.ai_counter_cooldown = 0
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.log = "심리전투를 시작합니다! 행동을 선택하세요."
    st.session_state.player_history = []
    st.session_state.initialized = True

def reset_game():
    st.session_state.player_hp = 5
    st.session_state.ai_hp = 5
    st.session_state.turn = 1
    st.session_state.player_wait_turns = 0
    st.session_state.ai_wait_turns = 0
    st.session_state.player_consecutive = 0
    st.session_state.ai_consecutive = 0
    st.session_state.player_ultimate = 0
    st.session_state.ai_ultimate = 0
    st.session_state.player_counter_cooldown = 0
    st.session_state.ai_counter_cooldown = 0
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.player_history = []
    st.session_state.log = "게임이 초기화되었습니다. 다시 시작하세요!"

def render_hp(current_hp, max_hp=5):
    return f"{'❤️' * current_hp}{'🖤' * (max_hp - current_hp)} ({current_hp}/{max_hp})"

def get_ai_choice(player_history, ai_ultimate, ai_counter_cooldown):
    if ai_ultimate >= 3 and random.random() < 0.7:
        return "필살기"
    choices = ["공격", "방어", "치료", "존버"]
    if ai_counter_cooldown == 0:
        choices.append("반격")
    if not player_history:
        return random.choice(choices)
    
    last_action = player_history[-1]
    weights = [3 if last_action == "공격" and c in ["방어", "반격"] else 1 for c in choices]
    return random.choices(choices, weights=weights, k=1)[0]

st.title("⚔️ 심리전 턴제 배틀 게임")
st.write("공격, 방어, 치료, 존버, 반격, 필살기를 활용해 상대와 겨루세요!")
st.divider()

p_hp, ai_hp = st.session_state.player_hp, st.session_state.ai_hp
p_ult, ai_ult = st.session_state.player_ultimate, st.session_state.ai_ultimate

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("내 체력", f"{render_hp(p_hp)}\n✨ 게이지({p_ult}/3)")
with col2:
    st.metric("현재 턴", f"{st.session_state.turn}턴")
with col3:
    st.metric("상대 체력", f"{render_hp(ai_hp)}\n✨ 게이지({ai_ult}/3)")

st.divider()

if st.session_state.game_over:
    if st.session_state.winner == "player":
        st.success("🎉 승리했습니다!")
    else:
        st.error("💀 패배했습니다...")
    if st.button("다시 하기"):
        reset_game()
        st.rerun()
else:
    st.subheader("행동 선택")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    player_choice = None
    
    with c1:
        if st.button("⚔️ 공격"): player_choice = "공격"
    with c2:
        if st.button("🛡️ 방어"): player_choice = "방어"
    with c3:
        if st.button("💊 치료"): player_choice = "치료"
    with c4:
        if st.button("⏳ 존버"): player_choice = "존버"
    with c5:
        if st.button("🥊 반격", disabled=(st.session_state.player_counter_cooldown > 0)): player_choice = "반격"
    with c6:
        if st.button("✨ 필살기", disabled=(p_ult < 3)): player_choice = "필살기"

    if player_choice:
        st.session_state.player_history.append(player_choice)
        ai_choice = get_ai_choice(st.session_state.player_history, ai_ult, st.session_state.ai_counter_cooldown)
        
        p_dmg, ai_dmg = 0, 0
        if player_choice == "필살기":
            st.session_state.player_ultimate = 0
            p_dmg = 3
        elif player_choice == "공격":
            p_dmg = 1
        elif player_choice == "치료":
            st.session_state.player_hp = min(5, st.session_state.player_hp + 1)
        elif player_choice == "존버":
            st.session_state.player_wait_turns = 2
            st.session_state.player_ultimate = min(3, st.session_state.player_ultimate + 1)
        elif player_choice == "방어":
            st.session_state.player_ultimate = min(3, st.session_state.player_ultimate + 1)
        elif player_choice == "반격":
            st.session_state.player_counter_cooldown = 3
            if ai_choice == "공격": p_dmg = 2

        if ai_choice == "필살기":
            st.session_state.ai_ultimate = 0
            ai_dmg = 3
        elif ai_choice == "공격" and player_choice != "방어":
            ai_dmg = 1
        elif ai_choice == "존버":
            st.session_state.ai_ultimate = min(3, st.session_state.ai_ultimate + 1)

        st.session_state.player_hp = max(0, st.session_state.player_hp - ai_dmg)
        st.session_state.ai_hp = max(0, st.session_state.ai_hp - p_dmg)
        st.session_state.turn += 1
        st.session_state.log = f"당신: {player_choice} | 상대: {ai_choice}"
        
        if st.session_state.player_hp == 0 or st.session_state.ai_hp == 0:
            st.session_state.game_over = True
            st.session_state.winner = "player" if st.session_state.ai_hp == 0 else "ai"
        st.rerun()

st.divider()
st.info(st.session_state.get("log", "게임을 시작하세요!"))
