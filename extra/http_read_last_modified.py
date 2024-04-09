import requests
import time

def check_and_read_if_modified(url, last_modified=None):

    headers = {}
    if last_modified:
        headers["If-Modified-Since"] = last_modified

    response = requests.get(url, headers=headers)

    if response.status_code == 304:
        print("Tiedosto ei ole muuttunut.")
        return None, last_modified
    else:
        print("Uutta dataa on saatavilla:")
        new_data = response.content.decode("utf-8")
        new_last_modified = response.headers.get("Last-Modified", last_modified)

        return new_data, new_last_modified

# Esimerkkinä käytämme URLia ja ensimmäistä pyyntöä ilman Last-Modified -otsaketta
url = "http://localhost:8000/httpserver.log"

# Tee pyyntö ja tulosta uudet tiedot, jos niitä on
new_data, last_modified = check_and_read_if_modified(url)
if new_data:
    print(new_data)

print("sleeping 30 sec")
time.sleep(30)
print("done sleeping")

# Oletetaan, että myöhemmin teet toisen pyynnön
# Käytä last_modified arvoa, jotta tiedät, onko tiedosto muuttunut
new_data, last_modified = check_and_read_if_modified(url, last_modified)
if new_data:
    print(new_data)



#
# kokeile sitä javascript-serveriä jos se tukee, tai googleta että mikä tukee
#