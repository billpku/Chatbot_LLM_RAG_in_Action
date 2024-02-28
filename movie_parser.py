import csv
import json

"""
This script parses the MovieSummaries dataset and combines the metadata, character (actor) information, and plot summaries
The data source : https://www.cs.cmu.edu/~ark/personas/
"""

# Paths to the dataset files
metadata_path = 'data/MovieSummaries/movie.metadata.tsv'
character_metadata_path = 'data/MovieSummaries/character.metadata.tsv'
plot_summaries_path = 'data/MovieSummaries/plot_summaries.txt'
output_json_path = 'data/MovieSummaries/movie.json'

# Initialize dictionaries to hold movie metadata, character (actor) information, and plot summaries
movies_metadata = {}
movie_actors = {}
plot_summaries = {}

# Function to parse Freebase ID:name tuples and return a list of names
def parse_freebase_tuples(freebase_tuples_str):
    tuples = eval(freebase_tuples_str)
    return [name for _, name in tuples.items()]

# Parse the movie metadata
with open(metadata_path, 'r', encoding='utf-8') as file:
    tsv_reader = csv.reader(file, delimiter='\t')
    for row in tsv_reader:
        wikipedia_movie_id = row[0]
        movies_metadata[wikipedia_movie_id] = {
            'movie_id': wikipedia_movie_id,
            'title': row[2],
            'release_date': row[3],
            'supported_languages': parse_freebase_tuples(row[6]),
            'movie_countries': parse_freebase_tuples(row[7]),
            'movie_genres_list': parse_freebase_tuples(row[8]),
            'movie_actor_list': []  # Placeholder, to be filled from character metadata
        }

# Parse the character metadata to build the actor list for each movie
with open(character_metadata_path, 'r', encoding='utf-8') as file:
    tsv_reader = csv.reader(file, delimiter='\t')
    for row in tsv_reader:
        wikipedia_movie_id = row[0]
        actor_name = row[8]
        if wikipedia_movie_id in movies_metadata:
            movies_metadata[wikipedia_movie_id]['movie_actor_list'].append(actor_name)

# Parse the plot summaries
with open(plot_summaries_path, 'r', encoding='utf-8') as file:
    for line in file:
        wikipedia_movie_id, summary = line.split('\t', 1)
        plot_summaries[wikipedia_movie_id] = summary.strip()

# Add plot summaries to the movie metadata
for movie_id, movie_info in movies_metadata.items():
    movie_info['summary'] = plot_summaries.get(movie_id, "Summary not available")

# Convert the movie metadata dictionary to a list of dictionaries
movies_info_list = list(movies_metadata.values())

# Write the combined information to a JSON file
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(movies_info_list, json_file, indent=4)
