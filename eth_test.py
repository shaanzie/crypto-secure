import pandas as pd
import sys

class Parser:

    def __init__(self) -> None:
        
        super().__init__()

    def read_data(self, json_file):

        self.eth_df = pd.read_json(json_file)
        self.eth_df = pd.DataFrame(list(self.eth_df['result']))
        self.eth_df = self.eth_df[self.eth_df.value.apply(lambda x: x.isnumeric())]
        return self.eth_df

if __name__ == '__main__':

    filename = r'D:\Code\CSE891\Project\eth_transactions.json'

    parser = Parser()
    df = parser.read_data(filename)