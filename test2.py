import requests

def trigger_red_color():
    response = requests.post('http://127.0.0.1:5000/trigger-red')
    if response.status_code == 200:
        print("Circles turned red.")
    else:
        print("Failed to trigger red color.")

if __name__ == "__main__":
    trigger_red_color()
