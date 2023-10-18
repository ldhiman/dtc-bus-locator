import gtfs_realtime_pb2
import urllib.request
import threading
import time
import turtle

print("Inititalizing...")

import StaticData


dataList = {}

stop_task = False


def background_task():
    while not stop_task:
        feed = gtfs_realtime_pb2.FeedMessage()

        # Replace this URL with the correct GTFS Realtime feed URL
        feed_url = "https://otd.delhi.gov.in/api/realtime/VehiclePositions.pb?key=8YFFZlIaZSrR2790xMx0cmTQ2n2qadOn"

        response = urllib.request.urlopen(feed_url)
        feed.ParseFromString(response.read())

        # print("Fetching Data..")
        for entity in feed.entity:
            vehicleID = entity.id
            data = entity.vehicle
            route = data.trip.route_id
            tripDetail = data.trip
            position = data.position
            if hasattr(entity, "timestamp"):
                print(entity.timestamp)
            data = {
                "id": vehicleID,
                "lat": position.latitude,
                "lon": position.longitude,
                "route": tripDetail.route_id,
                "trip_id": tripDetail.trip_id,
                "start_time": tripDetail.start_time,
                "start_date": tripDetail.start_date,
                "speed": position.speed,
                "scheduled": tripDetail.schedule_relationship,
                # "lastFetched": entity.timestamp,
            }

            dataList[vehicleID] = data

        # print("Data Feteched Successful")
        time.sleep(10)


def lat_lon_to_screen(lat, lon, width, height):
    # Define the range of latitude and longitude you want to represent
    lat_min = -90
    lat_max = 90
    lon_min = -180
    lon_max = 180

    # Calculate x and y screen coordinates based on the range
    x = int((lon - lon_min) / (lon_max - lon_min) * width)
    y = int((lat - lat_min) / (lat_max - lat_min) * height)

    return x, y


def draw_path(path_details):
    # Create a turtle screen
    screen = turtle.Screen()
    screen.title("Latitude-Longitude Path")
    screen.setup(width=800, height=600)

    # Create a turtle object
    path_turtle = turtle.Turtle()
    path_turtle.speed(1)
    path_turtle.penup()
    path_turtle.goto(
        lat_lon_to_screen(
            path_details[0]["stop_data"]["stop_lat"],
            path_details[0]["stop_data"]["stop_lon"],
            800,
            600,
        )
    )
    path_turtle.pendown()

    for coord in path_details[1:]:
        path_turtle.goto(
            lat_lon_to_screen(
                path_details[0]["stop_data"]["stop_lat"],
                path_details[0]["stop_data"]["stop_lon"],
                800,
                600,
            )
        )

    screen.exitonclick()


bg_thread = threading.Thread(target=background_task)
bg_thread.start()
print("Initalised!!")


def getBusByRoute(route):
    for a in dataList:
        if route in dataList["route"]:
            return a
    return -1


typeIf = input("Enter 1 for bus number and any other for route number: ")
while True:
    if typeIf == 1:
        id = input("Enter Bus Number to track: ")
        if id == "":
            break
        try:
            data = dataList[id]
            data["stops"] = StaticData.getStopTimes(data["trip_id"], data["route"])
            print(data)
            draw_path(data["stops"]["path_detail"])
        except Exception as e:
            print(e)
            # print("Bus Not Found!!")
    else:
        id = input("Enter Route Number to track: ")
        if id == "":
            break
        try:
            data = getBusByRoute(StaticData.getRouteIDbyName(str(id)))
            data["stops"] = StaticData.getStopTimes(data["trip_id"], data["route"])
            print(data)
            draw_path(data["stops"]["path_detail"])
        except Exception as e:
            print(e)
            # print("Bus Not Found!!")


print("End!!")


# id = DL1PC6580

# id: "DL1PC9122"
# vehicle {
#  trip {
#    trip_id: "5198_11_30"
#    route_id: "5198"
#    start_time: "11:45:08"
#    start_date: "20231017"
#    schedule_relationship: SCHEDULED
#  }
#  vehicle {
#    id: "DL1PC9122"
#    label: "DL1PC9122"
#  }
#  position {
#    latitude: 28.6186371
#    longitude: 77.2352905
#    speed: 0
#  }
#  timestamp: 1697527144
# }
