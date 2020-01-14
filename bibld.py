# читаем директори и читаем каждый файл в директории, создаем файл карегорий привязки файл-название
# можно брать от сюда https://bible.by/every-day/ план, но я беру локально из директории Plan.html -- уже не так
import os, requests, wget
import datetime
from bs4 import BeautifulSoup
import calendar
from datetime import timedelta

#from datetime import datetime, timedelta
#def get_dates():
#    date_format = '%d.%m.%Y'
#    today = datetime.now()
#    yesterday = today - timedelta(days=1)
#    #after_tomorrow = today + timedelta(days=2)
#   return {'today': today.strftime(date_format),
#            'yesterday': yesterday.strftime(date_format)}
#print(get_dates().get('today'))
#print(get_dates().get('yesterday'))

#print (calendar.monthrange(2019,8)[1])
#d = datetime.date.now()
#vchera = datetime.today() - timedelta(days=1)
#print(d.year) # 2012
#print(d.day)  # 14
#print(d.month) # 12
#vchera = print(d.day)
#print(vchera)
#print (datetime.date.day())
#exit(0)

iftest = False
s0 = requests.get('https://bible.by/every-day/')
bs = BeautifulSoup(s0.text, "html.parser")

playlist = open('bibl.m3u8', "w", encoding='utf-8')
playlist.write("#EXTM3U\n")
playlist.close()
#html_main = open('Plan.html', 'r', encoding='utf-8').read()

#bs = BeautifulSoup(html_main, 'html.parser')


d = datetime.date.today()
yesterday = d - timedelta(days=1)
print(d)
print('день:', d.day)
print('месяц:', d.month)
print('yesterday:', yesterday)
d = str(d)

def bibldwn(day, month, year):
	#находим 
	#  -- заголовок месяца
	# -- находим за ним все, что к этому месяцу относится
	# -- находим только нужный день
	# -- находим все ссылки на этот день
	print('Качаем день:', day, ' месяц:', month, ' год:', year)

	links_today = bs('h3', limit=month)[-1].find_next('ol').find_all('li')[day-1].find_all('a')



	no = 300
	for tag in links_today:
		link = tag.get('href')
		namef = tag.text.replace(' ','_')
		print(link , namef)
		s1 = requests.get('https://bible.by'+link)
		soup1 = BeautifulSoup(s1.text, "html.parser")
		#print(
		# нужно удалить все лишнее, что вылезает внизу после текста
		#soup1 = soup1.find('div',class_="hidden-xs").decompose()
		#soup1.find('span',class_="btn-group").extract()
		# скачаем звук
		print(soup1.find('source').get('src'))
		zvuk = str(soup1.find('source').get('src'))
		filename = wget.download('http:'+zvuk)
		os.rename(filename, u''+os.getcwd()+'/'+namef+'_'+filename)
		


		for tag in soup1.find_all('span',class_='btn-group'):
			tag.extract()

		#print(soup1.text)
		for tag in soup1.find_all('div', class_='hidden-xs'):
			tag.extract()

		z1 = soup1.h1.text # заголовок
		z2 = soup1.find('p',class_="gray").text # подпись
		z3 = soup1.find('div',class_="text bible").text # текст
		z3 = z3.replace('Обратите внимание. Номера стихов – это ссылки, ведущие на раздел со сравнением переводов, параллельными ссылками, текстами с номерами Стронга. Попробуйте,', '')
		z3 = z3.replace('возможно вы будете приятно удивлены.', '')
		print(z1)
		print(z2)
		print(z3)
		read_day = open(namef+'.txt', "w", encoding='utf-8')
		read_day.write(z1+'\n'+z2+'\n'+z3+'\n')
		read_day.close()

		playlist = open('bibl.m3u8', "a", encoding='utf-8')

		playlist.write("#EXTINF:"+str(no)+","+z1+"\n")
		playlist.write("/storage/emulated/0/Download/bibl/"+namef+'_'+filename+"\n")
		no = no + 1

		playlist.close()

		pass

def veradwn():
	no = 400
	s2 = requests.get('https://radiovera.ru/')
	bsoup = BeautifulSoup(s2.text, "html.parser")

	mp3evg = bsoup('a', {"class": "link-download-evangelie"})
	mp3cal = bsoup('a', {"class": "link-download-calendar"})

	mp3evgs = mp3evg[0].get('href')
	mp3evgt = mp3evg[0].get('download')
	print(mp3evgs, mp3evgt)

	mp3cals = mp3cal[0].get('href')
	mp3calt = mp3cal[0].get('download')
	print(mp3cals, mp3calt)	

	#mp3s = bsoup('a', {"class": "hh-autoplay-link"})[0].get('data-audio-src')
	#mp3t = bsoup('a', {"class": "hh-autoplay-link"})[0].get('data-audio-title')
	print("Dowload from radio Vera")
	filenameevg = wget.download(mp3evgs)
	filenamecal = wget.download(mp3cals)

	os.rename(filenameevg, u''+os.getcwd()+'/'+filenameevg)
	os.rename(filenamecal, u''+os.getcwd()+'/'+filenamecal)

	playlist = open('bibl.m3u8', "a", encoding='utf-8')

	playlist.write("#EXTINF:"+str(no)+","+mp3evgt+"\n")
	playlist.write("/storage/emulated/0/Download/bibl/"+filenameevg+"\n")
	print("#EXTINF:"+str(no)+","+mp3evgt+"\n")
	print("/storage/emulated/0/Download/bibl/"+filenameevg+"\n")

	playlist.write("#EXTINF:"+str(no+1)+","+mp3calt+"\n")
	playlist.write("/storage/emulated/0/Download/bibl/"+filenamecal+"\n")
	print("#EXTINF:"+str(no+1)+","+mp3calt+"\n")
	print("/storage/emulated/0/Download/bibl/"+filenamecal+"\n")

	playlist.close()

	pass

# читаем файл с датой
try:
    file = open("lastdate.dat", "r")
    ld = file.read()
    print(ld)
    file.close()
except FileNotFoundError:
	# если файла нет - дату ставим вчерашний день
	print('Файл не найден --- >>> ставим вчерашнюю')
	ld = yesterday
except IOError:
    print('Проблемы с открытием')

if (ld == d):
	print("Даты совпадают - уже запускали сегодня")
else:
	print("Даты не совпадают: текущая дата", d, "дата в файле", ld)
	# разбираем файл, если даты не совпадают
	lastday = str(ld).split("-")
	curentday = d.split("-")
	print(lastday, curentday)
	if (lastday[0]!=curentday[0]):
		print("Год не совпадает!!!")
		exit(0)
	if (lastday[1]!=curentday[1]):
		print("Месяц не совпадает!!!")
		# проверяем, что разница в месяцах только в 1 т.е. произошел переход
		if (int(lastday[1])<int(curentday[1]))and(int(curentday[1])-int(lastday[1])==1):
			print("Работаем дальше")
			dayinmes = calendar.monthrange(int(lastday[0]), int(lastday[1]))[1]
			razn = dayinmes - int(lastday[2])
			print("В предыдущем месяце было дней:",calendar.monthrange(int(lastday[0]), int(lastday[1]))[1])
			print("Разница в днях до конца месяца:", razn)
			for num in range(razn):
				needay = int(lastday[2]) + 1 + num
				print(needay)
				print("качаем", int(needay), int(lastday[1]), curentday[0])
				if iftest:
					print("Тестовый режим! в реале качаем с bible.by", int(needay), int(lastday[1]), curentday[0])
				else:
					bibldwn(int(needay), int(lastday[1]), curentday[0])
		else:
			exit(0)
		#exit(0) # сейчас пока по любому стопорим
		# считаем, что выше все скачалось за пред месяц, дальше нам нужно симитировать только переход через дату
		lastday[2] = 0
		lastday[1] = curentday[1]

	if (lastday[2]!=curentday[2]):
		print("День не совпадает!!!")
		razn = int(curentday[2])-int(lastday[2])
		print("Разница в", razn, "дней")
		for num in range(razn):
			needay = int(lastday[2])+1+num
			print(needay)
			#print("качаем",int(curentday[2])-num, curentday[1], curentday[0])
			if iftest :
				print("Тестовый режим! в реале качаем с bible.by", int(needay), int(curentday[1]), curentday[0])
			else:
				bibldwn(int(needay), int(curentday[1]), curentday[0])
		if iftest :
			print("Тестовый режим! в реале качаем с Веры и записываем в файл текущую дату")
		else :
			# veradwn()
			# записываем текущую дату в файл
			file = open("lastdate.dat", "w")
			file.write(d)
			file.close()
