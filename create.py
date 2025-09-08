import streamlit as st
import pandas as pd
import sqlite3


st.title('FURNITURE DATABASE SYSTEM')
rcolumn, ccolumn, lcolumn = st.columns(3)


st.image('sjlogo.png',width=250)
st.session_state.cdata = pd.DataFrame({
            "user_name":pd.Series(dtype="str"),
            "user_id": pd.Series(dtype="str"),
            "user_status": pd.Series(dtype="str"),
            "level": pd.Series(dtype="str"),
            "stream": pd.Series(dtype="str"),
            "desk_sj":pd.Series(dtype="str"),
            "desk_status": pd.Series(dtype="str"),
            "chair_sj": pd.Series(dtype="str"),
            "chair_status": pd.Series(dtype="str"),
            "locker_No":pd.Series(dtype="str"),
            "locker_status": pd.Series(dtype="str"),
            "Cupboard_sj":pd.Series(dtype="str"),
            "Cupboard_status": pd.Series(dtype="str"),
            "Block":pd.Series(dtype="str"),
            "Room_No":pd.Series(dtype="str"),
            "Floor": pd.Series(dtype="str"),
            "Table_sj":pd.Series(dtype="str"),
            "Table_status": pd.Series(dtype="str"),
            "Year_issued":pd.Series(dtype="str"),
            "Gender":pd.Series(dtype="str"),
            "Date_Returned": pd.Series(dtype="object"),
            

        })
if "save" not in st.session_state:
    st.session_state.save = False



    # Initialize session_state.cdata only once
    if "cdata" not in st.session_state:
        st.session_state.cdata = pd.DataFrame({
            "user_name":pd.Series(dtype="str"),
            "user_id": pd.Series(dtype="str"),
            "user_status": pd.Series(dtype="str"),
            "level": pd.Series(dtype="str"),
            "stream": pd.Series(dtype="str"),
            "desk_sj":pd.Series(dtype="str"),
            "desk_status": pd.Series(dtype="str"),
            "chair_sj": pd.Series(dtype="str"),
            "chair_status": pd.Series(dtype="str"),
            "locker_No":pd.Series(dtype="str"),
            "locker_status": pd.Series(dtype="str"),
            "Cupboard_sj":pd.Series(dtype="str"),
            "Cupboard_status": pd.Series(dtype="str"),
            "Block":pd.Series(dtype="str"),
            "Room_No":pd.Series(dtype="str"),
            "Floor": pd.Series(dtype="str"),
            "Table_sj":pd.Series(dtype="str"),
            "Table_status": pd.Series(dtype="str"),
            "Year_issued":pd.Series(dtype="str"),
            "Gender":pd.Series(dtype="str"),
            "Date_Returned": pd.Series(dtype="object"),
            

        })

# Always show the data editor if cdata exists
if "cdata" in st.session_state:
    st.session_state.cdata = st.data_editor(
        st.session_state.cdata,
        num_rows="dynamic",
        key="cdata_editor_unique"  # Keep a fixed key to preserve edits
    )

    levels=st.selectbox('select Level:',[
           'FORM1',
           'FORM2',
           'FORM3',
           'FORM4',
           'FORM5',
           'FORM6', 
           'STAFF',
            ])
    
  

     
# --- DATABASE SETUP ---
def init_db(levels):
    conn = sqlite3.connect("furniture.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {levels} (
            user_name TEXT,
            user_id TEXT PRIMARY KEY,
            user_status TEXT,
            level TEXT,
            stream TEXT,
            desk_sj TEXT,
            desk_status TEXT,
            chair_sj TEXT,
            chair_status TEXT,
            locker_No TEXT,
            locker_status TEXT,
            Cupboard_sj TEXT,
            Cupboard_status TEXT,
            Block TEXT,
            Room_No TEXT,
            Floor TEXT,
            Table_sj TEXT,
            Table_status TEXT, 
            Year_issued TEXT,
            Gender TEXT,
            Date_Returned TEXT
            
        )
    ''')
    conn.commit()
    return conn, cursor

# --- SAVE TO DATABASE ---
def save_to_db(df,levels):
    if df.empty:
        st.warning("No data to save")
        return

    conn, cursor = init_db(levels)
    for _, row in df.iterrows():
        cursor.execute(f"""
            INSERT OR REPLACE INTO {levels} (user_name,user_id,user_status,level,stream,desk_sj,desk_status,chair_sj,chair_status,locker_No,locker_status,Cupboard_sj,Cupboard_status,Block,Room_No,Floor,Table_sj,Table_status,Year_issued,Gender,Date_Returned)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (row['user_name'], row['user_id'], row['user_status'], row['level'],row['stream'],row['desk_sj'],row['desk_status'],row['chair_sj'],row['chair_status'],row['locker_No'],row['locker_status'],row['Cupboard_sj'],row['Cupboard_status'],row['Block'],row['Room_No'],row['Floor'],row['Table_sj'],row['Table_status'],row['Year_issued'],row['Gender'],row['Date_Returned']))
    conn.commit()
    conn.close()
    st.success(f"{len(df)} rows saved successfully to {levels}!")
    st.session_state.cdata = st.session_state.cdata.iloc[0:0]  # Clear table

# --- BUTTON TO SAVE ---
if st.button("Save"):
    if levels:
        df = st.session_state.cdata.dropna(how="all")   
        df = df[df.apply(lambda row: row.astype(str).str.strip().ne("").any(), axis=1)]  

        if df.empty:
            st.warning("⚠ No valid data to save. Please fill in the form before saving.")
        else:
            save_to_db(df, levels.replace(" ", "_"))  
            st.success("✅ Data saved successfully!")
    else:
        st.error("Please select a level (table) first.")

   
 
   