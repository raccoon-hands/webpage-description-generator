import io

#This function returns a truncated version of a long piece of text
#down to 500 words
def truncate_text(text):
    # Split the paragraph into words
    words = text.split()

    # Initialize an empty list to store the truncated words
    truncated_words = []

    # Initialize word count
    word_count = 0

    # Iterate through the words and keep adding them to the truncated_words list
    # until the total word count reaches 600
    for word in words:
        if word_count + len(word) + 1 <= 600:  # +1 to account for the space after the word
            truncated_words.append(word)
            word_count += len(word) + 1
        else:
            break

    # Use StringIO to join the truncated words into a new paragraph efficiently
    truncated_text = io.StringIO()
    truncated_text.write(' '.join(truncated_words))
    truncated_text_str = truncated_text.getvalue()
    truncated_text.close()

    return truncated_text_str

