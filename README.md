## Instructions
1- Install Python >3.8

2- Install virtual environmet

python3 -m venv venv_etsy

3- Activate virtual environment

source ./venv_etsy/bin/activate

4- Install dependencies

pip install -r requirements.txt

<!-- You can ignore the dependency error during pip install -->

5- Run server

uvicorn api:app --reload

6- Launch browser with link: http://127.0.0.1:8000

7- Make sure you are logged into Etsy (with the account relevant to the API used)

8- Upload CSV file containing data in similar format as in the example CSV file ./csv_files/etsy-list.csv (Choose file + click "Upload")

9- Click on "Update transactions" button

10- On the Etsy "An application would like to connect to your account." page, click on "Grant Access"

## Etsy Apps area
https://www.etsy.com/developers/your-apps

### Reference

<!-- API endpoints -->
https://www.etsy.com/developers/documentation/reference/receipt

https://developers.etsy.com/documentation/tutorials/fulfillment