import requests
web = requests.get('https://script.google.com/macros/s/AKfycbz09PI8QP2df6CCvRNcSbQxFxDMGpbKmkujqDOvkmfH2cvWFtkT9uWW_ucQNGxuhIzT3A/exec')
print(web.json())
