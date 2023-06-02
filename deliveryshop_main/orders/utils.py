import datetime

def generate_order_number(pk):
    #strftime will convert object to a string according to a given format
    # %Y prints the year/ %m the month/ %d my current date
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S') #2022060244
    order_number = current_datetime + str(pk)
    return order_number


