from pandas import DataFrame


class DataAnalyzer:
    def __init__(self):
        pass

    def write(self, data):
        df = DataFrame(data, columns=data.keys())
        df.to_excel('sim_out.xlsx', index=False, header=True)


if __name__ == "__main__":
    obj = DataAnalyzer()
    data = {'Product': ['Desktop Computer', 'Printer', 'Tablet', 'Monitor'],
            'Price': [1200, 150, 300, 450]
            }
    obj.write(data)
