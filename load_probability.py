import requests
from pprint import pprint
class ProbabilityManager:
    def __init__(self):
        url = "https://covidtracking.com/api/v1/states/current.json"
        r = requests.get(url)
        data = r.json()

        self.total_cases, self.num_hospitalized = [], []
        for state_dict in data:
            try:
                self.num_hospitalized.append(int(state_dict['hospitalizedCumulative']))
                self.total_cases.append((state_dict['state'], int(state_dict['positive'])))
            except:
                continue
        assert(len(self.num_hospitalized) == len(self.total_cases))

    def get_control(self):
        probability = sum(self.num_hospitalized) / sum([total_cases for state, total_cases in self.total_cases])
        return {
            'Control': (probability, 1 - probability)
        }
    
    def get_statewide(self):
        probability_list = [self.num_hospitalized[i] / self.total_cases[i][1] for i in range(len(self.total_cases))]
        probability_dict = {self.total_cases[i][0]: (probability_list[i], 1 - probability_list[i]) for i in range(len(self.total_cases))}
        return probability_dict