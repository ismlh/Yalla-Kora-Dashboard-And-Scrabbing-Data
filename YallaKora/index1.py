# pip install requests
# pip install beautifulsoup4
# pip install lxml

import requests as req
from bs4 import BeautifulSoup
import csv
from datetime import date, timedelta
import time

# -------------------------
# دوال مساعدة
# -------------------------

def scrabData(res,d):
    src = res.content
    soup = BeautifulSoup(src, "lxml")
    return getAllMatchesData(soup,d)

def getChampionShips(soup):  # master divs that contain all data
    CH_Types = soup.find_all("div", {'class': 'matchCard'})
    return CH_Types 

def getAllMatchesData(soup,day):
    all_Matches_Data = []

    Champions = getChampionShips(soup)

    for champion in Champions:
        champion_name = champion.find('h2').text.strip()

        allMatches = champion.find_all("div", {"class": "item"})
        for match in allMatches:
            TeamA = match.find("div", {"class": "teamA"}).find('p').text.strip()
            TeamB = match.find("div", {"class": "teamB"}).find('p').text.strip()

            Teams_SCore = match.find("div", {"class": "MResult"}).find_all(
                "span", {"class": "score"}
            )
            if len(Teams_SCore) < 2:  # لو المباراة لم تُلعب بعد
                team_A_Score = ""
                team_B_Score = ""
            else:
                team_A_Score = Teams_SCore[0].text.strip()
                team_B_Score = Teams_SCore[1].text.strip()

            Match_Time = match.find("div", {"class": "MResult"}).find(
                "span", {"class": "time"}
            ).text.strip()

            all_Matches_Data.append({
                "Champoin Type": champion_name,
                "Team A": TeamA,
                "Team B": TeamB,
                "Team A Score": team_A_Score,
                "Team B Score": team_B_Score,
                "Match Time": Match_Time,
                "day":d
            })

    return all_Matches_Data

def export_To_CSV(Data,year):
    if not Data:
        print("No data to export")
        return

    columns = Data[0].keys()

    with open(f'matches_Details_{year}.csv', 'w', newline='', encoding='utf-8-sig') as f:
        dict_writer = csv.DictWriter(f, columns)
        dict_writer.writeheader()
        dict_writer.writerows(Data)
        print(f"File Created: matches_Details_{year}.csv")

def get_all_dates_of_year(year):
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)

    current_date = start_date
    dates = []

    while current_date <= end_date:
        dates.append(current_date.strftime("%m/%d/%Y"))
        current_date += timedelta(days=1)

    return dates

# -------------------------
# Main
# -------------------------

year = int(input("Enter Year (YYYY): "))
all_data = []

dates = get_all_dates_of_year(year)

for d in dates:
    pageLink = f"https://www.yallakora.com/match-center?date={d}"
    response = req.get(pageLink)

    print(f"Scraping date {d} | Status Code: {response.status_code}")

    if response.status_code == 200:
        day_data = scrabData(response,d)
        if day_data:
            all_data.extend(day_data)

    # لتجنب الحظر من الموقع
   # time.sleep(1)

# تصدير CSV
export_To_CSV(all_data,year)
