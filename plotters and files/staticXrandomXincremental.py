import matplotlib.pyplot as plt

labels = ["random hopping", "incremental hopping", "Static channel"]


with open("staticXrandomXincremental") as file:

	static, incremental, random = 0, 0, 0

	for line in file:
		try:
			if line.split(" ")[2] == "kali-pi-1":
				static += 1
			elif line.split(" ")[2] == "kali-pi-4":
				incremental += 1
			elif line.split(" ")[2] == "kali-pi-2":
				random += 1
			else:
				print(line.split(" ")[2][2])
		except:
			print(line.split(" ")[2][2])
	
print(static)
print(random)
print(incremental)
fig = plt.figure(figsize =(10, 7)) 
plt.pie([random, incremental, static], labels=labels) 
plt.show() 
