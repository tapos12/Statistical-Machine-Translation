"""Author: Touhidul Alam (3293940)"""
from collections import defaultdict

class EM():
	def __init__(self, translationProb, translationCounts, EngCorpus, foreignCorpus, total):
		self.translationProb = translationProb
		self.translationCounts = translationCounts
		self.EngCorpus = EngCorpus
		self.foreignCorpus = foreignCorpus
		self.total = total

	def readFile(self, filename):
		raw_data = open(filename)
		data_lines = raw_data.read().split('\n')
		raw_data.close()

		i = 1
		foreignLine = []
		englishLine = []
		for line in data_lines:
			if i%2!=0:
				englishLine = line.split(" ")
				self.EngCorpus.append(line)
			else:
				foreignLine = line.split(" ")
				self.foreignCorpus.append(line)

				for item in foreignLine:
					if item not in self.translationProb:
						self.translationProb[item] = {}
						self.translationCounts[item] = {}
						self.total[item] = 0.0

					for item2 in englishLine:
						self.translationProb[item].update({item2: 0.0})
						self.translationCounts[item].update({item2: 0.0})
			i+=1

	def initializeTranslationProb(self):
		#print("")
		for item in self.translationProb:
			dictProbsForF = self.translationProb.get(item)
			numTranslations = len(dictProbsForF)

			for item2 in dictProbsForF:
				dictProbsForF[item2] = 1.0/numTranslations

	def computeTranslationProb(self):
		english = set()
		foreign = set()
		for line in self.EngCorpus:
			eng = line.split(" ")
			english.update(eng)
		for line in self.foreignCorpus:
			forgn = line.split(" ")
			foreign.update(forgn)
		for item2 in foreign:
			for item in english:
				if item in (self.translationProb[item2]):
					self.translationProb[item2][item] = self.translationCounts[item2][item] / self.total[item2]

	def computeCountsAndTotals(self):
		for eng, forgn in zip(self.EngCorpus, self.foreignCorpus):
			total_s = defaultdict(lambda:0)
			english = eng.split(" ")
			foreign = forgn.split(" ")
			for item in english:
				for item2 in foreign:
					#print(self.translationProb[item2])
					total_s[item] += (self.translationProb[item2][item])
			for item in english:
				for item2 in foreign:
					self.translationCounts[item2][item] += self.translationProb[item2][item] / total_s[item]
					self.total[item2] += self.translationProb[item2][item] / total_s[item]

	
	def main(self):
		self.readFile('ParallelSample.txt')
		noOfIterations = 1000
		#print(self.total)
		#print(self.translationProb)
		#print(self.translationCounts)
		#print(self.EngCorpus)
		#print(self.foreignCorpus)
		self.initializeTranslationProb()
		for i in range(0, noOfIterations):
			self.computeCountsAndTotals()
			#print(self.translationProb)
			self.computeTranslationProb()
			#print(self.translationProb)
			#print("----final-----")
		print(self.translationProb)


if __name__ == "__main__":
	translationProb = {}
	translationCounts = {}
	total = {}
	EngCorpus = []
	foreignCorpus = []
	EM(translationProb, translationCounts, EngCorpus, foreignCorpus, total).main()