import requests
import json
import time

API_URL = "https://api.lumalabs.ai/dream-machine/v1/generations"
API_KEY = ""  # Replace with your actual API key

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    
    "prompt": """Generate a 7-second video of a futuristic city at sunset. Skyscrapers glow with neon lights, and flying cars zip through the skyline. 
    A figure in a tech suit stands on a rooftop, gazing over the city as the camera pans. 
    Electronic music sets a futuristic vibe.""",

    "num_frames": 60,
    "resolution": "1080p",
    "fps": 30,
    "style": "cinematic",
}

try:
    #generation request
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload), timeout=10)
    response.raise_for_status()  # Raises an exception for 4xx/5xx responses

    # parsing the response JSON to get the job ID
    result = response.json()
    print("Request sent successfully!")
    print(result)

    job_id = result['id']  # Use the ID from the response

    # status of the job
    status_url = f"https://api.lumalabs.ai/dream-machine/v1/generations/{job_id}"

    while True:
        status_response = requests.get(status_url, headers=headers)
        status_response.raise_for_status()

        status_result = status_response.json()
        print(f"Current Status: {status_result['state']}")

        if status_result['state'] == "completed":
            print("Video generation completed!")
            download_url = status_result['assets']['video']  # Access the video URL
            video_response = requests.get(download_url)

            # saving the video file
            with open("generated_video.mp4", "wb") as f:
                f.write(video_response.content)

            print("Video downloaded successfully!")
            break
        elif status_result['state'] == "failed":
            print("Video generation failed.")
            break

        time.sleep(10)  # Wait before checking again

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
