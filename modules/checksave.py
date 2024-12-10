import pprint
import pickle
file = 'save/sauvegarde.pkl'
file = open(file, 'rb')
data = pickle.load(file)
pprint.pprint(data)
file.close()
