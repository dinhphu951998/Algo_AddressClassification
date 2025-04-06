# Address Classification Analysis

## Overview
This project implements a Vietnamese address classification system that extracts and normalizes province, district, and ward information from unstructured address strings. The solution uses efficient string matching algorithms and custom data structures to achieve high performance.

## Implementation Details
The implementation uses several key components:

### 1. Trie Data Structure
- Custom Trie implementation for efficient string matching
- Optimized for Vietnamese text with accent handling

### 2. Text Normalization
- Removes unnecessary spaces, punctuation, and standardizes formats
- Handles Vietnamese diacritics appropriately
- Normalizes common address prefixes (TP, Quận, Huyện, etc.)

### 3. Search Algorithm
- Multi-stage search process prioritizing province, district, then ward
- Segment-based search for handling unstructured input
- Autocorrection for misspelled location names

### 4. Autocorrection
- Edit distance calculations using Levenshtein algorithm
- Handles common Vietnamese spelling variations
- Configurable threshold for matching confidence with Cosine similarity

## Setup Instructions
1. Ensure Python 3.x is installed
2. Place the following files in the project root:
   - `list_province.txt`
   - `list_district.txt`
   - `list_ward.txt`
3. No additional dependencies required - uses only Python standard library

## Project Structure
- `Solution.py` - Main solution class and entry point
- `Searcher.py` - Core search algorithms and Trie operations
- `Autocorrect.py` - Spelling correction functionality
- `Utils.py` - Text normalization and utility functions
- `IndexAnalyzer.py` - Trie data structure implementation

## Performance Requirements
- Maximum time for 1 request: ≤ 0.1 seconds
- Average time for 1 request: ≤ 0.01 seconds

## Testing
- Unit tests available in `RunTests.py`
- Benchmark tests for performance validation

## Dataset
1. Province List (`list_province.txt`):
2. District List (`list_district.txt`):
3. Ward List (`list_ward.txt`):