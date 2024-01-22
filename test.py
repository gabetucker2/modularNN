import requests

def manual_trigger():
    response = requests.post('http://127.0.0.1:5000/trigger')
    if response.status_code == 200:
        print("Webpage trigger activated.")
    else:
        print("Failed to activate the trigger.")

if __name__ == "__main__":
    manual_trigger()
