import matplotlib.pyplot as plt

class analyze_PIUMet_data(object):

	def __init__(self, w_range, beta_range, mu_range, total_peaks):
		
		self.border = len(w_range)*len(beta_range)
		print self.border, len(total_peaks)
		for i in range(0, len(total_peaks), self.border):
			peaks_to_plot = total_peaks[i:i+len(mu_range)]
			print i, peaks_to_plot
			self.make_plots(mu_range, peaks_to_plot)


	def make_plots(self, mu_range, peaks_to_plot):
			""" Makes a plot of peaks against mu's for fixed value of beta and w """

			plt.plot(mu_range, peaks_to_plot, label = "Number of Total peaks")
			#plt.plot(mu_range, HMDB_peaks, label = "Number of HMDB peaks")
			#plt.plot(mu_range, PPMI_peaks, label = "Number of PPMi peaks")
			plt.xlabel("Mu")
			plt.ylim([0, 10])
			plt.legend(loc = 'best')
			plt.title("Total peaks vs Mu")

			plt.show()
