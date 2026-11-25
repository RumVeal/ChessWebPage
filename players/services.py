import requests
from django.utils import timezone


HEADERS = {"User-Agent": "GambitChessClub/1.0 (https://rumveal.pythonanywhere.com)"}
MODES = ["bullet", "blitz", "rapid"]

def fetch_lichess(nickname):
    url=f"https://lichess.org/api/user/{nickname}"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
    except requests.RequestException:
        return None
    
    if response.status_code != 200:
            return None
        
    data = response.json()
    perfs = data.get("perfs", {})

    result = {}
    for mode in MODES:
        perf = perfs.get(mode, {})
        if perf.get("games", 0) > 0:
            result[f"{mode}_rating"] = perf.get("rating")
            result[f"{mode}_prov"] = perf.get("prov", False)
        else:
            result[f"{mode}_rating"] = None
            result[f"{mode}_prov"] = False

    return result
    
def fetch_chesscom(nickname):
    url = f"https://api.chess.com/pub/player/{nickname}/stats"
        
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
    except requests.RequestException:
        return None
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    
    result = {}
    for mode in MODES:
        result[f"{mode}_rating"] = data.get(f"chess_{mode}", {}).get("last", {}).get("rating")
    return result

def update_player_ratings(player):
    errors = []

    if player.lichess_nickname:
        data = fetch_lichess(player.lichess_nickname)
        if data is None:
            errors.append("Lichess nickname not found")
        else:
            for mode in MODES:
                setattr(player, f"lichess_{mode}_rating", data[f"{mode}_rating"])
                setattr(player, f"lichess_{mode}_prov", data[f"{mode}_prov"])
    else:
        for mode in MODES:
            setattr(player, f"lichess_{mode}_rating", None)
            setattr(player, f"lichess_{mode}_prov", False)

    if player.chesscom_nickname:
        data = fetch_chesscom(player.chesscom_nickname)
        if data is None:
            errors.append("Chess.com nickname not found")
        else:
            for mode in MODES:
                setattr(player, f"chesscom_{mode}_rating", data[f"{mode}_rating"])
    else:
        for mode in MODES:
            setattr(player, f"chesscom_{mode}_rating", None)

    player.ratings_updated_at = timezone.now()
    player.save()

    return errors
        