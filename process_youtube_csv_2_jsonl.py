import pandas as pd
import json

def combine_features(row):
    try:
        return row['title'] + " " + row["channel_title"]
    except Exception as e:
        print("Error:", row, e)

def process_us_videos_csv(input_file, output_file):
    # Load the CSV file
    videos = pd.read_csv(input_file)
    
    # Fill missing values for relevant columns
    for f in ['title', 'channel_title']:
        videos[f] = videos[f].fillna('')
    
    # Create a "text" column by combining title and channel_title
    videos["text"] = videos.apply(combine_features, axis=1)
    
    # Select and rename columns to match required Vespa format
    videos = videos[['video_id', 'title', 'text', 'views', 'likes', 'dislikes', 'comment_count', 'publish_time']]
    videos.rename(columns={'video_id': 'doc_id'}, inplace=True)
    
    # Create 'fields' column as JSON-like structure of each record
    videos['fields'] = videos.apply(lambda row: row.to_dict(), axis=1)
    
    # Create 'put' column based on 'doc_id'
    videos['put'] = videos['doc_id'].apply(lambda x: f"id:hybrid-search:doc::{x}")
    
    # Prepare the final DataFrame for JSONL export
    df_result = videos[['put', 'fields']]
    
    # Output the processed data to a JSON file in Vespa-compatible format
    df_result.to_json(output_file, orient='records', lines=True)

# Usage example
process_us_videos_csv("CAvideos.csv", "clean_ca_videos.jsonl")
