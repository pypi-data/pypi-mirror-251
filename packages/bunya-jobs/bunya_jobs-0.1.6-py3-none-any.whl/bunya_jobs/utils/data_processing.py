import pandas as pd
from typing import List


def strip_spaces(l: List[str]) -> List[str]:
    return [x for x in l if x != ""]


def stdout_to_dataframe(s: str) -> pd.DataFrame:
    s = s.strip()
    s_list = s.split("\n")
    headers = strip_spaces(s_list[0].split(" "))
    data = [strip_spaces(element.split(" ")) for element in s_list[1:]]
    return pd.DataFrame(data=data, columns=headers)
