import requests

# Replace these variables with your WordPress site details
wordpress_url = 'https://kw.smart-media.agency'
username = 'admin'

# Example: Get a list of posts
posts_url = f'{wordpress_url}/wp-json/wp/v2/posts'
headers = {
    'Authorization': f'Bearer {password}',
    'Content-Type': 'application/json',
}
posts_response = requests.get(posts_url, headers=headers)
posts_data = posts_response.json()

# Print the titles of the first 5 posts
for post in posts_data:
    print(post['title']['rendered'])