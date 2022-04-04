from datetime import datetime
def generate_time_stamp():
    datetime_obj = datetime.now()
    timestamp = datetime_obj.strftime("%d-%b-%Y_%H_%M_%S-%f")
    return timestamp