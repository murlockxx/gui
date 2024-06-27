import json
from pymavlink import mavutil
import time

class MavlinkHelper:
    def __init__(self, contype, port):
        try:
            self.connection_string = f"{contype}:{port}"
            self.connection = mavutil.mavlink_connection(self.connection_string)
            self.connection.wait_heartbeat()
            print("Heartbeat from system (system %u component %u)" % (self.connection.target_system, self.connection.target_component))
        except Exception as e:
            print(f"Failed to connect: {e}")
            raise

    def location(self, relative_alt=False):
        self.connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        if relative_alt:
            alt = self.connection.messages['GLOBAL_POSITION_INT'].relative_alt * 0.001
        else:
            alt = self.connection.messages['GLOBAL_POSITION_INT'].alt
        return {
            'lat': self.connection.messages['GPS_RAW_INT'].lat * 1.0e-7,
            'lon': self.connection.messages['GPS_RAW_INT'].lon * 1.0e-7,
            'alt': alt,
            'heading': self.connection.messages['VFR_HUD'].heading
        }

    def speed(self):
        self.connection.recv_match(type='VFR_HUD', blocking=True)
        return self.connection.messages['VFR_HUD'].airspeed, self.connection.messages['VFR_HUD'].groundspeed

def fetch_data(helper):
    # Initialize the data structure with default values
    data = {
        'Latitude': None,
        'Longitude': None,
        'Altitude': None,
        'Heading': None,
        'Airspeed': None,
        'Groundspeed': None
    }
    
    try:
        # Attempt to fetch location and speed
        location_data = helper.location(relative_alt=True)
        airspeed, groundspeed = helper.speed()

        # Update the data dictionary with actual values
        data.update({
            'Latitude': location_data['lat'],
            'Longitude': location_data['lon'],
            'Altitude': location_data['alt'],
            'Heading': location_data['heading'],
            'Airspeed': airspeed,
            'Groundspeed': groundspeed
        })
    except Exception as e:
        print(f"Error fetching data: {e}")
        # No need to change 'data', it's already initialized with None values

    return data  # Return the data dictionary regardless of success or failure

# Example usage
contype = "tcp"
port = "127.0.0.1:5763"
helper = MavlinkHelper(contype, port)
data = fetch_data(helper)
print(json.dumps(data, indent=4))
