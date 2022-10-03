#Tiek importetas libraries
#Prieks requestiem no API
import requests
#Json prieks parsesanas
import json
#Lai varetu uzgeneret datumu
import datetime
import time
#Prieks zurnalesanas konfiguracijas
import yaml

from datetime import datetime
print('Asteroid processing service')

# Initiating and reading config values
print('Loading configuration from file')

#Mana api atslega un majaslapa kurai ta ir 
nasa_api_key = "i2qMFdo18iOVkYdJGNSvTBP1pc5dcg80IZWcekRe"
nasa_api_url = "https://api.nasa.gov/neo/"

# Dabu sodienas datumu
dt = datetime.now()
#Tiek sakartots datums kuru dabuja
request_date = str(dt.year) + "-" + str(dt.month).zfill(2) + "-" + str(dt.day).zfill(2) 
#Tas tiek izprintets 
print("Generated today's date: " + str(request_date))

#Tiek izprinteti requesta parametri (url, laiki, api atslega)
print("Request url: " + str(nasa_api_url + "rest/v1/feed?start_date=" + request_date + "&end_date=" + request_date + "&api_key=" + nasa_api_key))
#Tas tiek storots r mainigaja
r = requests.get(nasa_api_url + "rest/v1/feed?start_date=" + request_date + "&end_date=" + request_date + "&api_key=" + nasa_api_key)
#Tiek izprinteti status kodi, headeri un texts kas tika ieguts
print("Response status code: " + str(r.status_code))
print("Response headers: " + str(r.headers))
print("Response content: " + str(r.text))

if r.status_code == 200:
#Ja sanemtais statusa kods ir 200 tad tiek ar Json parsets sanemtais texts
	json_data = json.loads(r.text)
#Tiek izveidoti saraksti ar drosajiem un nedrosajiem asteroidiem
	ast_safe = []
	ast_hazardous = []
#parbauda vai parsetaja Json texta ir element_count
	if 'element_count' in json_data:
		#ieliek element_count mainigaja un izprinte asteroidu skaitu
		ast_count = int(json_data['element_count'])
		print("Asteroid count today: " + str(ast_count))
		#Ja asteroidi vairak par 0
		if ast_count > 0:
			#katram asteroidam piefikse vardu,vai ir bistams un cits parametrus
			for val in json_data['near_earth_objects'][request_date]:
				if 'name' and 'nasa_jpl_url' and 'estimated_diameter' and 'is_potentially_hazardous_asteroid' and 'close_approach_data' in val:
					#tiek izveidoti kaut kadi variable kas glaba asteroida vardu un nasas url
					tmp_ast_name = val['name']
					tmp_ast_nasa_jpl_url = val['nasa_jpl_url']
					if 'kilometers' in val['estimated_diameter']:
						if 'estimated_diameter_min' and 'estimated_diameter_max' in val['estimated_diameter']['kilometers']:
							#izveido mainigos kuri glaba vinu lielumus
							tmp_ast_diam_min = round(val['estimated_diameter']['kilometers']['estimated_diameter_min'], 3)
							tmp_ast_diam_max = round(val['estimated_diameter']['kilometers']['estimated_diameter_max'], 3)
						else:
	`						#ja nav asteroidi kilometra diametra tad tiek iedotac citas vertibas
							tmp_ast_diam_min = -2
							tmp_ast_diam_max = -2
					else:
						tmp_ast_diam_min = -1
						tmp_ast_diam_max = -1
					#Tiek galbats kaut kas ar is_potentially_hazardous_asteroid
					tmp_ast_hazardous = val['is_potentially_hazardous_asteroid']
					#parbauda vai nav close_aproach _data teksta
					if len(val['close_approach_data']) > 0:
						#tiek pierakstiti close_aproach_data lielumi
						if 'epoch_date_close_approach' and 'relative_velocity' and 'miss_distance' in val['close_approach_data'][0]:
							tmp_ast_close_appr_ts = int(val['close_approach_data'][0]['epoch_date_close_approach']/1000)
							tmp_ast_close_appr_dt_utc = datetime.utcfromtimestamp(tmp_ast_close_appr_ts).strftime('%Y-%m-%d %H:%M:%S')
							tmp_ast_close_appr_dt = datetime.fromtimestamp(tmp_ast_close_appr_ts).strftime('%Y-%m-%d %H:%M:%S')
							#sitais parbauda atrumu
							if 'kilometers_per_hour' in val['close_approach_data'][0]['relative_velocity']:
								tmp_ast_speed = int(float(val['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']))
							#ja nav vajadzigais tad speed -1
							else:
								tmp_ast_speed = -1
							#panem attalumu
							if 'kilometers' in val['close_approach_data'][0]['miss_distance']:
								tmp_ast_miss_dist = round(float(val['close_approach_data'][0]['miss_distance']['kilometers']), 3)
							else:
							#ja nav tad attalums ir -1
								tmp_ast_miss_dist = -1
						else:
							#iznemuma gadijuma tiek iedotas default vertibas
							tmp_ast_close_appr_ts = -1
							tmp_ast_close_appr_dt_utc = "1969-12-31 23:59:59"
							tmp_ast_close_appr_dt = "1969-12-31 23:59:59"
					else:
						#ja iznemums tad iedod default vertibas
						print("No close approach data in message")
						tmp_ast_close_appr_ts = 0
						tmp_ast_close_appr_dt_utc = "1970-01-01 00:00:00"
						tmp_ast_close_appr_dt = "1970-01-01 00:00:00"
						tmp_ast_speed = -1
						tmp_ast_miss_dist = -1
					#kad tie daudzie if izdariti tiek izprinteti visi asteroidi un to parametri
					print("------------------------------------------------------- >>")
					print("Asteroid name: " + str(tmp_ast_name) + " | INFO: " + str(tmp_ast_nasa_jpl_url) + " | Diameter: " + str(tmp_ast_diam_min) + " - " + str(tmp_ast_diam_max) + " km | Hazardous: " + str(tmp_ast_hazardous))
					print("Close approach TS: " + str(tmp_ast_close_appr_ts) + " | Date/time UTC TZ: " + str(tmp_ast_close_appr_dt_utc) + " | Local TZ: " + str(tmp_ast_close_appr_dt))
					print("Speed: " + str(tmp_ast_speed) + " km/h" + " | MISS distance: " + str(tmp_ast_miss_dist) + " km")
					
					# Adding asteroid data to the corresponding array
					if tmp_ast_hazardous == True:
						ast_hazardous.append([tmp_ast_name, tmp_ast_nasa_jpl_url, tmp_ast_diam_min, tmp_ast_diam_max, tmp_ast_close_appr_ts, tmp_ast_close_appr_dt_utc, tmp_ast_close_appr_dt, tmp_ast_speed, tmp_ast_miss_dist])
					else:
						ast_safe.append([tmp_ast_name, tmp_ast_nasa_jpl_url, tmp_ast_diam_min, tmp_ast_diam_max, tmp_ast_close_appr_ts, tmp_ast_close_appr_dt_utc, tmp_ast_close_appr_dt, tmp_ast_speed, tmp_ast_miss_dist])

		else:
			print("No asteroids are going to hit earth today")
	#Izprinte droso un nedroso asteroidu skaitu
	print("Hazardous asteorids: " + str(len(ast_hazardous)) + " | Safe asteroids: " + str(len(ast_safe)))
	if len(ast_hazardous) > 0:
		#Tiek sortoti bistamie asteroidi
		ast_hazardous.sort(key = lambda x: x[4], reverse=False)
		#Katram tiek izprinteti laiki kad bistamie asteroidi varetu ietriekties
		print("Today's possible apocalypse (asteroid impact on earth) times:")
		for asteroid in ast_hazardous:
			print(str(asteroid[6]) + " " + str(asteroid[0]) + " " + " | more info: " + str(asteroid[1]))
		#Izprintets tuvaka distance asteroidam
		ast_hazardous.sort(key = lambda x: x[8], reverse=False)
		print("Closest passing distance is for: " + str(ast_hazardous[0][0]) + " at: " + str(int(ast_hazardous[0][8])) + " km | more info: " + str(ast_hazardous[0][1]))
	else:
		print("No asteroids close passing earth today")

else:
	#Kaut kas nogajis geizi
	print("Unable to get response from API. Response code: " + str(r.status_code) + " | content: " + str(r.text))
