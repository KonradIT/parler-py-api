import datetime
import matplotlib.pyplot as plt
import json

filename = "data/stopthesteal_3_days.pretty.json"

with open(filename, "r") as posts:
	posts = json.loads(posts.read())
	print(len(posts))
	posts.reverse()
	x = [datetime.datetime.strptime(i.get("CreatedAt"), '%Y%m%d%H%M%S') for i in posts]
	y = [i for i,_ in enumerate(x)]

	# plot
	plt.plot(x,y)
	plt.gcf().autofmt_xdate()

	plt.show()