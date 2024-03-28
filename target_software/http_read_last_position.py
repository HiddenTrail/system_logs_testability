import requests
import time

def read_new_data_with_range(url, last_byte_position):

    headers = {"Range": f"bytes={last_byte_position}-"}
    response = requests.get(url, headers=headers)
    new_data = response.content.decode("utf-8")
    new_last_byte_position = last_byte_position + len(new_data)

    return new_data, new_last_byte_position

# Esimerkkinä käytämme URLia ja aloitamme lukemisen tiedoston alusta
url = "http://localhost:8000/httpserver.log"
initial_position = 0

# Lue uudet tiedot
new_data, new_position = read_new_data_with_range(url, initial_position)
print("vanha data -----------------")
print(new_data)

print("sleeping 30 sec")
time.sleep(30)
print("done sleeping")

# Oletetaan, että myöhemmin teet toisen pyynnön
new_data, new_position2 = read_new_data_with_range(url, new_position)
print("uusi data ------------------")
print(new_data)

# This works with Nginx, Node.js http-server

# Does not work with Python http-server
