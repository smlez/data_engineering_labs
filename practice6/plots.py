import seaborn as sns
from matplotlib import pyplot as plt


def stepped(data, x, y, name):
	plt.title(name)
	sns.stripplot(data=data.sample(1000), x=x, y=y, dodge=True)
	plt.savefig(f"graphics/{name}.png")
	plt.close()
	
def box(data, x, y, name):
	sns.boxplot(data=data.sample(1000), x=x, y=y)
	plt.savefig(f"graphics/{name}.png")
	plt.close()
	
def linear(data, x, y, name):
	plt.title(name)
	sns.lineplot(data=data.sample(1000), x=x, y=y, errorbar=None)
	plt.savefig(f"graphics/{name}.png")
	plt.close()

def histogram(data, x, y, name):
	sns.histplot(data=data.sample(1000), x=x, y=y)
	plt.savefig(f"graphics/{name}.png")
	plt.close()