import json
import aiosqlite
import asyncio
import pandas as pd
import streamlit as st

from test_tele.config import CONFIG_FILE_NAME, read_config, write_config
from test_tele.database.db_helper import Query
from test_tele.config_bot import read_bot_config, write_bot_config
from test_tele.web_ui.password import check_password
from test_tele.web_ui.utils import hide_st, export_dataframe, get_list, get_string

CONFIG = read_config()
BOT_CONFIG = read_bot_config()

query = Query()
con = asyncio.run(aiosqlite.connect('ttele.db', uri=True))

st.set_page_config(
    page_title="All Datas",
    page_icon="📒",
)

hide_st(st)


# Mengambil data seluruh Mata Kuliah
@st.cache_resource(show_spinner="Loading user datas")
def get_users():
    users = asyncio.run(query.read_data('users'))
    result = []

    if users:
        for user in users:
            result.append({"id": user[0], "username": user[1], "chat_id": user[2], "firstname": user[3], "is_subscriber": user[4], "is_full_subscriber": user[5]})
        return result
    
    result = [{"id": 1, "username": None, "chat_id": None, "firstname": None, "is_subscriber": None, "is_full_subscriber": None}]
    return result


# Tambah data dari tabel
# def simpan_data(table, conn, keys, data_iter):
#     data = [dict(zip(keys, row)) for row in data_iter]

#     for x in data:
#         id, unique_id, nama_matkul, metode, sks, peserta = x['id'], x['unique_id'], x['nama_matkul'], x['metode'], x['sks'], x['perkiraan_peserta']
#         add_matkul(id, unique_id, nama_matkul, metode, sks, peserta)



# Konten dari tab1 Tampil data ruang
def inside_tab1():
    user = get_users()
    savetable = False
    export_csv = False

    cols = st.columns([1,1,1,6])
    with cols[0]:
        refresh_btn = st.button("Refresh")
    with cols[1]:
        simpan_btn = st.button('Simpan')
    with cols[2]:
        export_btn = st.button('Export')

    if refresh_btn:
        st.cache_resource.clear()
        st.rerun()
    if simpan_btn:
        savetable = True
    if export_btn:
        export_csv = True

    df = pd.DataFrame(user)
    edited_df = st.data_editor(
        df, 
        column_order=['chat_id', 'username', 'firstname', 'is_subscriber', 'is_full_subscriber'],
        column_config={
            "chat_id": st.column_config.NumberColumn("Chat ID"),
            "username": st.column_config.TextColumn("Username"), 
            "firstname": st.column_config.NumberColumn("First Name"),
            "is_subscriber": st.column_config.CheckboxColumn("Subscribe", default=False),
            "is_full_subscriber": st.column_config.CheckboxColumn("Full Subscribe", default=False)
        },
        num_rows="dynamic", 
        use_container_width=True, 
        hide_index=False
        )

    if savetable:
        savetable = False
        edited_df.to_sql('courses', con, if_exists='append', index=False, method='multi')
        st.cache_resource.clear()
        st.rerun()
    
    if export_csv:
        export_csv = False
        export_dataframe(st, user, 'ttele users.csv')


if check_password(st):
    st.header("Data Mata Kuliah 📓")
    tab1, tab2 = st.tabs(
        ["Data Mata Kuliah", "Tambah Data Mata Kuliah"])

    with tab1:
        inside_tab1()
    with tab2:
        # with st.expander("Tambah Data Manual", expanded=False):
        #     inside_tab2()
        # with st.expander("Import Data", expanded=False):
        #     import_section()

        st.write("Test")


