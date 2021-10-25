from datetime import datetime, date

data_now = date.today()
time_now = datetime.now().time()
data_now = data_now.strftime('%d.%m.%Y')
time_now = time_now.strftime('%H:%M')
print(time_now)
print(data_now)
