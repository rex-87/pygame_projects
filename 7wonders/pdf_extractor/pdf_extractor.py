# create logger
import MyLogging
LOG, handle_retval_and_log = MyLogging.CreateLogger("poppler_test")

try:

	# standard imports
	import os
	import subprocess
	import numpy as np
	
	# custom imports
	import Misc
	
	# helpful folders
	ThisFolder = os.path.dirname(os.path.realpath(__file__))	
	TopFolder = os.path.dirname(ThisFolder)	
	
	# change working directory
	os.chdir(TopFolder)
	
	# paths
	PdfSrcPath = r'raw\7Wonders-CardsList-EN.pdf'
	if not os.path.exists('proc'):
		os.makedirs('proc')
	HtmlDstPath = PdfSrcPath.replace('raw', 'proc').replace("pdf", "html")
	
	
	# extract words with associated bounding box from pdf
	subprocess.check_output = handle_retval_and_log(subprocess.check_output) # logging decorator
	# subprocess.check_output([r"poppler-0.68.0\bin\pdftotext.exe", "-bbox", PdfSrcPath, HtmlDstPath])
	subprocess.check_output([r"poppler-0.68.0\bin\pdfimages.exe", "-png", PdfSrcPath, r'proc\image-root'])
	# with open(r'proc\pdfimages_list.txt', 'w') as fout:
		# fout.write(
			# subprocess.check_output(
				# [r"poppler-0.68.0\bin\pdfimages.exe", "-list", PdfSrcPath]
			# ).decode()
		# )
	# subprocess.check_output([r"poppler-0.68.0\bin\pdftohtml.exe", "-xml", PdfSrcPath, r'proc\7wonders_card.xml'])
	# subprocess.check_output([r"poppler-0.68.0\bin\pdftocairo.exe", "-jpeg", "-r", "900", PdfSrcPath, r'proc\7wonders_cards.jpg'])
	# subprocess.check_output([r'poppler-0.68.0\bin\pdftocairo.exe -png -f 1 -l 1 -x 172 -y 484 -W 196 -H 83 raw\7Wonders-CardsList-EN.pdf'])
	
	# 150 dpi
	# x_ar = np.linspace(172, 872, 4)
	# y_ar = np.linspace(484, 1305, 10)
	
	# 900 dpi
	# x_ar = np.linspace(1035, 5234, 4)
	# y_ar = np.linspace(2904, 7831, 10)
	# for x in x_ar:
		# for y in y_ar:
			# x_str = str(int(round(x)))
			# y_str = str(int(round(y)))
			# subprocess.check_output([
				# r'poppler-0.68.0\bin\pdftocairo.exe',
				# '-jpeg',
				# '-r',
				# '900',
				# '-x',
				# x_str,
				# '-y',
				# y_str,
				# '-W',
				# '1171',
				# '-H',
				# '498',
				# r'raw\7Wonders-CardsList-EN.pdf',
				# r'proc\7wonders-card-{}-{}'.format(x_str, y_str),
			# ])

except:

	# log exceptions as errors
	LOG.error("Something went wrong! Exception details:\n{}".format(Misc.GetExceptionText()))
	
finally:
	
	# exit gracefully
	LOG.debug("END of {}".format(__name__))
		