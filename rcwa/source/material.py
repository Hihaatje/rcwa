import context
import csv
import numpy as np
import pandas as pd
from shorthand import *

class Material:
	"""
	Material class for defining materials permittivity / permeability / refractive index as a function of wavelength / angle.

	:param filename: File containing n/k data for the material in question
	"""

	def __init__(self, filename):
		self.name = ''
		self.wavelengths = np.array([])
		self.nkData = complexArray([])
		self.erData = complexArray([])
		self.urData = complexArray([])

		self.parseCSV(filename)

	"""
	Parses data from a CSV file into a set of numpy arrays.

	:param filename: File containing n/k data for material in question
	"""
	def parseCSV(self, filename):

		data = pd.read_csv(filename, skiprows=1)
		self.wavelengths = data['Wavelength (um)'].to_numpy()
		self.nkData = (data['n'] + 1j*data['k']).to_numpy()

		self.dataSize = len(self.nkData)
		self.erData = sq(self.nkData)
		self.urData = np.ones(self.dataSize)

	def n(self, wavelength):
		indexOfWavelength = np.searchsorted(self.wavelengths, wavelength)

		if wavelength > self.wavelengths[-1]:
			print(f"CAUTION - EXTRAPOLATING INDEX LINEARLY FOR WAVELENGTH {wavelength}." + \
					f"Closest wavelength is {self.wavelengths[-1]}")

			slope = (self.nkData[-1] - self.nkData[-2]) / (self.wavelengths[-1] - self.wavelengths[-2])
			deltaWavelength = wavelength - self.wavelengths[-1]
			return self.nkData[-1] + slope * deltaWavelength

		elif wavelength < self.wavelengths[0]:
			print(f"CAUTION - EXTRAPOLATING INDEX FOR WAVELENGTH {wavelength}. Closest wavelength is " + \
					f'{self.wavelengths[-1]}')
			slope = (self.nkData[1] - self.nkData[0]) / (self.wavelengths[1] - self.wavelengths[0])
			deltaWavelength = self.wavelengths[0] - wavelength
			return self.nkData[0] - slope * deltaWavelength
		else:
			if wavelength == self.wavelengths[indexOfWavelength]:
				return self.nkData[indexOfWavelength]
			else:
				return self.nkData[indexOfWavelength - 1]


	def er(self, wavelength):
		indexOfWavelength = np.searchsorted(self.wavelengths, wavelength)

		if wavelength > self.wavelengths[-1]:
			print(f"CAUTION - EXTRAPOLATING INDEX LINEARLY FOR WAVELENGTH {wavelength}." + \
					f"Closest wavelength is {self.wavelengths[-1]}")
			slope = (self.erData[-1] - self.erData[-2]) / (self.wavelengths[-1] - self.wavelengths[-2])
			deltaWavelength = wavelength - self.wavelengths[-1]
			return self.erData[-1] + slope * deltaWavelength
		elif wavelength < self.wavelengths[0]:
			print(f"CAUTION - EXTRAPOLATING INDEX FOR WAVELENGTH {wavelength}. Closest wavelength is " + \
					f'{self.wavelengths[-1]}')
			slope = (self.erData[1] - self.erData[0]) / (self.wavelengths[1] - self.wavelengths[0])
			deltaWavelength = self.wavelengths[0] - wavelength
			return self.erData[0] - slope * deltaWavelength
		else:
			if wavelength == self.wavelengths[indexOfWavelength]:
				return self.erData[indexOfWavelength]
			else:
				return self.erData[indexOfWavelength - 1]

	def ur(self, wavelength):
		indexOfWavelength = np.searchsorted(self.wavelengths, wavelength)

		if wavelength > self.wavelengths[-1]:
			print(f"CAUTION - EXTRAPOLATING PERMEABILITY LINEARLY FOR WAVELENGTH {wavelength}." + \
					f"Closest wavelength is {self.wavelengths[-1]}")
			slope = (self.urData[-1] - self.urData[-2]) / (self.wavelengths[-1] - self.wavelengths[-2])
			deltaWavelength = wavelength - self.wavelengths[-1]
			return self.urData[-1] + slope * deltaWavelength

		elif wavelength < self.wavelengths[0]:
			print(f"CAUTION - EXTRAPOLATING PERMEABILITY FOR WAVELENGTH {wavelength}. Closest wavelength is " + \
					f'{self.wavelengths[-1]}')
			slope = (self.urData[1] - self.urData[0]) / (self.wavelengths[1] - self.wavelengths[0])
			deltaWavelength = self.wavelengths[0] - wavelength
			return self.urData[0] - slope * deltaWavelength
		else:
			if wavelength == self.wavelengths[indexOfWavelength]:
				return self.urData[indexOfWavelength]
			else:
				return self.urData[indexOfWavelength - 1]
