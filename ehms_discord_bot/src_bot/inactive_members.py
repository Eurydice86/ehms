import sqlite3
import requests
import json
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
database = os.getenv("DB")
myclub_token = os.getenv("MC_TOKEN")
headers = {"X-myClub-token": myclub_token}


def inactive_members():
    now = datetime.datetime.now()
    first_month_day = now.replace(day=1)
    last_day_of_previous_month = first_month_day - datetime.timedelta(days=1)

    three_months_ago = f"{last_day_of_previous_month.year}-"
    three_months_ago += f"{(last_day_of_previous_month.month - 2):02}"

    now_month = f"{now.year}-"
    now_month += f"{now.month:02}"

    message = f"# Inactive members (have not trained in 3 months) as of {first_month_day.date()}\n"
    message += "## Members on this list are kindly requested to take any gear stored at the salle, in order to make space for active members' gear\n"
    message += "### If you see your name on this list but _have_ been at training in the last three months, please contact the Board by email\n"

    query = f"""
    with active as
    (select distinct m.member_id
    from members m
    join presences p on m.member_id = p.member_id
    join events e on e.event_id = p.event_id
    where
    p.confirmed like 'True'
    and e.starts_at between '{three_months_ago}' and '{now_month}'),
    all_members as (select m.member_id
    from members m)
    select distinct(l.member_id) from all_members l
    left join active a on a.member_id = l.member_id
    where a.member_id is NULL;
    """

    conn = sqlite3.Connection(database)
    cursor = conn.cursor()

    base_url = "https://ehms.myclub.fi/api/"

    inactive_members_list = []
    q_res = cursor.execute(query).fetchall()
    for q in q_res:
        member_id = str(q).strip("',()")
        member_url = "members/" + member_id
        full_url = base_url + member_url
        response = requests.get(full_url, headers=headers)
        content = json.loads(response.content)
        m = content.get("member")
        inactive_members_list.append(f"{m.get("last_name")} {m.get("first_name")}")

    inactive_members_list.sort()
    mes = ""
    message2 = []
    counter = 0
    for m in inactive_members_list:
        if counter < 50:
            counter += 1
            mes += f"{m}\n"
        else:
            counter = 0
            message2.append(mes)
            mes = f"{m}\n"
    message2.append(mes)

    conn.commit()
    conn.close()

    return (message, message2)
