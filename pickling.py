from pattern.web import *
import pickle

def get_text(url):
	""" Fetch the text of a webpage. """
	url = ""
	full_text = URL('url').download

	file_name = "Mabinogion"
	f = open(file_name, 'w')
	f.write(full_text)
	f.close()
	print 'done'

	h = {}
	for w in full_text.split():
		h[w] = h.get(w, 0) + 1

	mess = pickle.dumps(h)

	hist_file_name = "histogram" + file_name + ".pickle"
	f2 = open(hist_file_name, 'w')
	f2.write(mess)
	f2.close()

#	f3 = open(hist_file_name,'r')
#	histogram = pickle.loads(f3.read())
#	f3.close()

get_text("http://www.gutenberg.org/files/5160/5160-0.txt")