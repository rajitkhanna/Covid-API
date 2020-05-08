#!/usr/bin/env python3

# RETRIEVING THE DATA
# from pprint import pprint
# myfile = open("Hospitalization_Data.csv")
# myfile.readline()
# data = [line.strip().split(',') for line in myfile.readlines() if line.strip().split(',')[0] != ""]
# data = data[ : 24]
# myfile.close()

# myfile = open("Hospitalization_Data.csv")
# myfile.readline()
# line_count = 0
# data_dict = {}
# for line in myfile.readlines():
#     if line_count == 23: break
#     line = line.strip().split(',')
#     if line[0] == '': continue
#     data_dict[line[0].split(' (')[0]] = (float(line[1]), float(line[2]))
#     line_count += 1
# myfile.close()
# pprint(data_dict)

mapping = {
    '0–9 years': (0.01, 0.99),
    '10–19 years': (0.0408, 0.959),
    '20–29 years': (0.0104, 0.99),
    '30–39 years': (0.0343, 0.966),
    '40–49 years': (0.0425, 0.958),
    '50–59 years': (0.0816, 0.918),
    '60–69 years': (0.118, 0.882),
    '70–79 years': (0.166, 0.834),
    'Cardiovascular disease': (0.202, 0.046),
    'Chronic liver disease': (0.008, 0.005),
    'Chronic lung disease': (0.145, 0.071),
    'Chronic renal disease': (0.08, 0.01),
    'Control': (0.836, 0.164),
    'Current smoker': (0.017, 0.012),
    'Former smoker': (0.042, 0.016),
    'Diabetes mellitus': (0.224, 0.064),
    'Immunocompromised condition': (0.061, 0.027),
    'Neurologic disorder/Intellectual disability': (0.017, 0.003),
    'None of the above conditions': (0.354, 0.73),
    'One or more conditions': (0.646, 0.27),
    'Other chronic disease': (0.297, 0.113),
    'Pregnant': (0.035, 0.014),
    '≥80 years': (0.184, 0.816)
}

condition_list = [
    'Cardiovascular disease',
    'Chronic liver disease',
    'Chronic lung disease',
    'Chronic renal disease',
    'Current smoker',
    'Former smoker',
    'Diabetes mellitus',
    'Immunocompromised condition',
    'Neurologic disorder/Intellectual disability',
    'Other chronic disease',
    'Pregnant'
    ]

class Naive_Bayes:
    def __init__(self, age, condition_list = []):
        self.age = age
        self.condition = condition_list
        if not self.condition:
            self.condition.append('None of the above conditions')
        else: self.condition.append('One or more conditions')
        self.age_helper()

    def get_probability(self):
        probability = self.get_prior_prob(True) * self.get_posterior_prob(True) / self.get_evidence()
        return int(probability * 100)

    def get_prior_prob(self, key):
        yes, no = mapping["Control"]
        return yes if key else no
    
    def get_posterior_prob(self, key):
        posterior_prob = 1.0
        for condition in self.condition:
            posterior_prob *= mapping[condition][not key]
        return posterior_prob

    def get_evidence(self):
        return self.get_prior_prob(True)*self.get_posterior_prob(True) + self.get_prior_prob(False)*self.get_posterior_prob(False)

    def age_helper(self):
        if self.age >= 80:
            self.condition.append('≥80 years')
        elif self.age >= 70:
            self.condition.append('70–79 years')
        elif self.age >= 60:
            self.condition.append('60–69 years')
        elif self.age >= 50:
            self.condition.append('50–59 years')
        elif self.age >= 40:
            self.condition.append('40–49 years')
        elif self.age >= 30:
            self.condition.append('30–39 years')
        elif self.age >= 20:
            self.condition.append('20–29 years')
        elif self.age >= 10:
            self.condition.append('10–19 years')
        else:
            self.condition.append('0–9 years')