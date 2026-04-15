# a script to process and count words in a CSV file
import csv


# Load the CSV file so that we can work with each response as structured data
filename = "demo_responses.csv"
responses = []

# Opens a comma separated value (.csv) file that contains the dataset and reads it into our responses variable so that we can work with it in Python
with open(filename, newline="", encoding="utf-8") as f:
    #DictReader reads the CSV file and returns a dictionary of the rows so I can use things like row["participant_id"] to access the data in the row instead of remembering where each value is
    reader = csv.DictReader(f)
    for row in reader:
        responses.append(row)

# Helper function to count the number of words in a response
def count_words(response):
    """Count the number of words in a response string.

    Takes a string, splits it on whitespace, and returns the word count.
    Used to measure response length across all participants.
    """
    return len(response.split())


# Count words in each response and print a row-by-row summary so that we have readable output
print(f"{'ID':<6} {'Role':<22} {'Words':<6} {'Response (first 60 chars)'}")
print("-" * 75)

word_counts = []


# Loop through each row in the responses list and count the words in the response

for row in responses:
    participant = row["participant_id"]
    role = row["role"]
    response = row["response"]

    # Call our function to count words in this response
    # split on whitespace to count words
    count = count_words(response)
    #append the count to the word_counts list 
    word_counts.append(count)

    # Truncate the response preview for display so that we have a readable output that isn't too long
    if len(response) > 60:
        preview = response[:60] + "..."
    else:
        preview = response

    print(f"{participant:<6} {role:<22} {count:<6} {preview}")

# Print summary statistics to give an overview of the dataset such as the total number of responses, the shortest response, the longest response, and the average response length
print()
print("── Summary ─────────────────────────────────")
print(f"  Total responses : {len(word_counts)}")
print(f"  Shortest        : {min(word_counts)} words")
print(f"  Longest         : {max(word_counts)} words")
print(f"  Average         : {sum(word_counts) / len(word_counts):.1f} words")
