import ujson as json
from collections import defaultdict, Counter


if __name__ == "__main__":
    data = defaultdict(lambda : Counter())
    networks = set()
    for line in open("referrers.tsv"):
        key_raw, value_raw = line.strip().rsplit('\t', 1)
        key = json.loads(key_raw)
        value = float(value_raw)

        ctry = key["c"]
        network = key["sn"]
        networks.add(network)

        if ctry not in data:
            data[ctry] = {}

        data[ctry][network] = value

    totals = {}
    for network in networks:
        high = max(x.get(network, 0) for x in data.itervalues())
        low = min(x.get(network, high) for x in data.itervalues())
        totals[network] = {
            "high" : high,
            "low" : low,
        }

    json.dump({"country" : data, "totals" : totals, "networks" : list(networks)}, open("ctry_ntwk.json", "w+"))



