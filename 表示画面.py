import streamlit as st
import pandas as pd

st.set_page_config(page_title="タスクアプリ")
if "batch_size" not in st.session_state:
    st.session_state["batch_size"] = 10
if "start_pos" not in st.session_state:
    st.session_state["start_pos"] = 0


@st.cache_data(show_spinner=False)
def load_data(csv_file):
    data = pd.read_csv(csv_file)
    data["kigen"] = pd.to_datetime(data["kigen"])
    data["cost"] = pd.to_numeric(data["cost"])
    data["complete"] = pd.to_numeric(data["complete"])
    return data


data = load_data("tasks_data.csv")

header = st.columns((3, 5))
with header[0]:
    st.title("タスク一覧")
with header[1]:
    with st.expander("タスクを作る"):
        with st.form("create_task"):
            form_name = st.text_input("名前", key="namae")
            form_description = st.text_area("詳細", max_chars=100, key="shousai")
            form_time_limit = st.date_input(
                "期限", value="today", key="kigen", format="YYYY-MM-DD"
            )
            form_importance = st.number_input(
                "優先順位", key="yuusen_juni", min_value=0, placeholder=len(data) + 1
            )
            form_cost = st.number_input("費用", key="cost", min_value=0)
            form_complete = st.checkbox("もう完了されました", key="complete")
            form_submit = st.form_submit_button("タスクを作る")
            if form_submit:
                form_data = {
                    "namae": form_name,
                    "shousai": form_description,
                    "kigen": form_time_limit,
                    "yuusen_juni": form_importance,
                    "cost": form_cost,
                    "complete": form_complete,
                }
                data[len(data)] = form_data
                data.to_csv("data_faker.csv", index=False)


st.write(data)
sort = st.selectbox("データの順分を変える？", options=["いいえ", "はい"])
if sort == "はい":
    show_df = data_df.copy()
    label_change_dict = {"タスクの期限": "kigen", "タスクの優先順位": "yuusen_juni", "費用": "cost"}
    sort_category = st.multiselect("カテゴリ", options=["タスクの期限", "タスクの優先順位", "費用"])
    sub_menu = st.columns(2)
    with sub_menu[0]:
        sort_direction = st.selectbox("順序", options=["昇順⬇️", "降順⬆️"])
    with sub_menu[1]:
        completed_task = st.selectbox("完了?", ["", "はい", "いいえ"])
    if len(sort_category) > 0 and sort_direction != "":
        df_sort_list = [label_change_dict[i] for i in sort_category]
        temp_df = data.sort_values(
            by=df_sort_list,
            ascending=sort_direction == "昇順⬇️",
        )
        if completed_task == "":
            hyouji_df = temp_df
        elif completed_task == "はい":
            hyouji_df = temp_df[temp_df["complete"] == 1]
        else:
            hyouji_df = temp_df[temp_df["complete"] == 0]
    else:
        hyouji_df = data
else:
    hyouji_df = data


num_rows = len(hyouji_df)

row_indices = [
    i
    for i in range(
        st.session_state["start_pos"],
        st.session_state["start_pos"] + st.session_state["batch_size"],
    )
]
row_data = hyouji_df.iloc[row_indices]

for row in row_data.itertuples():
    with st.empty():
        with st.container():
            st.markdown(f"#### {row.namae}")
            st.write(row.shousai)
            text_cols = st.columns(5)
            with text_cols[0]:
                st.write(f"期限: {str(row.kigen.strftime('%Y-%m-%d'))}")
            with text_cols[1]:
                st.write(f"優先順位: {str(row.yuusen_juni)}")
            with text_cols[2]:
                st.write(f"費用: {str(row.cost)}円")
            with text_cols[3]:
                if row.complete:
                    st.write("完了？ はい")
                else:
                    st.write("完了？ いいえ")
            with text_cols[4]:
                st.button("編集", on_click="", key=row.namae, use_container_width=True)

    st.session_state["start_pos"] = row_indices[-1] + 1


footer = st.columns((4, 1, 1))
with footer[2]:
    batch_size = st.session_state["batch_size"]
    st.session_state["batch_size"] = st.selectbox("タスク数", options=[10, 25, 50, 100])
    if batch_size != st.session_state["batch_size"]:
        batch_size = st.session_state["batch_size"]
        st.rerun()
with footer[1]:
    total_pages = (
        int(len(hyouji_df) / st.session_state["batch_size"])
        if int(len(hyouji_df) / st.session_state["batch_size"]) > 0
        else 1
    )
    current_page = st.number_input("ページ", min_value=1, max_value=total_pages, step=1)
with footer[0]:
    st.markdown(f"**{total_pages}**個ページの中の**{current_page}**番目ページ")
