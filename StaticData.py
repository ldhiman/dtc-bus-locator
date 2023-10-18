import ujson

# DTC Files
dtc_calender = r"D:\Python\DTC Live Bus tracking\DTC_GTFS\calendar.json"
dtc_agency = r"D:\Python\DTC Live Bus tracking\DTC_GTFS\agency.json"
dtc_fare_attributes = r"D:\Python\DTC Live Bus tracking\DTC_GTFS\fare_attributes.json"
dtc_fare_rules = r"D:\Python\DTC Live Bus tracking\DTC_GTFS\fare_rules.json"
dtc_stop_times = r"D:\Python\DTC Live Bus tracking\DTC_GTFS\stop_times.json"
dtc_stops = r"D:\Python\DTC Live Bus tracking\DTC_GTFS\stops.json"
dtc_trips = r"D:\Python\DTC Live Bus tracking\DTC_GTFS\trips.json"
dtc_routes = r"D:\Python\DTC Live Bus tracking\DTC_GTFS\routes.json"


# DMRC Files
dmrc_agency = r"D:\Python\DTC Live Bus tracking\DMRC_GTFS\agency.json"
dmrc_calender = r"D:\Python\DTC Live Bus tracking\DMRC_GTFS\calendar.json"
dmrc_routes = r"D:\Python\DTC Live Bus tracking\DMRC_GTFS\routes.json"
dmrc_shapes = r"D:\Python\DTC Live Bus tracking\DMRC_GTFS\shapes.json"
dmrc_stop_times = r"D:\Python\DTC Live Bus tracking\DMRC_GTFS\stop_times.json"
dmrc_stops = r"D:\Python\DTC Live Bus tracking\DMRC_GTFS\stops.json"
dmrc_trips = r"D:\Python\DTC Live Bus tracking\DMRC_GTFS\trips.json"


with open(dtc_routes, "r") as file:
    dtc_routes_content = file.read()

dtc_routes_json = ujson.loads(dtc_routes_content)

# print(dtc_routes_json)

with open(dtc_stops, "r") as file:
    dtc_stops_content = file.read()

dtc_stop_json = ujson.loads(dtc_stops_content)

# print(dtc_stop_json)

with open(dtc_stop_times, "r") as file:
    dtc_stop_times_content = file.read()

dtc_stop_times_json = ujson.loads(dtc_stop_times_content)

# print(dtc_stop_times_json)


def getStopTimes(tripId, routeID):
    combinedData = {}
    combinedData["route_detail"] = getRoute(routeID)
    datalist = []
    for a in dtc_stop_times_json:
        if a["trip_id"] == tripId:
            data = {
                "arrival_time": a["arrival_time"],
                "departure_time": a["departure_time"],
                "stop_id": a["stop_id"],
                "stop_sequence": a["stop_sequence"],
                "stop_data": getStopData(a["stop_id"]),
            }
            datalist.append(data)

    datalist = sorted(datalist, key=lambda x: int(x["stop_sequence"]))
    combinedData["path_detail"] = datalist
    return combinedData


def getStopData(id):
    for a in dtc_stop_json:
        if a["stop_id"] == id:
            return a
    return -1


def getRoute(id):
    for a in dtc_routes_json:
        if a["route_id"] == id:
            return a
    return -1


def getRouteIDbyName(name):
    for a in dtc_routes_json:
        if a["route_long_name"] == name:
            return a["route_id"]


# print(getStopTimes("5198_11_30"))
