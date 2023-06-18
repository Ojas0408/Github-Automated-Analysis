import openai
import requests
import base64
from dataclasses import dataclass
from urllib.parse import urlparse
from urllib.error import HTTPError
from nltk.tokenize import word_tokenize

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
        engine="text-davinci-003",
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


# Take GitHub user ID as input
user_id = input("Enter GitHub user ID: ")
user_url = f"https://github.com/{user_id}"

try:
    user = GitHubUser(giturl=user_url)
    repositories = fetch_user_repositories(user.giturl)

    complex_repository = None
    max_complexity = float('-inf')

    for repo in repositories:
        # Fetch README file contents
        readme_url = f"{repo['url']}/readme"
        readme_response = requests.get(readme_url, timeout=10, headers=headers)
        readme_content = base64.b64decode(readme_response.json()['content']).decode('utf-8')

        # Generate GPT analysis for the repository
        prompt = f"This repository, {repo['full_name']}, is technically complex because {readme_content}."
        gpt_response = generate_gpt_response(prompt)

        # Calculate complexity score based on GPT response
        complexity_score = len(word_tokenize(gpt_response))

        # Print repository analysis
        print(f"Repository: {repo['full_name']}")
        print(f"Complexity Score: {complexity_score}")
        print(f"Analysis: {gpt_response}")
        print("-------------------------------------")

        # Update max complexity and complex repository if necessary
        if complexity_score > max_complexity:
            max_complexity = complexity_score
            complex_repository = repo['full_name']

    # Print the most technically complex repository
    print(f"The most technically complex repository is: {complex_repository}")

except requests.exceptions.HTTPError as e:
    print(f"HTTPError occurred: {str(e)}")
except ValueError as e:
    print(f"ValueError occurred: {str(e)}")
