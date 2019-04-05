import datetime

time=datetime.datetime.today().strftime("%H-%M-%S")

text_file = open("/home/pi/TutorCal/CRONtest/"+time+".txt", "w")
text_file.write("Hello world!")
text_file.close()