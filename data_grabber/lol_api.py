import requests
import os
from dotenv import load_dotenv

from typing import Dict, Tuple


class InvalidSummonerNameError(Exception):
    """Raised when summoner name is invalid"""
    pass


def fetch_summoner_account_id(summoner_name: str) -> str:
    url = f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
    try:
        resp = requests.get(url, headers=HEADER)
        return resp.json()['accountId']
    except KeyError:
        raise InvalidSummonerNameError


def fetch_last_matches(account_id: str, number: int) -> Dict:
    url = f'https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}'
    resp = requests.get(url, headers=HEADER)
    return resp.json()['matches'][:number]


def fetch_match_info(game_id: str) -> Dict:
    url = f'https://euw1.api.riotgames.com/lol/match/v4/matches/{game_id}'
    resp = requests.get(url, headers=HEADER)
    return resp.json()


def parse_participant_id(match_dict: Dict, account_id: str) -> str:
    participant_identities = match_dict['participantIdentities']

    for identity in participant_identities:
        player = identity['player']
        if player['accountId'] == account_id:
            return identity['participantId']


def parse_participant_match_info(match_dict: Dict,
                                 participant_id: str) -> Dict:
    participants = match_dict['participants']

    for participant in participants:
        if participant['participantId'] == participant_id:
            return participant


def parse_dame_duration(match_dict: Dict) -> int:
    game_duration = match_dict['gameDuration']

    return game_duration


def parse_useful_participant_match_info(participant_match_info: Dict) -> Tuple:
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

    return champion_id, lane, kills, deaths, assists, gold_earned, total_minions_killed, neutral_minions_killed, \
        total_damage_dealt_to_champions, vision_score, win


def get_champion_name(champion_id: int) -> str:
    data = champions_dict['data']
    for champion_name in data:
        if int(data[champion_name]['key']) == int(champion_id):
            return champion_name


load_dotenv()
HEADER = {
    'X-Riot-Token': os.environ['LOL_API_KEY'],
}
champions_dict = requests.get('http://ddragon.leagueoflegends.com/cdn/10.18.1/data/en_US/champion.json').json()
