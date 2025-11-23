
import streamlit as st


st.markdown(
    "<h1>おっくうやけどレシートを集計するツールぞね！ <span style='color:black; font-size:20px;'>まだ試作版っす！</span></h1>",
    unsafe_allow_html=True
)



# セッションステート初期化
if "remaining" not in st.session_state:
    st.session_state["remaining"] = []

if "sets" not in st.session_state:
    st.session_state["sets"] = []

if "guess_total" not in st.session_state:
    st.session_state["guess_total"] = ""

if "guess_count" not in st.session_state:
    st.session_state["guess_count"] = ""

# 遊び：予想入力（タイトルは不要）
guess_total = st.text_input("おまさんの全部合計の予想は？（円）", st.session_state["guess_total"])
guess_count = st.text_input("枚数の予想は？", st.session_state["guess_count"])

st.session_state["guess_total"] = guess_total
st.session_state["guess_count"] = guess_count

st.write("---")

# レシート入力欄
input_text = st.text_area(
    "レシート金額を入力するぞね",
    value=" ".join([str(x) for x in st.session_state["remaining"]]),
    height=100
)

# リセットボタン
if st.button("まっさらにするぞね！"):
    st.session_state["remaining"] = []
    st.session_state["sets"] = []
    st.session_state["guess_total"] = ""
    st.session_state["guess_count"] = ""
    st.rerun()

# 目標金額入力
target = st.number_input("1セットの目標金額を入力してよ", min_value=1, value=54000)

colA, colB = st.columns(2)
calc = colA.button("計算するかえ？")
recalc = colB.button("再計算するかね？")

# 計算実行
def run_calc():
    if not input_text.strip():
        st.warning("レシート金額を入力してよ")
        return

    try:
        cleaned = input_text.replace("、", " ").replace(",", " ")
        parts = [p for p in cleaned.split() if p.strip() != ""]
        receipts = [int(x) for x in parts]
    except:
        st.error("数字として読み取れんデータがあるぞね")
        return

    # 入力反映
    st.session_state["remaining"] = receipts.copy()
    st.session_state["sets"] = []

    remaining = st.session_state["remaining"].copy()
    sets = []

    # 自動セット仕分け
    while remaining:
        remaining.sort(reverse=True)
        current = []
        total = 0
        for r in remaining[:]:
            if total + r <= target:
                current.append(r)
                total += r
                remaining.remove(r)
        if not current:
            n = remaining.pop(0)
            current = [n]
            total = n
        sets.append((current, total))

    st.session_state["sets"] = sets

if calc:
    run_calc()

if recalc:
    run_calc()


# 計算結果表示
if st.session_state["sets"]:
    st.markdown("## 計算の結果発表ぞね。")

# セットごと表示
for i, (comb, total) in enumerate(list(st.session_state["sets"])):
    diff = total - target

    if diff == 0:
        comment = "たまるか！"
    elif abs(diff) <= 999:
        comment = "おしいにゃぁ"
    elif abs(diff) >= 33000:
        comment = "どいた？！"
    else:
        comment = "！？"

    st.markdown(f"### 束ぞね{i+1}（{len(comb)}枚）")
    st.write("レシート：" + " ".join([str(x) for x in comb]))
    st.write(f"合計：{total}円 → 差額：{diff:+}円 → {comment}")

    btn_key = f"done_{i}"
    if st.button(f"束ぞね{i+1}を片付けたぞね", key=btn_key):
        for x in comb:
            if x in st.session_state["remaining"]:
                st.session_state["remaining"].remove(x)
        st.session_state["sets"].remove((comb, total))
        st.rerun()

# 全体合計
all_sum = sum(st.session_state["remaining"])
all_count = len(st.session_state["remaining"])

st.write(f"**全部で {all_count} 枚　{all_sum} 円だったぞね。**")
