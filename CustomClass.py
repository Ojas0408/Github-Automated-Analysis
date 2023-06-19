import openai
import requests
from dataclasses import dataclass
from urllib.parse import urlparse
from nltk.tokenize import word_tokenize
import tkinter as tk

access_token = "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"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/vnd.github.v3+json"
}

openai.api_key = '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'


@dataclass
class GitHubUser:
    giturl: str


def validate_url(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme and parsed_url.netloc


def fetch_user_repositories(giturl):
    # Validate the giturl parameter
    if not isinstance(giturl, str):
        raise ValueError("giturl parameter must be a string")

    # Validate the URL
    if not validate_url(giturl):
        raise ValueError("Invalid URL format")

    # Extract the username from the GitHub user URL
    username = giturl.split("/")[-1]

    # Fetch the user repositories using the GitHub API
    api_url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(api_url, timeout=10, headers=headers)

    # Check if the request was successful
    response.raise_for_status()

    # Get the repositories from the response
    repositories = response.json()

    # Return the repositories
    return repositories


# Function to generate GPT-3.5 response using OpenAI API
def generate_gpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    return response.choices[0].text.strip()


def analyze_repositories():
    # Take GitHub user ID as input
    user_id = user_entry.get()
    user_url = f"https://github.com/{user_id}"

    try:
        user = GitHubUser(giturl=user_url)
        repositories = fetch_user_repositories(user.giturl)

        complex_repository = None
        max_complexity = float('-inf')

        for repo in repositories:
            # Generate GPT analysis for the repository
            prompt = f"This repository, {repo['full_name']}, is technically complex."

            # Calculate complexity score based on GPT response
            gpt_response = generate_gpt_response(prompt)
            complexity_score = len(word_tokenize(gpt_response))

            # Print repository analysis
            result_text.insert(tk.END, f"Repository: {repo['full_name']}\n")
            result_text.insert(tk.END, f"Complexity Score: {complexity_score}\n")
            result_text.insert(tk.END, f"Analysis: {gpt_response}\n")
            result_text.insert(tk.END, "-------------------------------------\n")

            # Update max complexity and complex repository if necessary
            if complexity_score > max_complexity:
                max_complexity = complexity_score
                complex_repository = repo['full_name']

        # Print the most technically complex repository
        result_text.insert(tk.END, f"The most technically complex repository is: {complex_repository}\n")

    except requests.exceptions.HTTPError as e:
        result_text.insert(tk.END, f"HTTPError occurred: {str(e)}\n")
    except ValueError as e:
        result_text.insert(tk.END, f"ValueError occurred: {str(e)}\n")


# Create the main Tkinter window
window = tk.Tk()
window.title("GitHub Repository Complexity Analysis")
window.geometry("400x300")

# Create the user entry label and entry field
user_label = tk.Label(window, text="GitHub User ID:")
user_label.pack()
user_entry = tk.Entry(window)
user_entry.pack()

# Create the analyze button
analyze_button = tk.Button(window, text="Analyze Repositories", command=analyze_repositories)
analyze_button.pack()

# Create the result text box
result_text = tk.Text(window)
result_text.pack()

# Start the Tkinter event loop
window.mainloop()
