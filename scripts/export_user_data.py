import numpy as np
import pandas as pd
from django.contrib.auth.models import User

from users.models import Profile

users = pd.DataFrame(User.objects.all().values())
profiles = pd.DataFrame(Profile.objects.all().values())

data = (
    users.merge(profiles, left_on="id", right_on="user_id", how="left")
    .rename(columns={"id_x": "id"})
    .loc[:, ["id", "username", "first_name", "last_name", "trikotnummer"]]
    .set_index("id")
    .sort_index()
)


data["list_name"] = data["first_name"] + " " + data["last_name"]
data["list_name"] = np.where(data["list_name"] == " ", data["username"], data["list_name"])

data.to_csv("data/userdata.csv")
