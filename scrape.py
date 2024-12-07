from datetime import datetime
import requests
import os
from dotenv import load_dotenv


# load environment variables
load_dotenv()
api_url = os.environ.get('API_REVIEW')


DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9"
}


def main():
    res = requests.get(api_url, headers=headers)

    updated_at = datetime.now().strftime(DATE_FORMAT + ' ' + TIME_FORMAT)
        
    # get the review data 
    # convert it to csv line
    if res.ok:
        data = res.json()
        people = data['results']
        if len(people) > 0:
            person = people[0]
            try:
                name = person['name']['first']
                gender = person['gender']
                country = person['location']['country']
                email = person['email']
                age = person['dob']['age']
                newline = f'{updated_at}, {name}, {email}, {gender}, {age}, {country}'
            except Exception as e:
                newline = f'{updated_at}, {repr(e)}'
        else:
            newline = f'{updated_at}, no people found'
    else:
        newline = f'{updated_at}, status={res.status_code}'
    
    
    with open('data.csv', 'r+') as f:
        lines = f.readlines()
        lines.append(newline)
        # bring pointer to start
        f.seek(0)
        # update the dates
        f.write('\n'.join([line.strip() for line in lines]))
        f.truncate()


main()