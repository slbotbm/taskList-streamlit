import streamlit as st
from datetime import datetime
import pandas as pd


@st.cache_data(show_spinner=False)
def load_data(csv_file):
    data = pd.read_csv(csv_file)
    data["time_limit"] = pd.to_datetime(data["time_limit"], format="mixed")
    data["importance"] = pd.to_numeric(data["importance"])
    data["cost"] = pd.to_numeric(data["cost"])
    data["complete"] = pd.to_numeric(data["complete"])
    data["created_at"] = pd.to_datetime(data["created_at"], format="mixed")
    data["updated_at"] = pd.to_datetime(data["updated_at"], format="mixed")
    return data


def edit_data():
    st.session_state["data_df"].at[
        st.session_state["task_index"], "name"
    ] = st.session_state["task_name"]
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

    del st.session_state["task_index"]
    del st.session_state["task_name"]
    del st.session_state["task_details"]
    del st.session_state["task_time_limit"]
    del st.session_state["task_cost"]
    del st.session_state["task_category"]
    del st.session_state["task_complete"]
    del st.session_state["task_importance"]

    st.session_state["data_df"].to_csv("tasks_data.csv", index=False)


def create_data():
    if (
        st.session_state["new_task_name"] != ""
        and st.session_state["new_task_details"] != ""
    ):
        data_to_insert = {
            "name": st.session_state["new_task_name"],
            "details": st.session_state["new_task_details"],
            "time_limit": pd.Timestamp(st.session_state["new_task_time_limit"]),
            "importance": st.session_state["new_task_importance"],
            "cost": st.session_state["new_task_cost"],
            "category": st.session_state["new_task_category"],
            "complete": 1 if st.session_state["new_task_complete"] == "はい" else 0,
            "updated_at": pd.Timestamp(datetime.now()),
            "created_at": pd.Timestamp(datetime.now()),
        }
        print(data_to_insert)
        st.session_state["data_df"].loc[
            len(st.session_state["data_df"])
        ] = data_to_insert
        st.session_state["data_df"].to_csv("tasks_data.csv", index=False)


def show_tasks(df):
    if (
        "task_name" in st.session_state.keys()
        and "task_index" in st.session_state.keys()
    ):
        edit_data()
        st.rerun()
    if "new_task_name" in st.session_state:
        create_data()

    if len(df) > 0:
        st.write(f"タスクの数：{len(st.session_state['data_df'])}")
        for row in df.iterrows():
            with st.container(border=True):
                st.markdown(f"##### {row[1]['name']}")
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
                    sub_column = st.columns(2)
                    with sub_column[0]:
                        edit_button = st.button(
                            "編集", key=str(row[0]) + "_edit", use_container_width=True
                        )
                    with sub_column[1]:
                        delete_button = st.button(
                            "削除", key=str(row[0]) + "_delete", use_container_width=True
                        )
            if delete_button:
                st.session_state["data_df"] = st.session_state["data_df"].drop(row[0])
                st.session_state["data_df"].to_csv("tasks_data.csv", index=False)
                st.rerun()

            if edit_button:
                with st.form("edit_form", border=True):
                    st.text_input(
                        "タスクの名前", value=row[1]["name"], max_chars=50, key="task_name"
                    )
                    st.text_area("タスクの詳細", value=row[1]["details"], key="task_details")
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
                            "タスクのコスト",
                            value=row[1]["cost"],
                            min_value=0,
                            key="task_cost",
                        )
                    with form_columns_2[0]:
                        st.selectbox(
                            "タスクのカテゴリ",
                            options=st.session_state["data_df"]["category"].unique(),
                            key="task_category",
                        )
                    with form_columns_2[1]:
                        st.selectbox(
                            "完了？", options=["", "はい", "いいえ"], key="task_complete"
                        )
                    st.session_state["task_index"] = row[0]
                    form_submit = st.form_submit_button(
                        type="primary",
                        use_container_width=True,
                        disabled=False,
                    )
    else:
        st.markdown("### 条件に一致しているタスクが見つからなかった")


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


header = st.columns((5, 3))
with header[0]:
    st.markdown("### タスク一覧")
with header[1]:
    create_task = st.button("タスクを作成する", use_container_width=True, type="primary")
if create_task:
    with st.form("create_form", border=True):
        st.text_input("タスクの名前", max_chars=50, key="new_task_name")
        st.text_area("タスクの詳細", key="new_task_details")
        form_columns_1 = st.columns(3)
        form_columns_2 = st.columns(2)
        with form_columns_1[0]:
            st.date_input("タスクの期限", key="new_task_time_limit")
        with form_columns_1[1]:
            st.number_input(
                "タスクの優先順位",
                min_value=1,
                max_value=len(st.session_state["data_df"]) + 2,
                key="new_task_importance",
            )
        with form_columns_1[2]:
            st.number_input("タスクのコスト", min_value=0, key="new_task_cost")
        with form_columns_2[0]:
            st.selectbox(
                "タスクのカテゴリ",
                options=st.session_state["data_df"]["category"].unique(),
                key="new_task_category",
            )
        with form_columns_2[1]:
            st.selectbox("完了？", options=["はい", "いいえ"], key="new_task_complete")
        form_submit = st.form_submit_button(
            type="primary",
            use_container_width=True,
            disabled=False,
        )


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
            options=["仕事", "運動", "家族", "友達"],
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

show_tasks(
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
    temp_var = len(show_df) / st.session_state["batch_size"]
    total_pages = (
        (int(temp_var) + 1 if temp_var - int(temp_var) > 0 else int(temp_var))
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
