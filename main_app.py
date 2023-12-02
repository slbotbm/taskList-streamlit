import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np


@st.cache_data(show_spinner=False)
def load_data(csv_file):
    data = pd.read_csv(csv_file)
    data["time_limit"] = pd.to_datetime(data["time_limit"])
    data["importance"] = pd.to_numeric(data["importance"])
    data["cost"] = pd.to_numeric(data["cost"])
    data["complete"] = pd.to_numeric(data["complete"])
    data["created_at"] = pd.to_datetime(data["created_at"])
    data["updated_at"] = pd.to_datetime(data["updated_at"])
    return data


def show_df_in_page(df):
    for row in df.iterrows():
        with st.container():
            st.markdown(f"#### {row[1]['name']}")
            st.write(row[1]["details"])
            columns_1 = st.columns(3)
            columns_2 = st.columns(3)
            with columns_1[0]:
                st.write(f"期限: {str(row[1]['time_limit'].strftime('%Y-%m-%d'))}")
            with columns_1[1]:
                st.write(f"優先順位: {str(row[1]['importance'])}")
            with columns_1[2]:
                st.write(f"費用: {str(row[1]['cost'])}円")
            with columns_2[0]:
                st.write(f"カテゴリ: {row[1]['category']}")
            with columns_2[1]:
                if row[1]["complete"]:
                    st.write(":green[完了された]")
                else:
                    st.write(":red[完了されていない]")
            with columns_2[2]:
                edit_button = st.button("編集", key=row[0], use_container_width=True)
        if edit_button:
            with st.form("form"):
                task_name = st.text_input(
                    "タスコの名前", value=row[1]["name"], max_chars=50, key="task_name"
                )
                task_details = st.text_area(
                    "タスクの詳細", value=row[1]["details"], key="task_details"
                )
                form_columns_1 = st.columns(3)
                form_columns_2 = st.columns(2)
                with form_columns_1[0]:
                    st.date_input(
                        "タスクの期限", value=row[1]["time_limit"], key="task_time_limit"
                    )
                with form_columns_1[1]:
                    st.number_input(
                        "タスクの優先順位",
                        value=row[1]["importance"],
                        min_value=1,
                        max_value=len(st.session_state["data_df"]) + 2,
                        key="task_importance",
                    )
                with form_columns_1[2]:
                    st.number_input(
                        "タスクのコスト", value=row[1]["cost"], min_value=0, key="task_cost"
                    )
                with form_columns_2[0]:
                    st.selectbox(
                        "タスクのカテゴリ",
                        options=st.session_state["data_df"]["category"].unique(),
                        key="task_category",
                    )
                with form_columns_2[1]:
                    task_complete = st.selectbox(
                        "完了？", options=["", "はい", "いいえ"], key="task_complete"
                    )
                st.session_state["task_index"] = row[0]
                submit_activate = False
                if task_complete != "":
                    if task_name.strip() != "":
                        if task_details.strip() != "":
                            submit_activate = True

                form_submit = st.form_submit_button(
                    type="primary",
                    use_container_width=True,
                    disabled=not submit_activate,
                )
                print(form_submit)
                if st.session_state["FormSubmitter:form-Submit"]:
                    edit_data()


def edit_data():
    print("Entered edit_data()")
    print(st.session_state["data_df"].at[st.session_state["task_index"], "name"])
    print(st.session_state["task_name"])
    st.session_state["data_df"].at[
        st.session_state["task_index"], "name"
    ] = st.session_state["task_name"]
    print(st.session_state["data_df"].at[st.session_state["task_index"], "name"])
    st.session_state["data_df"].at[
        st.session_state["task_index"], "details"
    ] = st.session_state["task_details"]
    st.session_state["data_df"].at[
        st.session_state["task_index"], "time_limit"
    ] = st.session_state["task_time_limit"]
    st.session_state["data_df"].at[
        st.session_state["task_index"], "importance"
    ] = st.session_state["task_importance"]
    st.session_state["data_df"].at[
        st.session_state["task_index"], "cost"
    ] = st.session_state["task_cost"]
    st.session_state["data_df"].at[
        st.session_state["task_index"], "category"
    ] = st.session_state["task_category"]
    if st.session_state["task_complete"] == "はい":
        st.session_state["data_df"].at[st.session_state["task_index"], "complete"] = 1
    else:
        st.session_state["data_df"].at[st.session_state["task_index"], "complete"] = 0
    st.session_state["data_df"].loc[
        st.session_state["task_index"], "updated_at"
    ] = datetime.now()
    st.session_state["data_df"].to_csv("tasks_data.py", index=False)


st.set_page_config(
    page_title="タスクアプリ", layout="centered", initial_sidebar_state="collapsed"
)

if "batch_size" not in st.session_state:
    st.session_state["batch_size"] = 10
if "start_pos" not in st.session_state:
    st.session_state["start_pos"] = 0
if "data_df" not in st.session_state:
    st.session_state["data_df"] = load_data("tasks_data.csv")

show_df = st.session_state["data_df"].copy()
st.session_state["data_df"]
st.session_state
st.title("タスク一覧")
sort = st.selectbox("データの順分を変える？", options=["いいえ", "はい"])
if sort == "はい":
    sort_menu_dict = {
        "期限": "time_limit",
        "優先順位": "importance",
        "コスト": "cost",
        "カテゴリ": "category",
        "作成日": "created_at",
        "編集日": "updated_at",
    }

    sort_menu = st.multiselect(
        "表示順位の変更項目",
        options=["期限", "優先順位", "コスト", "作成日", "編集日"],
        placeholder="項目を選択する",
    )

    sub_menu = st.columns(3)
    with sub_menu[0]:
        sort_category = st.multiselect(
            "カテゴリ",
            options=st.session_state["data_df"].unique(),
            placeholder="カテゴリを選択する",
        )
    with sub_menu[1]:
        sort_direction = st.selectbox("順序", options=["昇順⬇️", "降順⬆️"])
    with sub_menu[2]:
        sort_by_completed_task = st.selectbox("完了?", options=["", "はい", "いいえ"])

    if len(sort_menu) > 0:
        sort_menu = [sort_menu_dict[i] for i in sort_menu]
        show_df = st.session_state["data_df"].sort_values(
            by=sort_menu, ascending=sort_direction == "昇順⬇️"
        )
    if len(sort_category) > 0:
        show_df = show_df[show_df["category"].isin(sort_category)]
    if sort_by_completed_task != "":
        if sort_by_completed_task == "はい":
            show_df = show_df[show_df["complete"] == 1]
        else:
            show_df = show_df[show_df["complete"] == 0]


show_df_in_page(
    show_df.iloc[
        st.session_state["start_pos"] : st.session_state["start_pos"]
        + st.session_state["batch_size"]
    ]
)

footer = st.columns((4, 1, 1))

with footer[2]:
    new_batch_size = st.selectbox("タスク数", options=[10, 25, 50, 100])
    if new_batch_size != st.session_state["batch_size"]:
        st.session_state["batch_size"] = new_batch_size
        st.rerun()
with footer[1]:
    total_pages = (
        int(len(show_df) / st.session_state["batch_size"])
        if int(len(show_df) / st.session_state["batch_size"]) > 0
        else 1
    )
    current_page = st.number_input("ページ", min_value=1, max_value=total_pages, step=1)
    if st.session_state["start_pos"] != st.session_state["batch_size"] * (
        current_page - 1
    ):
        st.session_state["start_pos"] = st.session_state["batch_size"] * (
            current_page - 1
        )
        st.rerun()
with footer[0]:
    st.markdown(f"**{total_pages}**ページの中の**{current_page}**番目ページ")
