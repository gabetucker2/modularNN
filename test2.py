import requests

def trigger_red_for_element(element_id):
    url = f"http://127.0.0.1:5000/trigger-red/{element_id}"
    response = requests.post(url)
    if response.status_code == 200:
        print(f"Triggered red for {element_id}.")
    else:
        print(f"Failed to trigger for {element_id}.")

if __name__ == "__main__":
    # Example: Trigger red for a specific circle or line
    trigger_red_for_element("circle_0_1")  # Circle in the first row, second column
    # trigger_red_for_element("line_circle_0_1_to_circle_1_2")  # Line from circle_0_1 to circle_1_2
