# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 17:14:06 2024

@author: StammyG
"""

import streamlit as st
import pandas as pd

st.title('StammyApp')

db_csv = "Top_Leagues.csv"

@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path, delimiter=";")

data = load_data(db_csv)
data['Season'] = data['Season'].astype(str)

tab1, tab2 = st.tabs(["Team Stats", "Different Filters"])

with tab1:
    st.header('Filter Options')

    competitions = st.multiselect(
        'Select Competitions', options=data['Competition'].unique(), default=[], key='competition'
    )
    competition_filtered_data = data[data['Competition'].isin(competitions)]

    # Sidebar - Season selection
    seasons = competition_filtered_data['Season'].unique()
    season = st.selectbox('Select Season', options=seasons, key='season')
    Season_Filtered_data = competition_filtered_data[competition_filtered_data['Season'] == season]

    home_team = st.selectbox('Select Home Team', options=Season_Filtered_data['Team'].unique())
    filtered_data = Season_Filtered_data[Season_Filtered_data['Team'].isin([home_team])]
    opponents = st.multiselect(
        'Select Opponents', options=filtered_data['Opponent'].unique(), default=filtered_data['Opponent'].unique()
    )
    filtered_data = filtered_data[filtered_data['Opponent'].isin(opponents)]

    venues = filtered_data['Venue'].unique()
    venue = st.multiselect('Select Venue for Home Team', options=venues, key='venue')
    venue_home_filtered_data = filtered_data[filtered_data['Venue'].isin(venue)]

    away_team = st.selectbox('Select Away Team', options=Season_Filtered_data['Team'].unique())
    away_filtered_data = Season_Filtered_data[Season_Filtered_data['Team'].isin([away_team])]
    away_opponents = st.multiselect(
        'Select Opponents', options=away_filtered_data['Opponent'].unique(), default=away_filtered_data['Opponent'].unique(),
        key='away_team'
    )
    away_filtered_data = away_filtered_data[away_filtered_data['Opponent'].isin(away_opponents)]

    venues = away_filtered_data['Venue'].unique()
    venue = st.multiselect('Select Venue for Away Team', options=venues)
    venue_away_filtered_data = away_filtered_data[away_filtered_data['Venue'].isin(venue)]

    st.markdown(
    "<h2 style='color: red;'>Team Stats for selected Teams</h2>",
    unsafe_allow_html=True
    for_filtered_data = venue_home_filtered_data[venue_home_filtered_data["ForAgainst"] == "For"]
    against_filtered_data = venue_home_filtered_data[venue_home_filtered_data["ForAgainst"] == "Against"]
    for_away_filtered_data = venue_away_filtered_data[venue_away_filtered_data["ForAgainst"] == "For"]
    against_away_filtered_data = venue_away_filtered_data[venue_away_filtered_data["ForAgainst"] == "Against"]

    def write_mean_stat_to_columns(stat, column, selected_data):
        stat_mean = selected_data[stat].mean()
        column.write(f"{stat_mean:.1f}")

    def write_stat_to_container(columns_, title, csv_stat, is_against):
        home_data = for_filtered_data if not is_against else against_filtered_data
        away_data = for_away_filtered_data if not is_against else against_away_filtered_data
        col1_, col2_, col3_ = columns_
        write_mean_stat_to_columns(csv_stat, col1_, home_data)
        col2_.write(title)
        write_mean_stat_to_columns(csv_stat, col3_, away_data)

    st.markdown(
    "<h2 style='color: red;'>Stats for selected teams</h2>",
    unsafe_allow_html=True

    header_columns = st.columns(3)
    header_columns[0].write(home_team)
    header_columns[1].write("vs")
    header_columns[2].write(away_team)

    for_stats = st.container()
    with for_stats:
        columns = st.columns(3)
        write_stat_to_container(columns, "Shots on Target", "SoT", False)
        write_stat_to_container(columns, "Shots", "Shots", False)
        write_stat_to_container(columns, "Tackles", "Tackles", False)
        write_stat_to_container(columns, "Goal Kicks", "Goal_Kicks", False)
        write_stat_to_container(columns, "Fouls Commited", "Fouls_Commited", False)
        write_stat_to_container(columns, "Offsides", "Offsides", False)
        write_stat_to_container(columns, "Yellow Cards", "Yellow_Cards", False)
        write_stat_to_container(columns, "xG", "xG", False)

    st.markdown(
    "<h2 style='color: red;'>Stats against selected teams</h2>",
    unsafe_allow_html=True
)
    against_header_columns = st.columns(3)
    against_header_columns[0].write(home_team)
    against_header_columns[1].write("vs")
    against_header_columns[2].write(away_team)
    against_stats = st.container()
    with against_stats:
        against_columns = st.columns(3)
        write_stat_to_container(against_columns, "Shots on Target", "SoT", True)
        write_stat_to_container(against_columns, "Shots", "Shots", True)
        write_stat_to_container(against_columns, "Tackles", "Tackles", True)
        write_stat_to_container(against_columns, "Goal Kicks", "Goal_Kicks", True)
        write_stat_to_container(against_columns, "Fouls Commited", "Fouls_Commited", True)
        write_stat_to_container(against_columns, "Offsides", "Offsides", True)
        write_stat_to_container(against_columns, "Yellow Cards", "Yellow_Cards", True)
        write_stat_to_container(against_columns, "xG", "xG", True)

    tab1_1, tab1_2 = st.tabs(["Home Data", "Away Data"])

    with tab1_1:
        st.write("Home Data")
        st.dataframe(venue_home_filtered_data)

    with tab1_2:
        st.write("Away Data")
        st.dataframe(venue_away_filtered_data)

if tab2:
    st.sidebar.header('Filter Options')
    
    

   
