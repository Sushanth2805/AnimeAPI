import streamlit as st
import requests

# Function to query the AniList API
def search_anime(query):
    url = 'https://graphql.anilist.co'
    query_string = '''
    query ($search: String) {
        Media (search: $search, type: ANIME) {
            id
            title {
                romaji
                english
                native
            }
            description
            episodes
            averageScore
            genres
            coverImage {
                large
            }
        }
    }
    '''
    variables = {
        'search': query
    }
    response = requests.post(url, json={'query': query_string, 'variables': variables})
    return response.json()

# Streamlit app
st.title('Anime Search App')
st.write('Search for your favorite anime!')

# Search bar
query = st.text_input('Enter anime title')

if query:
    result = search_anime(query)
    
    if 'data' in result and result['data']['Media']:
        anime = result['data']['Media']
        
        st.image(anime['coverImage']['large'])
        st.write(f"**Title (Romaji):** {anime['title']['romaji']}")
        st.write(f"**Title (English):** {anime['title']['english']}")
        st.write(f"**Title (Native):** {anime['title']['native']}")
        st.write(f"**Episodes:** {anime['episodes']}")
        st.write(f"**Average Score:** {anime['averageScore']}")
        st.write(f"**Genres:** {', '.join(anime['genres'])}")
        st.write(f"**Description:** {anime['description']}")
    else:
        st.write("No anime found. Please try another title.")
