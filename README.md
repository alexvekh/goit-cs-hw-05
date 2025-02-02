## goit-cs-hw-05

# Asynchronous File Sorter

This Python script reads all files in a specified source folder and distributes them into subfolders in a destination directory based on their file extensions. The script performs the sorting asynchronously for more efficient processing of a large number of files.

### Features

- Asynchronous processing: Utilizes Python's asyncio and aiofiles libraries for efficient file handling.
- Automatic virtual environment activation: The script can activate a specified virtual environment automatically.
- Error logging: Logs any errors that occur during the file copying process.

### Script Details

- read_folder: Recursively reads all files in the source folder and its subfolders, creating tasks for copying each file.
- copy_file: Copies each file to the corresponding subfolder in the destination directory based on the file extension.

### Prerequisites

- Python 3.7+
- aiofiles library: Install via pip install aiofiles
- argparse library (included in Python standard library)

### Before usage

- Create a Virtual Environment

      python -m venv venv

- Activate the Virtual Environment

  - Windows:

         Set-ExecutionPolicy Bypass -Scope Process
         .\venv\Scripts\

  - MacOS/Linux:

        source venv/bin/activate

- Install Required Libraries

      pip install aiohttp aiofiles

### Usage:

      python copy_files_by_ext.py /path/to/source_folder /path/to/output_folder

### Acknowledgments

Thanks to the authors of asyncio and aiofiles libraries for enabling efficient asynchronous file handling in Python.

#

#

# Asynchronous Word Frequency Counter

This project implements an asynchronous word frequency counter using Python. It reads a text from a specified URL, processes the text to remove punctuation, convert words to lowercase, and exclude articles. The processed text is then analyzed using a MapReduce approach to count the frequency of each word. The results are visualized using a horizontal bar chart created with Matplotlib.

### Features

- Asynchronous Processing: Uses ThreadPoolExecutor for parallel mapping and reduction to efficiently handle large texts.
- Punctuation Removal: Cleans the text by removing punctuation.
- Lowercase Conversion: Converts all words to lowercase to ensure accurate frequency counting.
- Article Exclusion: Excludes common articles (the, a, an) from the word count.
- Custom Word Search: Allows for counting specific words if a search list is provided.
- Visualization: Visualizes the top N most frequent words using Matplotlib.

### Prerequisites

Ensure you have Python installed. You'll also need to install the following libraries:

- requests: For fetching text from a URL.
- matplotlib: For visualizing the word frequencies.
- concurrent.futures: For asynchronous processing (included in the Python standard library).
- string: For handling string operations (included in the Python standard library).

### Function Descriptions

- get_text(url): Fetches text from the specified URL.
- remove_punctuation(text): Removes punctuation from the text.
- map_function(word): Maps each word to a tuple (word, 1).
- shuffle_function(mapped_values): Groups the mapped values by key.
- reduce_function(key_values): Reduces the grouped values by summing the counts.
- map_reduce(text, search_words=None): Executes the MapReduce process on the text.
- visualize_top_words(result, top_n=10): Visualizes the top N most frequent words using a horizontal bar chart.
