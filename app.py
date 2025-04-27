from flask import Flask, render_template ,request,redirect, url_for
from bs4 import BeautifulSoup 
import requests
import os
import csv
from datetime import datetime
app = Flask(__name__)

@app.route('/', methods=['GET'])
def get():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def post():
    url = request.form.get('url')
    tag = request.form.get('tag')
    return redirect(url_for('scrap', url=url , tag =tag))

@app.route('/scrap')
def scrap():
    # Get the URL from the request arguments
    url = request.args.get('url')
    tag = request.args.get('tag')
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
    
    try:
        response = requests.get(url,headers=headers)
        if response.status_code != 200:
            return render_template('result.html', 
                                error=f"Failed to access the URL. Status code: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all(tag)
        
        count = len(data)

        # Save to txt file
        os.makedirs("data", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename1 = f"data/scrapped_{timestamp}.txt" 
        filename2 = f"data/scrapped_{timestamp}.csv"
        with open(filename1, 'w', encoding='utf-8') as file:
          for element in data:
                    text = element.get_text(strip=True)
                    if text:
                        file.write(text + "\n\n")
        #  write in csv 
        with open(filename2, 'w', newline='', encoding='utf-8') as file:
          writer = csv.writer(file)
          writer.writerow(['URL', 'Tag', 'Content'])
          for element in data:
            text = element.get_text(strip=True)
            if text:
              writer.writerow([url, tag, text]) 


        return render_template('result.html', data=data, url=url, count=count)
    except Exception as e:
        return render_template('result.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)