import numpy as np

# Sample mutual information between syllable pairs
# In practice, these values should be computed from a large dataset
mutual_info = {
    ('học', 'sinh'): 2.5,
    ('sinh', 'học'): 1.8,
    ('học', 'sinh học'): 0.5,
    ('sinh học', 'sinh'): 0.3,
    # Add more syllable pairs and their MI values if needed
}

def compute_mi(syllable1, syllable2):
    """Retrieve the mutual information value for a pair of syllables."""
    return mutual_info.get((syllable1, syllable2), 0)

def segment_text(syllables):
    """
    Segment a list of syllables into words using dynamic programming
    to maximize the sum of mutual information values.
    """
    n = len(syllables)
    dp = np.zeros(n + 1)  # Initialize dynamic programming table
    segmentation = [[] for _ in range(n + 1)]  # Store the segmented words as lists

    for i in range(1, n + 1):
        best_score = dp[i - 1]
        best_segmentation = segmentation[i - 1] + [syllables[i - 1]]

        # Iterate over previous positions to find the best segmentation
        for j in range(i):
            word = ' '.join(syllables[j:i])  # Create a potential word from syllables[j:i]
            if j > 0:
                # Compute the mutual information between the last word of previous segment and the current word
                mi = compute_mi(' '.join(segmentation[j][-1:]), word)
                score = dp[j] + mi
                if score > best_score:
                    best_score = score
                    best_segmentation = segmentation[j] + [word]

        dp[i] = best_score  # Update the dp table with the best score
        segmentation[i] = best_segmentation  # Store the best segmentation so far

    return segmentation[-1]  # Return the final segmented words as a list

# Example usage
text = "học sinh học sinh học"  # Input text to be segmented
syllables = text.split()  # Split the text into syllables
segmented_array = segment_text(syllables)  # Get the segmented words as an array
print(segmented_array)  # Print the segmented words
