import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from utils import visualize_type
import altair as alt
from streamlit_option_menu import option_menu
from UI import make_header
from UI import make_footer

url: str = 'https://docs.google.com/spreadsheets/d/1JMutCrRaKG3PsU0fgve98aSjKAP4miARE9hIGAQRSdk/edit?usp=sharing'
conn: GSheetsConnection = st.experimental_connection('imdb_anime', type=GSheetsConnection)

df: pd.DataFrame = conn.read(spreadsheet=url, worksheet=0)
df = df.drop(840)
df = df.drop_duplicates()

make_header()
make_footer()

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Home", "Animation Data", "Animation Filter", "Average Rating Animation"]
    )

if selected == "Home":
    st.header(':rainbow[TOP ANIMATION IN IMDB]')
    st.subheader('Check Your Popular Animation')
    st.write('Obtained from the kaggle dataset')
    
    title_search = st.text_input("Animation Title")
    if st.button("Search"):
        df_result_search = df[df['Title'].str.contains(title_search, case=False, na=False)]
        st.write("{} Results ".format(str(df_result_search.shape[0])))
        st.dataframe(df_result_search[["Title", "User Rating"]])  
    else:
        st.dataframe(df[["Title", "User Rating"]])  
        st.write('This data consists of {} rows and 2 columns'.format(df.shape[0]))

if selected == "Animation Data":
    st.header(':rainbow[DATA-DATA ANIMATION]')
    st.subheader('Top 5 Animation')
    st.write('Top 5 animation according to User Rating')

    top_10_anime: pd.DataFrame = df[['Title', 'User Rating']].sort_values(by=['User Rating'], ascending=False).head(10)
    top_10_anime['User Rating'] = top_10_anime['User Rating'].astype(float)

    top_10_anime_chart = (
    alt.Chart(top_10_anime).mark_bar().encode(
        x = alt.X('Title', sort='-y'),
        y = alt.Y('User Rating')
    )
    )

    st.altair_chart(top_10_anime_chart, use_container_width=True)

    st.divider()

    st.subheader('Top 10 Genres')
    st.write('Top 10 genres with most animation')

    top_10_genres: pd.DataFrame = df['Genre'].apply(lambda x: x.replace(' ,', ',').replace(', ', ',').split(','))

    Genres: list = []
    for i in top_10_genres: Genres += i
    Genres: pd.DataFrame = pd.DataFrame(Genres, columns=['Genres']).value_counts().head(10).reset_index()
    Genres.columns = ['Genre', 'Count']

    genre_chart = (
    alt.Chart(Genres).mark_bar().encode(
        x = alt.X('Count'),
        y = alt.Y('Genre', sort='-x')
    )
    )

    st.altair_chart(genre_chart, use_container_width=True)

    st.divider()

    st.subheader('Certificate Spread')
    st.write('The spread of give certificates')

    certificate_spread: pd.DataFrame = df['Certificate'].value_counts().reset_index()
    certificate_spread.columns = ['Certificate', 'Count']

    certificate_spread_chart = (
    alt.Chart(certificate_spread).mark_bar().encode(
        x = alt.X('Certificate', sort='-y'),
        y = alt.Y('Count')
    )
    )

    st.altair_chart(certificate_spread_chart, use_container_width=False)

    st.divider()

    st.subheader('Biggest Gross Income')
    st.write('Anime with the biggest gross income')

    gross_income: pd.DataFrame = df[['Title', 'Gross']].dropna()
    gross_income['Gross'] = gross_income['Gross'].astype(int)
    gross_income = gross_income.sort_values(by=['Gross'], ascending=False).head(10)

    gross_income_chart = (
    alt.Chart(gross_income).mark_bar().encode(
        x = alt.X('Gross'),
        y = alt.Y('Title', sort='-x')
    )
    )

    st.altair_chart(gross_income_chart, use_container_width=True)

    st.divider()

    st.subheader('Most Present Actors/Actressess')
    st.write('Actors/Actressess with most appearance in shows')

    top_10_actors: pd.DataFrame = df['Stars'].dropna().apply(lambda x: x.split(','))

    Actors:list = []
    for i in top_10_actors: Actors += i
    Actors:pd.DataFrame = pd.DataFrame(Actors, columns=['Actors']).value_counts().head(10).reset_index()
    Actors.columns = ['Actor/Actress', 'Count']

    actors_chart = (
    alt.Chart(Actors).mark_bar().encode(
        x = alt.X('Count'),
        y = alt.Y('Actor/Actress', sort='-x')
    )
    )

    st.altair_chart(actors_chart, use_container_width=True)

    st.divider()

    st.subheader('Longest Shows')
    st.write('Shows with the longest runtime')

    show_runtime:pd.DataFrame = df[['Title', 'Runtime']].dropna()
    show_runtime['Runtime'] = show_runtime['Runtime'].apply(lambda x: x.split(' ')[0].replace(',', '')).astype(float)
    show_runtime = show_runtime.sort_values(by=['Runtime'], ascending=False).head(10)
    show_runtime.columns = ['Title', 'Runtime(minutes)']

    show_runtime_chart = (
    alt.Chart(show_runtime).mark_bar().encode(
        x = alt.X('Runtime(minutes)'),
        y = alt.Y('Title', sort='-x')
    )
    )

    st.altair_chart(show_runtime_chart, use_container_width=True)

    st.divider()

    st.subheader('Runtime Rating Correlation')
    st.write('Correlation between runtime and rating')

    runtime_rating:pd.DataFrame = df[['Runtime', 'User Rating']].dropna()
    runtime_rating['Runtime'] = runtime_rating['Runtime'].apply(lambda x: x.split(' ')[0].replace(',', '')).astype(float)
    q_high = runtime_rating['Runtime'].quantile(0.95)
    q_low = runtime_rating['Runtime'].quantile(0.05)
    runtime_rating = runtime_rating[(runtime_rating['Runtime'] < q_high) & (runtime_rating['Runtime'] > q_low)]
    runtime_rating['User Rating'] = runtime_rating['User Rating'].astype(float)
    runtime_rating.columns = ['Runtime(minutes)', 'User Rating']

    runtime_rating_chart = (
    alt.Chart(runtime_rating).mark_point().encode(
        x = 'Runtime(minutes)',
        y = 'User Rating'
    )
    )

    st.altair_chart(runtime_rating_chart, use_container_width=True)

    full_data_runtime_rating = st.checkbox('See full data', key=1)
    runtime_rating_group_avg:pd.DataFrame
    runtime_rating_group_avg_chart:alt.Chart
    if full_data_runtime_rating: 
        runtime_rating_group_avg = runtime_rating.groupby(by=['Runtime(minutes)']).mean().reset_index().sort_values(by=['Runtime(minutes)'])
        runtime_rating_group_avg_chart = (
            alt.Chart(runtime_rating_group_avg).mark_bar().encode(
                y = alt.Y('User Rating').title('User Rating (Avg)'),
                x = alt.X('Runtime(minutes):N')
            )
        )
    else:
        runtime_rating_group_avg = runtime_rating.groupby(by=['Runtime(minutes)']).mean().reset_index().sort_values(by=['Runtime(minutes)']).head(10)
        runtime_rating_group_avg_chart = (
            alt.Chart(runtime_rating_group_avg).mark_bar().encode(
                x = alt.X('User Rating').title('User Rating (Avg)'),
                y = alt.Y('Runtime(minutes):N')
            )
        )
        
    st.altair_chart(runtime_rating_group_avg_chart, use_container_width=True)

    st.divider()

    st.subheader('Rating Gross Correlation')
    st.write('Correlation between rating and gross')

    rating_gross:pd.DataFrame = df[['User Rating', 'Gross']].dropna()
    rating_gross['Gross'] = rating_gross['Gross'].astype(int)
    rating_gross['User Rating'] = rating_gross['User Rating'].astype(float)
    q_high = rating_gross['Gross'].quantile(0.95)
    q_low = rating_gross['Gross'].quantile(0.05)
    rating_gross = rating_gross[(rating_gross['Gross'] < q_high) & (rating_gross['Gross'] > q_low)]

    rating_gross_chart = (
    alt.Chart(rating_gross).mark_point().encode(
        x = 'Gross',
        y = 'User Rating'
    )
    )

    st.altair_chart(rating_gross_chart, use_container_width=True)

    full_data_rating_gross = st.checkbox('See full data', key=2)
    rating_gross_group_avg:pd.DataFrame
    rating_gross_group_avg_chart:alt.Chart
    if full_data_rating_gross:
        rating_gross_group_avg = rating_gross.groupby(by=['User Rating']).mean().reset_index().sort_values(by=['User Rating'])
        rating_gross_group_avg_chart = (
            alt.Chart(rating_gross_group_avg).mark_bar().encode(
                x = alt.X('User Rating:N'),
                y = alt.Y('Gross').title('Gross (Avg)')
            )
        )
    else:
        rating_gross_group_avg = rating_gross.groupby(by=['User Rating']).mean().reset_index().sort_values(by=['User Rating']).head(10)
        rating_gross_group_avg_chart = (
            alt.Chart(rating_gross_group_avg).mark_bar().encode(
                y = alt.Y('User Rating:N'),
                x = alt.X('Gross').title('Gross (Avg)')
            )
        )

    st.altair_chart(rating_gross_group_avg_chart, use_container_width=True)

if selected == "Animation Filter":
    st.header(':rainbow[Animation Filter]')
    st.subheader('Search Your Genre Animation')
    #navbar filter
    st.sidebar.header("Animation Filter: ")
    Genre = st.sidebar.multiselect(
        "Select the genre: ",
        options=df["Genre"].unique()
    )

    df_selection = df.query(
        "Genre == @Genre"
    )
    st.dataframe(df_selection)

if selected == "Average Rating Animation":
    st.header(':rainbow[ANIMATION RATING]')
    st.subheader('Search Your Animation Rating In Here')
    def average_rating(title):
        filtered_df = df[df['Title'].str.contains(title, case=False, na=False)]
        
        if not filtered_df.empty:
            try:
                filtered_df['User Rating'] = pd.to_numeric(filtered_df['User Rating'], errors='coerce')
                filtered_df = filtered_df.dropna(subset=['User Rating'])

                average_rating = filtered_df['User Rating'].mean()
                return average_rating
            except Exception as e:
                return str(e)
        else:
            return "No matching data found"

    title_search = st.text_input("Animation Title")
    if st.button("search"):
        predicted_rating = average_rating(title_search)
        if isinstance(predicted_rating, float):
            df_result_search = df[df['Title'].str.contains(title_search,case=False, na=False)]
            st.dataframe(df_result_search)
            st.write(f"Average Rating for '{title_search}': {predicted_rating:.2f}")
        else:
            st.write(predicted_rating)
