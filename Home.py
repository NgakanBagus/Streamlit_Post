import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from utils import visualize_type

url: str = 'https://docs.google.com/spreadsheets/d/1JMutCrRaKG3PsU0fgve98aSjKAP4miARE9hIGAQRSdk/edit?usp=sharing'
conn: GSheetsConnection = st.experimental_connection('job_skills', type=GSheetsConnection)

df: pd.DataFrame = conn.read(spreadsheet=url, worksheet=0)

st.header('TOP ANIME IN IMDB')
st.subheader('')
st.write('Didapatkan dari dataset kaggle')
st.dataframe(df)

st.sidebar.header("Anime Filter: ")
Genre = st.sidebar.multiselect(
    "Select the genre: ",
    options=df["Genre"].unique(),
    default=df["Genre"].unique()

    
)




