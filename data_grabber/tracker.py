import time
import pandas as pd
import matplotlib.pyplot as plt

from . import lol_api


def get_performance(summoner_name):
    account_id = lol_api.fetch_summoner_account_id(summoner_name)
    last_matches = lol_api.fetch_last_matches(account_id, 10)

    table_rows = []
    df = pd.DataFrame(columns=['Lane', 'Champ', 'Win', 'KDA', 'Gold / Min', 'Dmg / Min', 'Vision / Min', 'CS / Min'])

    for i in range(len(last_matches)):
        match = last_matches[i]
        game_id = match['gameId']
        match_info = lol_api.fetch_match_info(game_id)
        participant_id = lol_api.parse_participant_id(match_info, account_id)
        participant_match_info = lol_api.parse_participant_match_info(match_info, participant_id)
        game_duration = lol_api.parse_dame_duration(match_info)
        champion_id, lane, kills, deaths, assists, gold_earned, total_minions_killed, neutral_minions_killed, total_damage_dealt_to_champions, vision_score, win = lol_api.parse_useful_participant_match_info(participant_match_info)
        champion_name = lol_api.get_champion_name(champion_id)

        kda = (kills + assists) / max(deaths, 1)
        gold_per_min = gold_earned * 60 / game_duration / 100
        dmg_per_min = total_damage_dealt_to_champions * 60 / game_duration / 100
        minions_per_min = (neutral_minions_killed + total_minions_killed) * 60 / game_duration
        vis_per_min = vision_score * 60 / game_duration * 10

        df.loc[len(last_matches) - i - 1] = [lane, champion_name, win, kda, gold_per_min, dmg_per_min, vis_per_min, minions_per_min]

        time.sleep(0.1)

    df = df[::-1]

    # multiple line plot
    fig, _ = plt.subplots()
    for column in df.columns:
        if column not in ['Lane', 'Champ', 'Win']:
            plt.plot(column, data=df)

    # build x ticks
    xticks = []
    win_indices = []
    for index, row in df.iterrows():
        xticks.append(f'{row.Lane}, {row.Champ}')
        if row.Win:
            win_indices.append(index)
    plt.xticks(range(df.shape[0]), xticks, color='red', rotation='vertical')
    plt.tight_layout()
    for w in win_indices:
        plt.gca().get_xticklabels()[w].set_color('green')

    # Grid + Legend
    plt.grid(color='k', linestyle='-', linewidth=0.5)
    plt.legend()

    return fig
