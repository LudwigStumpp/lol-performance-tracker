import streamlit as st
import modules.tracker as tracker

'# LOL Performance Tracker'


summoner_name = st.text_input("Please enter your summoner name and hit Enter.")

if summoner_name != '':
    try:
        with st.spinner(f'Hello {summoner_name}! We will grab your last 10 matches now...'):
            df = tracker.get_performance(summoner_name)
            f'{summoner_name} last 10 matches:'
            st.pyplot()
    except tracker.InvalidSummonerNameError:
        'Invalid summoner name'
    except:
        'Try another summoner name'
