import matplotlib.pyplot as plt

# {'graniczące M\npobliskie S': 100, 'graniczące M\nwszystkie S': 150, 'wszystkie M\nwszystkie S': 92}
data100 = {'sposób 1': 100, 'sposób 2': 150, 'sposób 3': 92}
labels = list(data100.keys())
values = list(data100.values())

fig = plt.figure(figsize = (10, 5))

plt.subplot(1, 2, 1)
plt.bar(labels, values, color ='maroon', width = 0.4)
plt.ylabel("średnia ilość FPS")
plt.title("rozmiar próby: 100")

data400 = {'sposób 1': 9, 'sposób 2': 17, 'sposób 3': 11}
labels = list(data400.keys())
values = list(data400.values())

plt.subplot(1, 2, 2)
plt.bar(labels, values, width = 0.4)
plt.ylabel("średnia ilość FPS")
plt.title("rozmiar próby: 400")
plt.show()

#na 10 000 klatek