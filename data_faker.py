import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta


def important_task_maker(number):
    data = []
    for i in range(number):
        num = random.randint(1, number + 1)
        while num in data:
            num = random.randint(1, number + 1)
        data.append(num)
    return data

def dates_creator(number):
    data = []
    for i in range(number):
        created_at = (datetime.now() - timedelta(days=random.randint(0, 365)))
        updated_at = (created_at + timedelta(days=random.randint(1, 365)))
        time_limit = (updated_at + timedelta(days=random.randint(180, 730)))
        data.append([created_at, updated_at, time_limit])
    return data


fake = Faker("ja_JP")
dates = dates_creator(300)
data = {
    "name": [fake.sentence() for _ in range(300)],
    "details": [fake.text() for _ in range(300)],
    "time_limit": [dates[i][2].strftime("%Y-%m-%d") for i in range(300)],
    "importance": important_task_maker(300),
    "cost": [random.randint(1000, 100000) for _ in range(300)],
    "category": [random.choice(["仕事", "運動", "家族", "友達"]) for _ in range(300)],
    "complete": [random.choice([0, 1]) for _ in range(300)],
    "created_at": [dates[i][0].strftime("%Y-%m-%d") for i in range(300)],
    "updated_at": [dates[i][1].strftime("%Y-%m-%d") for i in range(300)],
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV file
df.to_csv("tasks_data.csv", index=False)
