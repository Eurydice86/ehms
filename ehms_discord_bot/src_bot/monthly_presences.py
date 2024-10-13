import sqlite3
import requests
import json
import datetime
import os
import random

from dotenv import load_dotenv


load_dotenv()
number_of_results = 5
database = os.getenv("DB")
myclub_token = os.getenv("MC_TOKEN")
headers = {"X-myClub-token": myclub_token}

def build_query(last_month, group, number_of_results):

    return f"""
select m.member_id, count(*), e.starts_at from members m
join presences p on m.member_id = p.member_id
join events e on e.event_id = p.event_id
join groups g on g.group_id = e.group_id
where starts_at like '{last_month}%'
and g.group_id like {group}
group by m.member_id
order by 2 desc limit {number_of_results};
    """


def group_monthly_presences(group):
    now = datetime.datetime.now()
    first_month_day = now.replace(day=1)
    last_day_of_previous_month = first_month_day - datetime.timedelta(days=1)

    last_month = f"{last_day_of_previous_month.year}-"
    last_month += f"{last_day_of_previous_month.month:02}"

    conn = sqlite3.Connection(database)
    cursor = conn.cursor()

    query0 = f"select group_name from groups where group_id like {group};"

    q_result = cursor.execute(query0).fetchone()
    group_name = str(q_result).strip("('),")

    message = f"**{group_name}**\n"

    query = build_query(last_month, group, number_of_results)

    result = cursor.execute(query).fetchall()
    members_list = []

    base_url = "https://ehms.myclub.fi/api/"
    for r in result:
        id = str(r[0]).strip("(,)'")
        member_url = "members/" + id
        full_url = base_url + member_url
        response = requests.get(full_url, headers=headers)
        content = json.loads(response.content)
        m = content.get("member")
        member = f"{m.get("first_name")} {m.get("last_name")}"
        members_list.append(member)

    random.shuffle(members_list)

    for m in members_list:
        message += f"{m}\n"

    return message + "\n"


def monthly_presences():
    message = "# Last month's top presences\n **(top 5 per weapon in no particular order)**\n\n"
    message += group_monthly_presences("28112")
    message += group_monthly_presences("28114")
    message += group_monthly_presences("28115")
    message += group_monthly_presences("28121")
    message += group_monthly_presences("31363")
    message += group_monthly_presences("38874")
    message += group_monthly_presences("48332")
    return message


if __name__ == "__main__":
    monthly_presences()
