import time

end_timer = time.time() + 10
i = 0

while time.time()<end_timer:
    i += 1

print(i)
