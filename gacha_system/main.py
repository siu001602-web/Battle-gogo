import streamlit as st
import random

st.set_page_config(page_title="능력 뽑기 시스템", page_icon="✨", layout="centered")

if "gems" not in st.session_state:
    st.session_state.gems = 1000
if "abilities" not in st.session_state:
    st.session_state.abilities = []

ABILITIES_POOL = {
    "3성": ["⚔️ 검투사 (필살기 시 50% 확률 데미지 2배)"],
    "4성": [
        "💊 힐러 (필살기 시 70% 확률 체력 3 회복)",
        "🚨 경찰 (필살기 시 70% 확률 상대 기술 1개 밴)"
    ],
    "5성": ["🤡 광대 (필살기 시 60% 확률 상대 피 -3 / 40% 본인 피 -2)"]
}

def roll_single():
    rand = random.random() * 100
    if rand < 0.1: tier = "5성"
    elif rand < 5.1: tier = "4성"
    else: tier = "3성"
    return {"tier": tier, "name": random.choice(ABILITIES_POOL[tier])}

st.title("✨ 능력 뽑기 시스템")
st.info("""
**📋 [확률 안내]**
* 🌟 **5성 (광대)** : **0.1%**
* ✨ **4성 (힐러, 경찰)** : **5.0%**
* 🔹 **3성 (검투사)** : **94.9%**
*(※ 10연차 시 4성 이상 1개 확정!)*
""")

st.metric("보유 보석", f"💎 {st.session_state.gems}개")
st.divider()

col1, col2 = st.columns(2)
with col1:
    if st.button("🎲 1회 뽑기 (보석 100개)"):
        if st.session_state.gems >= 100:
            st.session_state.gems -= 100
            res = roll_single()
            st.session_state.abilities.append(res)
            st.success(f"획득! [{res['tier']}] {res['name']}")
            if res["tier"] == "5성": st.balloons()
        else:
            st.error("보석 부족!")

with col2:
    if st.button("✨ 10연차 (보석 1000개 - 4성 확정)"):
        if st.session_state.gems >= 1000:
            st.session_state.gems -= 1000
            results = [roll_single() for _ in range(10)]
            if not any(item["tier"] in ["4성", "5성"] for item in results):
                gt = "5성" if random.random() * 100 < 2 else "4성"
                results[-1] = {"tier": gt, "name": random.choice(ABILITIES_POOL[gt])}
            st.session_state.abilities.extend(results)
            st.success("10연차 완료!")
            for r in results:
                st.write(f"- [{r['tier']}] {r['name']}")
            if any(r["tier"] == "5성" for r in results): st.balloons()
        else:
            st.error("보석 부족!")

if st.button("💎 보석 1000개 무료 충전"):
    st.session_state.gems += 1000
    st.rerun()

st.divider()
st.subheader("🎒 내 능력 목록")
if st.session_state.abilities:
    counts = {}
    for ab in st.session_state.abilities:
        key = f"[{ab['tier']}] {ab['name']}"
        counts[key] = counts.get(key, 0) + 1
    for name, cnt in counts.items():
        st.write(f"- **{name}** : {cnt}개 보유")
else:
    st.write("보유한 능력이 없습니다.")
