from libs.LogSlicer import LogSlicer

url = "http://localhost:8000/httpserver.log"
log_slicer = LogSlicer()
log_slicer.add_url(url)

data = log_slicer.get_data(url)
#print("old data:")
#print(data)

# print("sleeping 30 sec")
# time.sleep(30)
# print("done sleeping")
#
# data2 = log_slicer.get_data(url)
# print("new data:")
# print(data2)
