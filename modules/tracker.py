import requests
import json
import time
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv


class InvalidSummonerNameError(Exception):
    """Raised when summoner name is invalid"""
    pass


def get_summoner_account_id(header, summoner_name):
    url = f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
    try:
        resp = requests.get(url, headers=header)
        return resp.json()['accountId']
    except KeyError:
        raise InvalidSummonerNameError


def get_last_matches(header, account_id, number):
    url = f'https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}'
    resp = requests.get(url, headers=header)
    return resp.json()['matches'][:number]


def get_match_info(header, game_id):
    url = f'https://euw1.api.riotgames.com/lol/match/v4/matches/{game_id}'
    resp = requests.get(url, headers=header)
    return resp.json()


def get_participant_id(match_dict, account_id):
    participant_identities = match_dict['participantIdentities']

    for identity in participant_identities:
        player = identity['player']
        if player['accountId'] == account_id:
            return identity['participantId']


def get_participant_match_info(match_dict, participant_id):
    participants = match_dict['participants']

    for participant in participants:
        if participant['participantId'] == participant_id:
            return participant


def get_useful_match_info(match_dict):
    game_duration = match_dict['gameDuration']

    return game_duration


def get_useful_participant_match_info(participant_match_info):
    lane = participant_match_info['timeline']['lane']

    champion_id = participant_match_info['championId']

    stats = participant_match_info['stats']

    vision_score = stats['visionScore']
    total_damage_dealt_to_champions = stats['totalDamageDealtToChampions']
    kills = stats['kills']
    assists = stats['assists']
    deaths = stats['deaths']
    gold_earned = stats['goldEarned']
    total_minions_killed = stats['totalMinionsKilled']
    neutral_minions_killed = stats['neutralMinionsKilled']
    win = stats['win']

    return champion_id, lane, kills, deaths, assists, gold_earned, total_minions_killed, neutral_minions_killed, total_damage_dealt_to_champions, vision_score, win


def get_champion_name(champions_dict, champion_id):
    data = champions_dict['data']
    for champion_name in data:
        if int(data[champion_name]['key']) == int(champion_id):
            return champion_name


def get_performance(summoner_name):
    account_id = get_summoner_account_id(header, summoner_name)
    last_matches = get_last_matches(header, account_id, 10)

    table_rows = []
    df = pd.DataFrame(columns=['Lane', 'Champ', 'Win',
                               'KDA', 'Gold / Min', 'Dmg / Min', 'Vision / Min'])

    for i in range(len(last_matches)):
        match = last_matches[i]

        game_id = match['gameId']

        match_info = get_match_info(header, game_id)

        participant_id = get_participant_id(match_info, account_id)

        participant_match_info = get_participant_match_info(
            match_info, participant_id)

        game_duration = get_useful_match_info(match_info)

        champion_id, lane, kills, deaths, assists, gold_earned, total_minions_killed, neutral_minions_killed, total_damage_dealt_to_champions, vision_score, win = get_useful_participant_match_info(
            participant_match_info)

        champion_name = get_champion_name(champions_dict, champion_id)
        kda = (kills + assists) / max(deaths, 1)
        gold_per_min = gold_earned * 60 / game_duration / 100
        dmg_per_min = total_damage_dealt_to_champions * 60 / game_duration / 100
        minions_per_min = (neutral_minions_killed +
                           total_minions_killed) * 60 / game_duration
        vis_per_min = vision_score * 60 / game_duration * 10

        df.loc[len(last_matches) - i - 1] = [lane, champion_name,
                                             win, kda, gold_per_min, dmg_per_min, vis_per_min]

        time.sleep(0.1)

    df = df[::-1]

    # multiple line plot
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


load_dotenv()
api_key = os.environ['LOL_API_KEY']
header = {
    'X-Riot-Token': api_key,
}

with open('champion.json', encoding='utf8') as json_file:
    champions_dict = json.load(json_file)
