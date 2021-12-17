import requests
import dataclasses as D
from datetime import datetime

@D.dataclass
class Snapshot:
    timestamp: int
    buy: int
    sell: int
    supply: int
    demand: int
    sold: int
    __unknown: int
    bought: int
    __unknown2: int
    date: datetime = D.field(init=False)

    def __post_init__(self):
        self.date = datetime.fromtimestamp(self.timestamp)


def fetch_snapshots(*, item_id=92103):
    url = f'https://www.gw2bltc.com/api/tp/chart/{item_id}'
    data = requests.get(url).json()
    snapshots = [Snapshot(*frame) for frame in data]
    return snapshots
