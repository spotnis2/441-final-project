import requests
from bs4 import BeautifulSoup
import json
import pprint
import csv
import random
import time
# url = 'https://www.zillow.com/il/sold/?category=RECENT_SEARCH&searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Afalse%2C%22mapBounds%22%3A%7B%22west%22%3A-91.513079%2C%22east%22%3A-87.019935%2C%22south%22%3A36.970298%2C%22north%22%3A42.508338%7D%2C%22usersSearchTerm%22%3A%22IL%22%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A21%2C%22regionType%22%3A2%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22rs%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D'

# headers={
#   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#   'accept-encoding': 'gzip, deflate, br, zstd',
#   'accept-language': 'en-US,en;q=0.9',
#   'cache-control': 'max-age=0',
#   'cookie': 'zguid=24|%24c856be61-b78a-4401-9408-40b0b4b1ae32; zgsession=1|093eda94-522d-4f72-a99b-08309035b369; _ga=GA1.2.80188176.1764192058; _gid=GA1.2.348868539.1764192058; zjs_anonymous_id=%22c856be61-b78a-4401-9408-40b0b4b1ae32%22; zjs_user_id=null; zg_anonymous_id=%223142b4a1-c2d3-4628-a124-2f3e20d60dcf%22; pxcts=ccc55fd7-cb0d-11f0-9f03-7fc5910b3b33; _pxvid=ccc5581e-cb0d-11f0-9f03-02794babb67f; zjs_user_id_type=%22encoded_zuid%22; _gcl_au=1.1.1709024787.1764192059; datagrail_consent_id=7e84c9ce-057e-4c91-87ef-56e6d4914637.48592105-e265-4a30-8bc1-843d84ffa5d0; OptanonConsent=consentId=6457cab4-f752-45d9-80a7-0fe2afb5a1d5&datestamp=Wed%2BNov%2B26%2B2025%2B16%3A20%3A59%2BGMT-0500%2B(Eastern%2BStandard%2BTime)&version=202301.2.0&interactionCount=1&isAnonUser=1&isGpcEnabled=0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=1:1,2:1,3:1,4:1&AwaitingReconsent=false; datagrail_consent_id_s=7e84c9ce-057e-4c91-87ef-56e6d4914637.93612204-99e3-4962-bddb-8698721f026b; _scid=hgTGmmVSNpCAgL9qHQVXYrMZghw0mviY; _tt_enable_cookie=1; _ttp=01KB10N00T97NTET7XTENQ89NH_.tt.1; _fbp=fb.1.1764192059479.999416884873616629; _ScCbts=%5B%5D; DoubleClickSession=true; _sctr=1%7C1764133200000; _lr_env_src_ats=false; _pin_unauth=dWlkPVpUWmhPREF3WldZdE5tUXhOaTAwWVRjekxUZzRPV1V0TVRZMVlqTmxaakpoWVdReQ; _clck=596v77%5E2%5Eg1d%5E0%5E2156; web-platform-data=%7B%22wp-dd-rum-session%22%3A%7B%22doNotTrack%22%3Atrue%7D%7D; JSESSIONID=13A767C9D8BBE42E834CDADB2CDE5814; g_state={"i_l":0,"i_ll":1764266347210,"i_b":"qgEJQ/rLmyPOMEj4tgz8DViIbT6lpaSwX+fjO1J1Hgo"}; _rdt_uuid=1764192059270.6064135e-069e-484c-970c-7b2d33ba57ab; _scid_r=kITGmmVSNpCAgL9qHQVXYrMZghw0mviY2P1kog; tfpsi=64070dc5-a26c-4153-bfd0-3605d5e4d470; _lr_retry_request=true; __gads=ID=80a26282931d4de1:T=1764192081:RT=1764266349:S=ALNI_MZcwY2Aem8dAsoQeOpdwDzjRgujlA; __gpi=UID=000012cbc0f4d397:T=1764192081:RT=1764266349:S=ALNI_MbdUJ4gxY4ROZyYGNK-2HJULtzbcQ; __eoi=ID=58d7a331320708a0:T=1764192081:RT=1764266349:S=AA-AfjZERrQ0K07tzAAdCbqywLAB; search=6|1766858383996%7Crect%3D42.508338%2C-87.019935%2C36.970298%2C-91.513079%26rid%3D21%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26listPriceActive%3D1%26fs%3D0%26fr%3D0%26mmm%3D0%26rs%3D1%26singlestory%3D0%26housing-connector%3D0%26parking-spots%3Dnull-%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26showcase%3D0%26featuredMultiFamilyBuilding%3D0%26onlyRentalStudentHousingType%3D0%26onlyRentalIncomeRestrictedHousingType%3D0%26onlyRentalMilitaryHousingType%3D0%26onlyRentalDisabledHousingType%3D0%26onlyRentalSeniorHousingType%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%0921%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Afalse%7D%09%09%09%09%09; _px3=5f3e8a2359d445eae55e641242f68847dfc9df5d4f09bf5d198e8b8d0cae1233:WWUTP/DG2KSVdmzF1VBJ+XMPvhnt/KldDSKvkDsHWUSMzhn1Um7PvYELo1VO0J2ZkTFIu0hFhq317gJ9nIiZqg==:1000:TCjvGknRbPWuwX7zx04Gn6CbFTMHp9MQneSWv4HjrHgLy/wVrKEZ/qqwmXDqTlpL36zTFxvR5i08iOjmXBX3pRvcT3nzkGtf9qHXFid5WI4z17bcdT0m3WT/EbA1ZI4NLngcRiYa0NuLgKZeP+sw7grG9iVKq7AVVNRcJgbgD9snmQvXkJBuOj3IlhLln5p4LcpU72qrX7CgGmohRg6F1k5rBzmsXP8fM3k6bHsbRuiiJ2+KDrdlDIuOg9oDcVyZofx+XFbzhQUbizM9L3toSRo1UnwJmXl2Ljdbu+TA1NKl5FMa9BhGn6ugQw6TJ91AdFcrS/dmmGZsSjLV4ARHFc1d6qBQi0+iniZ661kS4iw=; AWSALB=C2O40lNTwJsEliKFL3oZxzAZStdSoSxKjQGHwekSLeFoGKZdq85UNu/lC91jIlo7lWyjUZhPAefwHWYxwCThhw7sxD2NeJhQ+3canja/pY2ggTQ6IlBVNMFKT+5y; AWSALBCORS=C2O40lNTwJsEliKFL3oZxzAZStdSoSxKjQGHwekSLeFoGKZdq85UNu/lC91jIlo7lWyjUZhPAefwHWYxwCThhw7sxD2NeJhQ+3canja/pY2ggTQ6IlBVNMFKT+5y; _uetsid=cd9dbca0cb0d11f08811e327b5f8d879; _uetvid=cd9de960cb0d11f089a939d7045695e5; connectId=%7B%22puid%22%3A%223eac921605d50047d6dc67eaef01aabe17073fa482a8571d08d3fcf421ff038f%22%2C%22vmuid%22%3A%22lyRQA60vtWqoI7xywOt2IFbrkwhi_PBStyHzmQy4c-6TF-QE0HO2ej0KdWgcp6t94uKlG1hupywatMN67uGChA%22%2C%22connectid%22%3A%22lyRQA60vtWqoI7xywOt2IFbrkwhi_PBStyHzmQy4c-6TF-QE0HO2ej0KdWgcp6t94uKlG1hupywatMN67uGChA%22%2C%22connectId%22%3A%22lyRQA60vtWqoI7xywOt2IFbrkwhi_PBStyHzmQy4c-6TF-QE0HO2ej0KdWgcp6t94uKlG1hupywatMN67uGChA%22%2C%22ttl%22%3A86400000%2C%22lastSynced%22%3A1764192080572%2C%22lastUsed%22%3A1764266592681%7D; ttcsid=1764266348241::LOQsBPzXCc3Ne-Pnbp-h.3.1764266592727.0; ttcsid_CN5P33RC77UF9CBTPH9G=1764266348239::o27d0bERsD0QaOm6BVj1.3.1764266592727.0; _clsk=1rmwaxx%5E1764266592948%5E8%5E0%5Ea.clarity.ms%2Fcollect; cto_bundle=kVd-iF9tZ3QyeEdsc1dhWG9xNGU2T0VBeVBrd2xqMGVRc3RvT1ZVSFREaUdOZzZkNThzdFVCNmhuSUtVTDc5UXRoak5zd3N5cjFQZzc5RUxDc0VDRXlEdWdBeHE2a1BIdXl4aWpuNSUyRjlMbFVKRUN0c0JaOGVkeWx0WW9ZWDJSN2FDSTZjUERIVmJ3bUZhb0hHaUVka1plQlAxQ2RRNFBNaW9TSmZDYnFEQU1GWmolMkY4MU9xMXl0Ym5xS0NnaXZPNlBHemRzeHh5anpVaHFlOCUyRlRXVHpTT3VsWmJUaDg4cXM5RUdTWEozNnU5ZkhRcm5hd0NXcGdVaUJ1RUNQRVFNaHpKaGNH',
#   'priority': 'u=0, i',
#   'referer': 'https://www.zillow.com/il/sold/?category=RECENT_SEARCH&searchQueryState=%7B%22isMapVisible%22%3Afalse%2C%22mapBounds%22%3A%7B%22west%22%3A-91.513079%2C%22east%22%3A-87.019935%2C%22south%22%3A36.970298%2C%22north%22%3A42.508338%7D%2C%22usersSearchTerm%22%3A%22IL%22%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A21%2C%22regionType%22%3A2%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22rs%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D',
#   'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
#   'sec-ch-ua-mobile': '?0',
#   'sec-ch-ua-platform': '"macOS"',
#   'sec-fetch-dest': 'document',
#   'sec-fetch-mode': 'navigate',
#   'sec-fetch-site': 'same-origin',
#   'sec-fetch-user': '?1',
#   'upgrade-insecure-requests': '1',
#   'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
# }

# params = {
#   'searchQueryState': '{"isMapVisible":false,"mapBounds":{"west":-91.513079,"east":-87.019935,"south":36.970298,"north":42.508338},"usersSearchTerm":"IL","regionSelection":[{"regionId":21,"regionType":2}],"filterState":{"sort":{"value":"globalrelevanceex"},"fsba":{"value":false},"fsbo":{"value":false},"nc":{"value":false},"cmsn":{"value":false},"auc":{"value":false},"fore":{"value":false},"rs":{"value":true}},"isListVisible":true}'
# }
# response = requests.get(url, headers=headers, params=params)
# print(response)


class ZillowScraper():
  headers={
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-encoding': 'gzip, deflate, br, zstd',
  'accept-language': 'en-US,en;q=0.9',
  'cache-control': 'max-age=0',
  'cookie': 'zguid=24|%24c856be61-b78a-4401-9408-40b0b4b1ae32; zgsession=1|093eda94-522d-4f72-a99b-08309035b369; _ga=GA1.2.80188176.1764192058; _gid=GA1.2.348868539.1764192058; zjs_anonymous_id=%22c856be61-b78a-4401-9408-40b0b4b1ae32%22; zjs_user_id=null; zg_anonymous_id=%223142b4a1-c2d3-4628-a124-2f3e20d60dcf%22; pxcts=ccc55fd7-cb0d-11f0-9f03-7fc5910b3b33; _pxvid=ccc5581e-cb0d-11f0-9f03-02794babb67f; zjs_user_id_type=%22encoded_zuid%22; _gcl_au=1.1.1709024787.1764192059; datagrail_consent_id=7e84c9ce-057e-4c91-87ef-56e6d4914637.48592105-e265-4a30-8bc1-843d84ffa5d0; OptanonConsent=consentId=6457cab4-f752-45d9-80a7-0fe2afb5a1d5&datestamp=Wed%2BNov%2B26%2B2025%2B16%3A20%3A59%2BGMT-0500%2B(Eastern%2BStandard%2BTime)&version=202301.2.0&interactionCount=1&isAnonUser=1&isGpcEnabled=0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=1:1,2:1,3:1,4:1&AwaitingReconsent=false; datagrail_consent_id_s=7e84c9ce-057e-4c91-87ef-56e6d4914637.93612204-99e3-4962-bddb-8698721f026b; _scid=hgTGmmVSNpCAgL9qHQVXYrMZghw0mviY; _tt_enable_cookie=1; _ttp=01KB10N00T97NTET7XTENQ89NH_.tt.1; _fbp=fb.1.1764192059479.999416884873616629; _ScCbts=%5B%5D; DoubleClickSession=true; _sctr=1%7C1764133200000; _lr_env_src_ats=false; _pin_unauth=dWlkPVpUWmhPREF3WldZdE5tUXhOaTAwWVRjekxUZzRPV1V0TVRZMVlqTmxaakpoWVdReQ; _clck=596v77%5E2%5Eg1d%5E0%5E2156; web-platform-data=%7B%22wp-dd-rum-session%22%3A%7B%22doNotTrack%22%3Atrue%7D%7D; JSESSIONID=13A767C9D8BBE42E834CDADB2CDE5814; g_state={"i_l":0,"i_ll":1764266347210,"i_b":"qgEJQ/rLmyPOMEj4tgz8DViIbT6lpaSwX+fjO1J1Hgo"}; _rdt_uuid=1764192059270.6064135e-069e-484c-970c-7b2d33ba57ab; _scid_r=kITGmmVSNpCAgL9qHQVXYrMZghw0mviY2P1kog; tfpsi=64070dc5-a26c-4153-bfd0-3605d5e4d470; _lr_retry_request=true; __gads=ID=80a26282931d4de1:T=1764192081:RT=1764266349:S=ALNI_MZcwY2Aem8dAsoQeOpdwDzjRgujlA; __gpi=UID=000012cbc0f4d397:T=1764192081:RT=1764266349:S=ALNI_MbdUJ4gxY4ROZyYGNK-2HJULtzbcQ; __eoi=ID=58d7a331320708a0:T=1764192081:RT=1764266349:S=AA-AfjZERrQ0K07tzAAdCbqywLAB; search=6|1766858383996%7Crect%3D42.508338%2C-87.019935%2C36.970298%2C-91.513079%26rid%3D21%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26listPriceActive%3D1%26fs%3D0%26fr%3D0%26mmm%3D0%26rs%3D1%26singlestory%3D0%26housing-connector%3D0%26parking-spots%3Dnull-%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26showcase%3D0%26featuredMultiFamilyBuilding%3D0%26onlyRentalStudentHousingType%3D0%26onlyRentalIncomeRestrictedHousingType%3D0%26onlyRentalMilitaryHousingType%3D0%26onlyRentalDisabledHousingType%3D0%26onlyRentalSeniorHousingType%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%0921%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Afalse%7D%09%09%09%09%09; _px3=5f3e8a2359d445eae55e641242f68847dfc9df5d4f09bf5d198e8b8d0cae1233:WWUTP/DG2KSVdmzF1VBJ+XMPvhnt/KldDSKvkDsHWUSMzhn1Um7PvYELo1VO0J2ZkTFIu0hFhq317gJ9nIiZqg==:1000:TCjvGknRbPWuwX7zx04Gn6CbFTMHp9MQneSWv4HjrHgLy/wVrKEZ/qqwmXDqTlpL36zTFxvR5i08iOjmXBX3pRvcT3nzkGtf9qHXFid5WI4z17bcdT0m3WT/EbA1ZI4NLngcRiYa0NuLgKZeP+sw7grG9iVKq7AVVNRcJgbgD9snmQvXkJBuOj3IlhLln5p4LcpU72qrX7CgGmohRg6F1k5rBzmsXP8fM3k6bHsbRuiiJ2+KDrdlDIuOg9oDcVyZofx+XFbzhQUbizM9L3toSRo1UnwJmXl2Ljdbu+TA1NKl5FMa9BhGn6ugQw6TJ91AdFcrS/dmmGZsSjLV4ARHFc1d6qBQi0+iniZ661kS4iw=; AWSALB=C2O40lNTwJsEliKFL3oZxzAZStdSoSxKjQGHwekSLeFoGKZdq85UNu/lC91jIlo7lWyjUZhPAefwHWYxwCThhw7sxD2NeJhQ+3canja/pY2ggTQ6IlBVNMFKT+5y; AWSALBCORS=C2O40lNTwJsEliKFL3oZxzAZStdSoSxKjQGHwekSLeFoGKZdq85UNu/lC91jIlo7lWyjUZhPAefwHWYxwCThhw7sxD2NeJhQ+3canja/pY2ggTQ6IlBVNMFKT+5y; _uetsid=cd9dbca0cb0d11f08811e327b5f8d879; _uetvid=cd9de960cb0d11f089a939d7045695e5; connectId=%7B%22puid%22%3A%223eac921605d50047d6dc67eaef01aabe17073fa482a8571d08d3fcf421ff038f%22%2C%22vmuid%22%3A%22lyRQA60vtWqoI7xywOt2IFbrkwhi_PBStyHzmQy4c-6TF-QE0HO2ej0KdWgcp6t94uKlG1hupywatMN67uGChA%22%2C%22connectid%22%3A%22lyRQA60vtWqoI7xywOt2IFbrkwhi_PBStyHzmQy4c-6TF-QE0HO2ej0KdWgcp6t94uKlG1hupywatMN67uGChA%22%2C%22connectId%22%3A%22lyRQA60vtWqoI7xywOt2IFbrkwhi_PBStyHzmQy4c-6TF-QE0HO2ej0KdWgcp6t94uKlG1hupywatMN67uGChA%22%2C%22ttl%22%3A86400000%2C%22lastSynced%22%3A1764192080572%2C%22lastUsed%22%3A1764266592681%7D; ttcsid=1764266348241::LOQsBPzXCc3Ne-Pnbp-h.3.1764266592727.0; ttcsid_CN5P33RC77UF9CBTPH9G=1764266348239::o27d0bERsD0QaOm6BVj1.3.1764266592727.0; _clsk=1rmwaxx%5E1764266592948%5E8%5E0%5Ea.clarity.ms%2Fcollect; cto_bundle=kVd-iF9tZ3QyeEdsc1dhWG9xNGU2T0VBeVBrd2xqMGVRc3RvT1ZVSFREaUdOZzZkNThzdFVCNmhuSUtVTDc5UXRoak5zd3N5cjFQZzc5RUxDc0VDRXlEdWdBeHE2a1BIdXl4aWpuNSUyRjlMbFVKRUN0c0JaOGVkeWx0WW9ZWDJSN2FDSTZjUERIVmJ3bUZhb0hHaUVka1plQlAxQ2RRNFBNaW9TSmZDYnFEQU1GWmolMkY4MU9xMXl0Ym5xS0NnaXZPNlBHemRzeHh5anpVaHFlOCUyRlRXVHpTT3VsWmJUaDg4cXM5RUdTWEozNnU5ZkhRcm5hd0NXcGdVaUJ1RUNQRVFNaHpKaGNH',
  'priority': 'u=0, i',
  'referer': 'https://www.zillow.com/il/sold/?category=RECENT_SEARCH&searchQueryState=%7B%22isMapVisible%22%3Afalse%2C%22mapBounds%22%3A%7B%22west%22%3A-91.513079%2C%22east%22%3A-87.019935%2C%22south%22%3A36.970298%2C%22north%22%3A42.508338%7D%2C%22usersSearchTerm%22%3A%22IL%22%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A21%2C%22regionType%22%3A2%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22rs%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D',
  'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
  }

  homes_list = []
  column_names = []

  def fetch(self, url, params=None):
    response = requests.get(url, headers=self.headers, params=params)
    print(response)
    return response
  
  def gen_dict_extract(self, key, var):
    if hasattr(var,'items'): 
        for k, v in var.items(): 
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in self.gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in self.gen_dict_extract(key, d):
                        yield result
  
  def parse(self, response):
    content = BeautifulSoup(response)
    #grab all the json
    result = content.find("script", id="__NEXT_DATA__")
    data = json.loads(result.string)
    #gen_dict_extract is a function that finds all occurences of a key in a nested dictionary.r
    for result in self.gen_dict_extract("homeInfo", data):
      #TO DO - if we navigate between pages too fast we risk getting blocked so sleep for a
      #random time for each iteration of the loop.(somewhere between 4-8 seconds?)
      sleep_time = random.uniform(5,10)
      time.sleep(sleep_time)
      #construct url string
      url_individual_home = f'https://www.zillow.com/homedetails/{result["streetAddress"].replace(" ", "-")}-{result["city"].replace(" ", "-")}-{result["state"]}-{result["zipcode"]}/{result["zpid"]}_zpid/"'
      resp = self.fetch(url_individual_home)
      content = BeautifulSoup(resp.text)
      result_indiv = content.find("script", id="__NEXT_DATA__")
      data_indiv = json.loads(result_indiv.string)
      home = json.loads(data_indiv["props"]["pageProps"]["componentProps"]["gdpClientCache"])
      listing_key = list(home.keys())[0]
      listing_data = home[listing_key]
      #adding heating, cooling, and year built
      has_heating = listing_data["property"]["resoFacts"].get("hasHeating")
      has_cooling = listing_data["property"]["resoFacts"].get("hasCooling")
      year_built = listing_data["property"]["resoFacts"].get("yearBuilt")
      result["has_heating"] = has_heating
      result["has_cooling"] = has_cooling
      result["year_built"] = year_built
      print("RESULTTTTTTTT")
      print(result)

      print("LISTING DATATAAA")
      pprint.pprint(listing_data["property"]["priceHistory"])
      #TO DO - parse listing_data["property"]["priceHistory"] for list price, sell price, list date, and sell date, and add these to result.
      # need to check event = sale and event = listed for sale and dates associated witht those events
      # list_price = listing_data["property"]["priceHistory"].get("")
      # sell_price = listing_data["property"]["priceHistory"].get("")
      # list_date = listing_data["property"]["priceHistory"].get("")
      # sell_date = listing_data["property"]["priceHistory"].get("")
      # result["list_price"] = list_price
      # result["sell_price"] = sell_price
      # result["list_date"] = list_date
      # result["sell_date"] = sell_date

      self.homes_list.append(result)
      break #TO DO - remove this break after we are sure one example is working. Also after the random sleeping is implemented

  def convert_to_csv(self, column_names, homes_list):
     #TO DO: convert the homes_list to df to csv.
     with open('zillow_homes.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(column_names)
        csv_writer.writerows(homes_list)
     pass
  
  def run(self):
    url = 'https://www.zillow.com/il/sold/?category=RECENT_SEARCH&searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Afalse%2C%22mapBounds%22%3A%7B%22west%22%3A-91.513079%2C%22east%22%3A-87.019935%2C%22south%22%3A36.970298%2C%22north%22%3A42.508338%7D%2C%22usersSearchTerm%22%3A%22IL%22%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A21%2C%22regionType%22%3A2%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22rs%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D'
    params = {
      'searchQueryState': '{"isMapVisible":false,"mapBounds":{"west":-91.513079,"east":-87.019935,"south":36.970298,"north":42.508338},"usersSearchTerm":"IL","regionSelection":[{"regionId":21,"regionType":2}],"filterState":{"sort":{"value":"globalrelevanceex"},"fsba":{"value":false},"fsbo":{"value":false},"nc":{"value":false},"cmsn":{"value":false},"auc":{"value":false},"fore":{"value":false},"rs":{"value":true}},"isListVisible":true}'
    }
    res = self.fetch(url, params)
    self.parse(res.text)

if __name__ == '__main__':
  scraper = ZillowScraper()
  scraper.run()