import requests

def trigger_red_for_element(element_id):
    url = f"http://127.0.0.1:5000/trigger-red/{element_id}"
    response = requests.post(url)
    if response.status_code == 200:
        print(f"Triggered red for {element_id}.")
    else:
        print(f"Failed to trigger for {element_id}.")

if __name__ == "__main__":
    trigger_red_for_element("circle1")  # Example: ID 'circle1'
