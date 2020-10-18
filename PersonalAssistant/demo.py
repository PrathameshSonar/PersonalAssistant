from datetime import date, datetime
import time

dt_string = input('\nDate (DD/MM/YYYY): ')

dt = datetime.strptime(dt_string,"%d/%m/%Y")
print(dt)
d = datetime.today()
print(d)
if dt <= d:
    print('Date should be greater than todays date')
else:

    print('fine')
        



        
