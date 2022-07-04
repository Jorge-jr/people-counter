import matplotlib.pyplot as plt

labels = ["0.5 second", "1 second"]


with open("halfXonedAndHalf") as file:

	half_second, one_second = 0, 0

	for line in file:
		try:
			if line.split(" ")[2] == "kali-pi-2":
				half_second += 1
			elif line.split(" ")[2] == "kali-pi-4":
				one_second += 1
			else:
				print(line.split(" ")[2][2])
		except:
			print(line.split(" ")[2][2])
	
print(half_second)
print(one_second)
"""fig = plt.figure(figsize =(10, 7)) 
plt.pie([half_second, one_second], labels=labels) 
plt.show() """
