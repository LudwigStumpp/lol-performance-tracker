import streamlit as st
import modules.tracker as tracker

"""
# LOL Performance Tracker
This tool helps you to track your performance on the rift.

For the last 10 games, the tools shows:
- KDA
- Gold / Min
- Dmg / Min
- Vision / Min

Wins are marked in green, losses in red.
"""

'### Enter your summoner name and hit Enter:'
summoner_name = st.text_input('')

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

'''
------
Made with :heart: in Munich by [Ludwig](https://ludwigstumpp.com).
'''
