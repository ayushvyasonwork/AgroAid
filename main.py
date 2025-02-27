import sys
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyByno6CfZaIhX5k4sWDj8akzNWsMZwxqtg"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

def generate_response(data):
    # Modify the prompt template to include the fetched data
    prompt_template = f"I am a farmer and you act as a scientist {data}. According to this data provide me with the most suitable crops as a list that can be grown on soil in the Indian subcontinent. Also tell that crop which is must to give good yield with a proper reason."
    # Generate the response using the modified prompt
    response = model.generate_content(prompt_template)
    return response.text

def beautify_response(response):
    # Add HTML formatting to the response
    beautified_response = "<p>"
    lines = response.split("\n")
    for line in lines:
        if line.startswith("* **"):
            beautified_response += f"<h2>{line.strip()}</h2>"
        elif line.startswith("**"):
            beautified_response += f"<h1>{line.strip()}</h1><br>"
        else:
            beautified_response += f"{line.strip()}<br>"
    beautified_response += "</p>"
     # Remove '*' characters from the response
    beautified_response = beautified_response.replace('*', '')
    return beautified_response

if __name__ == "__main__":
    data = sys.argv[1]
    response = generate_response(data)
    beautified_response = beautify_response(response)
    print(beautified_response)
