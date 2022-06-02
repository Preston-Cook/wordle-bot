import re
from datetime import datetime

import requests

js_data = requests.get('https://www.nytimes.com/games/wordle/main.9622bc55.js').text

answers = re.search(r"(?<=var ko=\[).*?(?=\])",js_data,re.DOTALL).group().replace('"','')

words = answers.split(',')

start_date = datetime.strptime('1/6/2022',"%d/%m/%Y").date()
current_date = datetime.now().date()
diff = current_date - start_date

starting_index = words.index('creak')

solution = words[starting_index + diff.days]