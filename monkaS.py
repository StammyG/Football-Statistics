# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 17:14:06 2024

@author: StammyG
"""
import streamlit as st
import pandas as pd
from PIL import Image


st.title('StammyApp')

db_csv = "Top5_League_Stats_Updated4.csv"

@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

data = load_data(db_csv)
YellowCards_Data = pd.read_csv("SusLeagues_Cards_2024_2.csv")
SuperLeague_Data = pd.read_csv('SuperLeague_Stats_Updated_Gameweek_final.csv')
data['Season'] = data['Season'].astype(str)
YellowCards_Data['Season'] = YellowCards_Data['Season'].astype(str)
SuperLeague_Data['Season'] = SuperLeague_Data['Season'].astype(str)

player_stats = pd.read_csv('Top5Leagues_player_stats_updated.csv')
player_stats['Team'] = player_stats['Team'].fillna('Random')
new_order = ['Match','round','minutes','SoT','Shots','Tackles','fouls_commited','fouls_received','Goals','Assists','Team','Competition','Name','Sofascore_Name','player_id','Season']
player_stats = player_stats[new_order]


#tabs

TabA,TabB = st.tabs(["Team Stats","Player Stats"])
with TabA:
    st.write("")
    st.write("")

    
    tab1, tab2, tab3 = st.tabs(["Team Stats for Top 5 and Latin America", "Yellow Cards for Leagues outside the Top 5","GREEK SUPERLEAGUE STATS"])
    
    with tab1:
        st.header('Filter Options')
    
        competitions = st.multiselect(
            'Select Competitions', options=data['Competition'].unique(), default=[]
        )
        competition_filtered_data = data[data['Competition'].isin(competitions)]
    
        seasons = competition_filtered_data['Season'].unique()
        season = st.selectbox('Select Season', options=seasons)
        season_filtered_data = competition_filtered_data[competition_filtered_data['Season'] == season]
    
        home_team = st.selectbox('Select Home Team', options=season_filtered_data['Team'].unique())
        filtered_data = season_filtered_data[season_filtered_data['Team'] == home_team]
        opponents = st.multiselect(
            'Select Opponents', options=filtered_data['Opponent'].unique(), default=filtered_data['Opponent'].unique()
        )
        filtered_data = filtered_data[filtered_data['Opponent'].isin(opponents)]
    
        venues = filtered_data['Venue'].unique()
        venue = st.multiselect('Select Venue for Home Team', options=venues)
        venue_filtered_data = filtered_data[filtered_data['Venue'].isin(venue)]
    
        away_team = st.selectbox('Select Away Team', options=season_filtered_data['Team'].unique())
        away_filtered_data = season_filtered_data[season_filtered_data['Team'] == away_team]
        away_opponents = st.multiselect('Select Opponents', options=away_filtered_data['Opponent'].unique(), default=away_filtered_data['Opponent'].unique(), key='away_opponents'
        )
        away_filtered_data = away_filtered_data[away_filtered_data['Opponent'].isin(away_opponents)]
        
        venues = away_filtered_data['Venue'].unique()
        venue_away = st.multiselect('Select Venue for Away Team', options=venues)
        venue_away_filtered_data = away_filtered_data[away_filtered_data['Venue'].isin(venue_away)]
        against_venue_filtered_data = filtered_data[~filtered_data['Venue'].isin(venue)]
        against_venue_away_filtered_data = away_filtered_data[~away_filtered_data['Venue'].isin(venue_away)]
    
     
        for_filtered_data = venue_filtered_data[venue_filtered_data["ForAgainst"] == "For"]
        against_filtered_data = venue_filtered_data[venue_filtered_data["ForAgainst"] == "Against"]
        for_away_filtered_data = venue_away_filtered_data[against_venue_filtered_data["ForAgainst"] == "For"]
        against_away_filtered_data = against_venue_away_filtered_data[against_venue_away_filtered_data["ForAgainst"] == "Against"]
        
        
        
        
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
        def write_std_stat_to_columns(stat, column, selected_data):
            stat_std = selected_data[stat].std()
            column.write(f"{stat_std:.2f}")
    
        def write_std_stat_to_container(columns_, title, csv_stat, is_against):
            home_data = for_filtered_data if not is_against else against_filtered_data
            away_data = for_away_filtered_data if not is_against else against_away_filtered_data
            col1_, col2_, col3_ = columns_
            write_std_stat_to_columns(csv_stat, col1_, home_data)
            col2_.write(title)
            write_std_stat_to_columns(csv_stat, col3_, away_data)
            
    
        Average_YellowCards1 = season_filtered_data.groupby('ForAgainst')['Yellow_Cards'].mean().reset_index()
        Average_YellowCards = Average_YellowCards1['Yellow_Cards'].sum()
    
    
    
    
        
    
        st.markdown('**Stats for selected teams**')
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
        
        st.write("") 
        
    
        st.markdown('**Stats against selected Teams**')
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
    
        st.write("") 
        st.markdown("**League Stats for Cards:**") 
            
    
    
        st.markdown(("**League Average Yellow Cards per Match: "  f"{Average_YellowCards:.1f}**"))
    
        
        
       
        tab1_1, tab1_2, tab1_3 = st.tabs(["Home Data", "Away Data","Standard Deviation"])
    
        with tab1_1:
            st.write("Home Data")
            st.dataframe(for_filtered_data)
    
        with tab1_2:
            st.write("Away Data")
            st.dataframe(against_away_filtered_data )
    
        with tab1_3:
            st.markdown('**Stats for selected teams**')
            header_columns = st.columns(3)
            header_columns[0].write(home_team)
            header_columns[1].write("vs")
            header_columns[2].write(away_team)
    
            for_stats = st.container()
            with for_stats:
                columns = st.columns(3)
                write_std_stat_to_container(columns, "Shots on Target", "SoT", False)
                write_std_stat_to_container(columns, "Shots", "Shots", False)
                write_std_stat_to_container(columns, "Tackles", "Tackles", False)
                write_std_stat_to_container(columns, "Goal Kicks", "Goal_Kicks", False)
                write_std_stat_to_container(columns, "Fouls Commited", "Fouls_Commited", False)
                write_std_stat_to_container(columns, "Offsides", "Offsides", False)
                write_std_stat_to_container(columns, "Yellow Cards", "Yellow_Cards", False)
                write_std_stat_to_container(columns, "xG", "xG", False)
            
            st.write("") 
            
    
            st.markdown('**Stats against selected Teams**')
            against_header_columns = st.columns(3)
            against_header_columns[0].write(home_team)
            against_header_columns[1].write("vs")
            against_header_columns[2].write(away_team)
            against_stats = st.container()
            with against_stats:
                against_columns = st.columns(3)
                write_std_stat_to_container(against_columns, "Shots on Target", "SoT", True)
                write_std_stat_to_container(against_columns, "Shots", "Shots", True)
                write_std_stat_to_container(against_columns, "Tackles", "Tackles", True)
                write_std_stat_to_container(against_columns, "Goal Kicks", "Goal_Kicks", True)
                write_std_stat_to_container(against_columns, "Fouls Commited", "Fouls_Commited", True)
                write_std_stat_to_container(against_columns, "Offsides", "Offsides", True)
                write_std_stat_to_container(against_columns, "Yellow Cards", "Yellow_Cards", True)
                write_std_stat_to_container(against_columns, "xG", "xG", True)
    
    with tab2:
        st.header('Filter Options')
        competitions = st.multiselect(
            'Select Competitions', options=YellowCards_Data['Competition'].unique(), default=[]
        )
        competition_filtered_YellowCards_Data = YellowCards_Data[YellowCards_Data['Competition'].isin(competitions)]
    
        seasons = competition_filtered_YellowCards_Data['Season'].unique()
        season = st.selectbox('Select Season', options=seasons,key = "Season_Cards")
        season_filtered_YellowCards_Data = competition_filtered_YellowCards_Data[competition_filtered_YellowCards_Data['Season'] == season]
    
        home_team = st.selectbox('Select Home Team', options=season_filtered_YellowCards_Data['Team'].unique(),key="Home_Team_Cards")
        filtered_YellowCards_Data = season_filtered_YellowCards_Data[season_filtered_YellowCards_Data['Team'] == home_team]
        opponents = st.multiselect(
            'Select Opponents', options=filtered_YellowCards_Data['Opponent'].unique(), default=filtered_YellowCards_Data['Opponent'].unique(), key = "Home_Opponent_Cards"
        )
        filtered_YellowCards_Data = filtered_YellowCards_Data[filtered_YellowCards_Data['Opponent'].isin(opponents)]
    
        venues = filtered_YellowCards_Data['Venue'].unique()
        venue = st.multiselect('Select Venue for Home Team', options=venues, key="Home_Venue_Cards")
        venue_filtered_YellowCards_Data = filtered_YellowCards_Data[filtered_YellowCards_Data['Venue'].isin(venue)]
    
        away_team = st.selectbox('Select Away Team', options=season_filtered_YellowCards_Data['Team'].unique(),key="Away_Team_Cards")
        away_filtered_YellowCards_Data = season_filtered_YellowCards_Data[season_filtered_YellowCards_Data['Team'] == away_team]
        away_opponents = st.multiselect('Select Opponents', options=away_filtered_YellowCards_Data['Opponent'].unique(), default=away_filtered_YellowCards_Data['Opponent'].unique(), key='away_opponents_cards'
        )
        away_filtered_YellowCards_Data = away_filtered_YellowCards_Data[away_filtered_YellowCards_Data['Opponent'].isin(away_opponents)]
    
        venues = away_filtered_YellowCards_Data['Venue'].unique()
        venue_away = st.multiselect('Select Venue for Away Team', options=venues,key="Away_Venue_Cards")
        venue_away_filtered_YellowCards_Data = away_filtered_YellowCards_Data[away_filtered_YellowCards_Data['Venue'].isin(venue_away)]
    
     
        for_filtered_YellowCards_Data = venue_filtered_YellowCards_Data[venue_filtered_YellowCards_Data["ForAgainst"] == "For"]
        against_filtered_YellowCards_Data = venue_filtered_YellowCards_Data[venue_filtered_YellowCards_Data["ForAgainst"] == "Against"]
        for_away_filtered_YellowCards_Data = venue_away_filtered_YellowCards_Data[venue_away_filtered_YellowCards_Data["ForAgainst"] == "For"]
        against_away_filtered_YellowCards_Data = venue_away_filtered_YellowCards_Data[venue_away_filtered_YellowCards_Data["ForAgainst"] == "Against"]
    
    
    
        League_Average_YellowCards1 = season_filtered_YellowCards_Data.groupby('ForAgainst')['Yellow_Cards'].mean().reset_index()
        League_Average_YellowCards = League_Average_YellowCards1['Yellow_Cards'].sum()
    
        League_Average_RedCards1 = season_filtered_YellowCards_Data.groupby('ForAgainst')['Red_Cards'].mean().reset_index()
        League_Average_RedCards = League_Average_RedCards1['Red_Cards'].sum()
    
    
        
        
        def write_mean_stat_to_columns_2(stat, column, selected_data):
            stat_mean = selected_data[stat].mean()
            column.write(f"{stat_mean:.1f}")
    
        def write_stat_to_container_2(columns_, title, csv_stat, is_against):
            home_data = for_filtered_YellowCards_Data if not is_against else against_filtered_YellowCards_Data
            away_data = for_away_filtered_YellowCards_Data if not is_against else against_away_filtered_YellowCards_Data
            col1_, col2_, col3_ = columns_
            write_mean_stat_to_columns_2(csv_stat, col1_, home_data)
            col2_.write(title)
            write_mean_stat_to_columns_2(csv_stat, col3_, away_data)
        
        def write_std_stat_to_columns_2(stat, column, selected_data):
            stat_std = selected_data[stat].std()
            column.write(f"{stat_std:.2f}")
        
        def write_std_stat_to_container_2(columns_, title, csv_stat, is_against):
            home_data = for_filtered_YellowCards_Data if not is_against else against_filtered_YellowCards_Data
            away_data = for_away_filtered_YellowCards_Data if not is_against else against_away_filtered_YellowCards_Data
            col1_, col2_, col3_ = columns_
            write_std_stat_to_columns_2(csv_stat, col1_, home_data)
            col2_.write(title)
            write_std_stat_to_columns_2(csv_stat, col3_, away_data)
    
            
    
    
        
    
        st.subheader('Stats of selected teams against selected opponents')
        header_columns = st.columns(3)
        header_columns[0].write(home_team)
        header_columns[1].write("vs")
        header_columns[2].write(away_team)
        for_stats = st.container()
        with for_stats:
            columns = st.columns(3)
            write_stat_to_container_2(columns, "Yellow Cards", "Yellow_Cards", False)
            write_stat_to_container_2(columns, "Red Cards", "Red_Cards", False)
            
        st.write("") 
    
        st.subheader('Stats of selected opponents against selected teams')
        against_header_columns = st.columns(3)
        against_header_columns[0].write(home_team)
        against_header_columns[1].write("vs")
        against_header_columns[2].write(away_team)
        against_stats = st.container()
        with against_stats:
            against_columns = st.columns(3)
            write_stat_to_container_2(against_columns, "Yellow Cards", "Yellow_Cards", True)
            write_stat_to_container_2(against_columns, "Red Cards", "Red_Cards", True)
    
        st.write("") 
        st.write("") 
        st.write("") 
    
    
        st.markdown(("**League Average Yellow Cards per Match: "  f"{League_Average_YellowCards:.1f}**"))
    
        st.markdown(("**League Average Red Cards per Match: " f"{League_Average_RedCards:.2f}**")) 
        st.write("") 
        st.write("") 
    
        
        
        
        
        
        tab2_1, tab2_2, tab3_2 = st.tabs(["Home Data", "Away Data","Standard Deviation"])
        
        with tab2_1:
            st.write("Home Data")
            st.dataframe(venue_filtered_YellowCards_Data)
    
        with tab2_2:
            st.write("Away Data")
            st.dataframe(venue_away_filtered_YellowCards_Data)
        with tab3_2:
            st.subheader('Stats of selected teams against selected opponents')
            header_columns = st.columns(3)
            header_columns[0].write(home_team)
            header_columns[1].write("vs")
            header_columns[2].write(away_team)
            std_for_stats = st.container()
            with std_for_stats:
                columns = st.columns(3)
                write_std_stat_to_container_2(columns, "Yellow Cards", "Yellow_Cards", False)
                write_std_stat_to_container_2(columns, "Red Cards", "Red_Cards", False)
                
            st.write("") 
    
            st.subheader('Stats of selected opponents against selected teams')
            against_header_columns = st.columns(3)
            against_header_columns[0].write(home_team)
            against_header_columns[1].write("vs")
            against_header_columns[2].write(away_team)
            std_against_stats = st.container()
            with std_against_stats:
                against_columns = st.columns(3)
                write_std_stat_to_container_2(against_columns, "Yellow Cards", "Yellow_Cards", True)
                write_std_stat_to_container_2(against_columns, "Red Cards", "Red_Cards", True)
    
        with tab3:
            # Create three columns with the middle one for the image
            colIM1, colIM2, colIM3 = st.columns([1, 2, 1])
    
            # Center the image by displaying it in the middle column
            with colIM2:
                st.image("super_league_logo.jpg")
    
            
            st.header('Filter Options')
            seasons = SuperLeague_Data['Season'].unique()
            season = st.selectbox('Select Season', options=seasons,key= "superleague_season")
            Superleague_season_filtered_data = SuperLeague_Data[SuperLeague_Data['Season'] == season]
            
            home_team = st.selectbox('Select Home Team', options=Superleague_season_filtered_data['Team'].unique(),key ="superLeague_home")
            Superleague_filtered_data = Superleague_season_filtered_data[Superleague_season_filtered_data['Team'] == home_team]
            opponents = st.multiselect(
                'Select Opponents', options=Superleague_filtered_data['Opponent'].unique(), default=Superleague_filtered_data['Opponent'].unique(),key="superleague_home_opponents"
            )
            Superleague_filtered_data = Superleague_filtered_data[Superleague_filtered_data['Opponent'].isin(opponents)]
            venues = Superleague_filtered_data['Venue'].unique()
            venue = st.multiselect('Select Venue for Home Team', options=venues,key="superleague_home_venue")
            Superleague_venue_filtered_data = Superleague_filtered_data[Superleague_filtered_data['Venue'].isin(venue)]
            
            away_team = st.selectbox('Select Away Team', options=Superleague_season_filtered_data['Team'].unique())
            superleague_away_filtered_data = Superleague_season_filtered_data[Superleague_season_filtered_data['Team'] == away_team]
            away_opponents = st.multiselect('Select Opponents', options=superleague_away_filtered_data['Opponent'].unique(), default=superleague_away_filtered_data['Opponent'].unique(), key='superleague_away_opponents'
            )
            superleague_away_filtered_data = superleague_away_filtered_data[superleague_away_filtered_data['Opponent'].isin(away_opponents)]
    
            venues = superleague_away_filtered_data['Venue'].unique()
            venue_away = st.multiselect('Select Venue for Away Team', options=venues,key="superleague_away_venues")
            superleague_venue_away_filtered_data = superleague_away_filtered_data[superleague_away_filtered_data['Venue'].isin(venue_away)]
            
            superleague_for_filtered_data = Superleague_venue_filtered_data[Superleague_venue_filtered_data["ForAgainst"] == "For"]
            superleague_against_filtered_data = Superleague_venue_filtered_data[Superleague_venue_filtered_data["ForAgainst"] == "Against"]
            superleague_for_away_filtered_data = superleague_venue_away_filtered_data[superleague_venue_away_filtered_data["ForAgainst"] == "For"]
            superleague_against_away_filtered_data = superleague_venue_away_filtered_data[superleague_venue_away_filtered_data["ForAgainst"] == "Against"]
    
            superleague_Average_YellowCards1 = Superleague_season_filtered_data.groupby('ForAgainst')['Yellow_Cards'].mean().reset_index()
            superleague_Average_YellowCards = superleague_Average_YellowCards1['Yellow_Cards'].sum()
    
            superleague_Average_RedCards1 = Superleague_season_filtered_data.groupby('ForAgainst')['Red_Cards'].mean().reset_index()
            superleague_Average_RedCards = superleague_Average_RedCards1['Red_Cards'].sum()
    
            def write_mean_stat_to_columns_3(stat, column, selected_data):
                stat_mean = selected_data[stat].mean()
                column.write(f"{stat_mean:.1f}")
    
            def write_stat_to_container_3(columns_, title, csv_stat, is_against):
                home_data = superleague_for_filtered_data if not is_against else superleague_against_filtered_data
                away_data = superleague_for_away_filtered_data if not is_against else superleague_against_away_filtered_data
                col1_, col2_, col3_ = columns_
                write_mean_stat_to_columns_3(csv_stat, col1_, home_data)
                col2_.write(title)
                write_mean_stat_to_columns_3(csv_stat, col3_, away_data)
    
            st.markdown('**Stats of selected Teams against selected Opponents**')
            header_columns = st.columns(3)
            header_columns[0].write(home_team)
            header_columns[1].write("vs")
            header_columns[2].write(away_team)
            
    
            for_stats = st.container()
            with for_stats:
                columns = st.columns(3)
                write_stat_to_container_3(columns, "Shots", "Shots", False)
                write_stat_to_container_3(columns, "Shots on Target", "SoT", False)
                write_stat_to_container_3(columns, "Throw Ins", "Throw_Ins", False)
                write_stat_to_container_3(columns, "Goal Kicks", "Goal_Kicks", False)
                write_stat_to_container_3(columns, "Fouls Commited", "Fouls_Commited", False)
                write_stat_to_container_3(columns, "Offsides", "Offsides", False)
                write_stat_to_container_3(columns, "Tackles", "Tackles", False)
                write_stat_to_container_3(columns, "Yellow Cards", "Yellow_Cards", False)
                write_stat_to_container_3(columns, "Red Cards", "Red_Cards", False)
                write_stat_to_container_3(columns, "Corner Kicks", "Corner_Kicks", False)
        
            st.write("") 
        
    
            st.markdown('**Stats of selected Opponents against selected Teams**')
            st.write("")
            against_header_columns = st.columns(3)
            against_header_columns[0].write(home_team)
            against_header_columns[1].write("vs")
            against_header_columns[2].write(away_team)
            against_stats = st.container()
            with against_stats:
                against_columns = st.columns(3)
                write_stat_to_container_3(against_columns, "Shots", "Shots", True)
                write_stat_to_container_3(against_columns, "Shots on Target", "SoT", True)
                write_stat_to_container_3(against_columns, "Throw Ins", "Throw_Ins", True)
                write_stat_to_container_3(against_columns, "Goal Kicks", "Goal_Kicks", True)
                write_stat_to_container_3(against_columns, "Fouls Commited", "Fouls_Commited", True)
                write_stat_to_container_3(against_columns, "Offsides", "Offsides", True)
                write_stat_to_container_3(against_columns, "Tackles", "Tackles", True)
                write_stat_to_container_3(against_columns, "Yellow Cards", "Yellow_Cards", True)
                write_stat_to_container_3(against_columns, "Red Cards", "Red_Cards", True)
                write_stat_to_container_3(against_columns, "Corner Kicks", "Corner_Kicks", True)
    
            st.write("") 
            st.markdown("**League Stats for Cards:**") 
            
    
    
            st.markdown(("**League Average Yellow Cards per Match: "  f"{superleague_Average_YellowCards:.1f}**"))
    
            st.markdown(("**League Average Red Cards per Match: " f"{superleague_Average_RedCards:.2f}**"))
            st.write("")
                
    
            tab3_1, tab3_2 = st.tabs(["Home Data", "Away Data"])
        
            with tab3_1:
                st.write("Home Data")
                st.dataframe(Superleague_venue_filtered_data)
    
            with tab3_2:
                st.write("Away Data")
                st.dataframe(superleague_venue_away_filtered_data)
    
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("Disclaimer: All stats that are used in tabs: Team stats for Top 5 and Yellow Cards outside the top 5 Leagues are provided by FBref and the rest are provided by Sofascore")

with TabB:
    st.title("Player Stats")
    players_team = player_stats['Team'].unique()
    
    colB1, colB2 = st.columns([1, 1])  # Adjust these values to control the width ratio
    
    with colB1:
        player_competition = st.selectbox('Select Competition',options =[comp for comp in player_stats['Competition'].unique() if pd.notna(comp)],key="team_competition")
        team_competition = player_stats[player_stats['Competition']== player_competition]
        season = st.multiselect('Select Season for player Stats', options=team_competition['Season'].unique(),key='player_season')
        player_team = st.selectbox('Select Team',options=team_competition['Team'].unique(), key= "team_roster" )
        

        
    team_roster = player_stats[(player_stats['Team'] == player_team) & (player_stats['Season'].isin(season))]
    filtered_team_roster = team_roster[team_roster['minutes']>10]
    player_id_counts = filtered_team_roster['player_id'].value_counts()
    filtered_team_roster['Importance'] = (90*filtered_team_roster.groupby('player_id')['SoT'].transform('mean'))+(4*filtered_team_roster['player_id'].map(player_id_counts)) + (0.25*filtered_team_roster.groupby('player_id')['minutes'].transform('mean'))
    unique_roster = filtered_team_roster.drop_duplicates(subset=['player_id'])
    unique_roster = unique_roster.sort_values(by='Importance', ascending=False)
    
    num_rows_slider = st.number_input('Last _ Matches:', 
                           min_value=1, 
                           max_value=150, 
                           value=150, 
                           step=1,key="slider")
    filtered_team_roster['chronological_order'] = filtered_team_roster['Season'] + (0.01*filtered_team_roster['round'])
    filtered_team_roster=filtered_team_roster.sort_values(by='chronological_order', ascending=False)
    supremacy = st.number_input('Supremacy:', 
                            
                           
                           
                           step=0.05,key="supremacy")
    totals = st.number_input('Totals:', 
                            
                           
                           step=0.05,key="Totals")
    def calculate_average_stats(player_id):
        player_data = filtered_team_roster[filtered_team_roster['player_id'] == player_id]
        player_data = player_data.head(num_rows_slider)
        avg_stats = player_data[['SoT', 'Shots', 'fouls_commited', 'fouls_received','Tackles','Goals','Assists',"minutes"]].mean()
        
        return avg_stats
    def calculate_suggested_totals_shots(player_id):
        avg_stats = calculate_average_stats(player_id)
        suggested_shots = avg_stats['Shots'] +((avg_stats['Shots']*supremacy)/totals)

        return suggested_shots
    
    # Streamlit app layout
    st.subheader(f'{player_team} Roster')
    
    # Create a layout with columns for player name and stats
   
            
    st.markdown("""
        <style>
        
        
        .player-stats {
            border: 2px solid #FF5733;
            border-radius: 5px;
            padding: 10px;
            margin-top: 5px;
            background-color: #FFFFFF;
        }
        
        </style>
    """, unsafe_allow_html=True)
  
    TabB5,TabB6 = st.tabs(["Player Average","Suggested Totals"])
    with TabB5:
        for _, player in unique_roster.iterrows():
            player_id = player['player_id']
            player_name = player['Sofascore_Name']
            
            
            # Create columns for player name and stats
            # Create columns for player name and stats
            
            avg_stats = calculate_average_stats(player_id)
            
            st.markdown(f"""
                    <div class='player-stats'>
                        <div style='font-size:14px; margin-top:0.5px;'>
                            <div style='display: flex; flex-wrap: wrap; gap: 8px;'>
                                <div style='font-size:17px;color:black;'><strong></strong> <span style='color:#000000; font-size:17px; font-weight:bold;'>{player_name}</span></div>
                                <div style='font-size:14px;color:black;'><strong>Minutes:</strong> <span style='color:#000000; font-size:17px; font-weight:bold;'>{avg_stats['minutes']:.2f}</span></div>
                                <div style='font-size:14px;color:black;'><strong>Shots on Target:</strong> <span style='color:#000000; font-size:17px; font-weight:bold;'>{avg_stats['SoT']:.2f}</span></div>
                                <div style='font-size:14px;color:black;'><strong>Shots:</strong> <span style='color:#000000; font-size:17px; font-weight:bold;'>{avg_stats['Shots']:.2f}</span></div>
                                <div style='font-size:14px;color:black;'><strong>Fouls Commited:</strong> <span style='color:#000000; font-size:17px; font-weight:bold;'>{avg_stats['fouls_commited']:.2f}</span></div>
                                <div style='font-size:14px;color:black;'><strong>Fouls Received:</strong> <span style='color:#000000; font-size:17px; font-weight:bold;'>{avg_stats['fouls_received']:.2f}</span></div>
                                <div style='font-size:14px;color:black;'><strong>Tackles:</strong> <span style='color:#000000; font-size:17px; font-weight:bold;'>{avg_stats['Tackles']:.2f}</span></div>
                                <div style='font-size:14px;color:black;'><strong>Goals:</strong> <span style='color:#000000; font-size:17px; font-weight:bold;'>{avg_stats['Goals']:.2f}</span></div>
                                <div style='font-size:14px;color:black;'><strong>Assists:</strong> <span style='color:#000000; font-size:17px; font-weight:bold;'>{avg_stats['Assists']:.2f}</span></div>
            
              
                            
                        
                         
                    """, unsafe_allow_html=True)
               
            with st.expander(f"Show all matches that {player_name} featured in"):
                 player_matches = filtered_team_roster[filtered_team_roster['player_id'] == player_id]
                 player_matches = filtered_team_roster[filtered_team_roster['player_id'] == player_id].head(num_rows_slider)   
                 st.write(player_matches)
    with TabB6:    
        for _, player in unique_roster.iterrows():
            player_id = player['player_id']
            player_name = player['Sofascore_Name']
                
                
                # Create columns for player name and stats
                # Create columns for player name and stats
                
            avg_stats = calculate_average_stats(player_id)
            suggested_shots = calculate_suggested_totals_shots(player_id)
            st.markdown(f"""
                        <div class='player-stats'>
                            <div style='font-size:14px; margin-top:0.5px;'>
                                <div style='display: flex; flex-wrap: wrap; gap: 8px;'>
                                    <div style='font-size:17px;color:black;'><strong></strong> <span style='color:#000000; font-size:17px; font-weight:bold;'>{player_name}</span></div>
                                    <div style='font-size:14px;color:black;'><strong>Minutes:</strong> <span style='color:#000000; font-size:17px; font-weight:bold;'>{avg_stats['minutes']:.2f}</span></div>
                                    <div style='font-size:14px;color:black;'><strong>Shots on Target:</strong> <span style='color:#000000; font-size:17px; font-weight:bold;'>{avg_stats['SoT']:.2f}</span></div>
                                    <div style='font-size:14px;color:black;'><strong>Shots:</strong> <span style='color:#000000; font-size:17px; font-weight:bold;'>{suggested_shots:.2f}</span></div>
                                    <div style='font-size:14px;color:black;'><strong>Fouls Commited:</strong> <span style='color:#000000; font-size:17px; font-weight:bold;'>{avg_stats['fouls_commited']:.2f}</span></div>
                                    <div style='font-size:14px;color:black;'><strong>Fouls Received:</strong> <span style='color:#000000; font-size:17px; font-weight:bold;'>{avg_stats['fouls_received']:.2f}</span></div>
                                    <div style='font-size:14px;color:black;'><strong>Tackles:</strong> <span style='color:#000000; font-size:17px; font-weight:bold;'>{avg_stats['Tackles']:.2f}</span></div>
                                    <div style='font-size:14px;color:black;'><strong>Goals:</strong> <span style='color:#000000; font-size:17px; font-weight:bold;'>{avg_stats['Goals']:.2f}</span></div>
                                    <div style='font-size:14px;color:black;'><strong>Assists:</strong> <span style='color:#000000; font-size:17px; font-weight:bold;'>{avg_stats['Assists']:.2f}</span></div>
                
                  
                                
                            
                            
                    """, unsafe_allow_html=True)
                   
            with st.expander(f"Show all matches that {player_name} featured in"):
                    player_matches = filtered_team_roster[filtered_team_roster['player_id'] == player_id]
                    player_matches = filtered_team_roster[filtered_team_roster['player_id'] == player_id].head(num_rows_slider)   
                    st.write(player_matches)

       










   

    




    


    
    
    
    
    
    





   


    
    

   
