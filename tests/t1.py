from datetime import datetime
time1 = datetime.now()
print(time1)
while (datetime.now() - time1).seconds < 5:
    print("sleep")
print("exec")