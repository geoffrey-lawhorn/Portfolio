import numpy as np
import pandas as pd
import statsapi as mapi
import collections
from pandas.api.types import is_hashable


def createTeamLookup():
    teams = mapi.lookup_team("")
    team_codes = []
    team_name = []
    for team_code in teams:
        team_codes.append(team_code["id"])
        team_name.append(team_code["teamName"])
    codes = np.asarray(team_codes)
    names = np.asarray(team_name)
    Teams_Codes = pd.DataFrame(data = {"Code": codes, "TeamName": names}, index = codes)
    return Teams_Codes


def pullTeamSchedule(passedCodeTable, start='01/01/2019', end='12/31/2019'):
    codes = np.int64(passedCodeTable.iloc[:,0])
    ret_df = pd.DataFrame()
    for x in codes:
        team_sched = mapi.schedule(start_date=start, end_date=end, team=x)
        x_df = pd.DataFrame(team_sched)

        ret_df = ret_df._append(x_df, ignore_index=True)

    # ret_df.sample(100).map(lambda x: isinstance(x, collections.abc.Hashable)).apply(tuple)
    # ret_df.drop_duplicates()

    return ret_df

def pullTeamSchedule_deprecated(passedCodeTable, start='01/01/2019', end='12/31/2019'):
    codes = np.int64(passedCodeTable.iloc[:,0])
    game_id, game_date, home_id, home_name, away_id, away_name, home_score, away_score, venue_id, venue_name, winning_team, losing_team, winning_pitcher, losing_pitcher, save_pitcher = ([] for i in range(15))
    for x in codes:
        team_sched = mapi.schedule(start_date=start, end_date=end, team=x)
        for d in team_sched:
            game_id.append(d["game_id"])
            game_date.append(d["game_date"])
            home_id.append(d["home_id"])
            home_name.append(d["home_name"])
            away_id.append(d["away_id"])
            away_name.append(d["away_name"])
            home_score.append(d["home_score"])
            away_score.append(d["away_score"])
            venue_id.append(d["venue_id"])
            venue_name.append(d["venue_name"])
            if d["status"]=="Final":
                winning_team.append(d["winning_team"])
                losing_team.append(d["losing_team"])
                winning_pitcher.append(d["winning_pitcher"])
                losing_pitcher.append(d["losing_pitcher"])
                save_pitcher.append(d["save_pitcher"])
            else:
                winning_team.append("")
                losing_team.append("")
                winning_pitcher.append("")
                losing_pitcher.append("")
                save_pitcher.append("")
    
    Team_Schedule = pd.DataFrame(data = {"Game_ID": game_id, "Game_Date": game_date, "Home_ID": home_id, "Home_Name": home_id, "Away_ID": away_id,
                                         "Away_Name": away_name, "Home_Score": home_score, "Away_Score": away_score, "Venue_ID": venue_id, "Venue_Name": venue_name,
                                         "Winning_Team": winning_team, "Losing_Team": losing_team, "Winning_Pitcher": winning_pitcher,
                                         "Losing_Pitcher": losing_pitcher, "Save_Pitcher": save_pitcher}, index = game_id)
    Team_Schedule.drop_duplicates()
    return(Team_Schedule)


"""
codeTable = createTeamLookup()
codeTable_Nats = codeTable[codeTable.Code==120]
sched = pullTeamSchedule(codeTable_Nats, start = "01/01/2023", end = "12/31/2023")
print(sched.dtypes)
print(sched)
"""