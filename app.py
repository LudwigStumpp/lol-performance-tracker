import streamlit as st
from data_grabber.tracker import get_performance
from data_grabber.lol_api import InvalidSummonerNameError

'''
# League of Legends Performance Tracker
This tool helps you to track your performance on the rift.

For the last 10 games, it shows in a graph:
- KDA
- Gold / Min
- Dmg / Min
- Vision / Min
- CS / Min

Wins are marked in green, losses in red.
'''

'### Enter your summoner name and hit Enter:'
summoner_name = st.text_input('')

if summoner_name != '':
    try:
        with st.spinner(f'Hello {summoner_name}! We will grab your last 10 matches now...'):
            df = get_performance(summoner_name)
            f'{summoner_name} last 10 matches:'
            st.pyplot()
    except InvalidSummonerNameError:
        st.error('Invalid summoner name.')
    except:
        st.error('Ups! Something went wrong. Try another summoner name.')

'''
### Info on units:
One needs to multiply to get the real values:
- Gold / Min: * 100 
- DMG / Min: * 100
- Vision / Min: / 10
------
Made with :heart: in Munich by [Ludwig](https://ludwigstumpp.com).
'''
