import datetime as dt
test = dt.datetime.strptime(input('Введите дату в формате дд.мм.гггг '),'%d.%m.%Y')
print((test-dt.datetime.now()).days + 'дней')