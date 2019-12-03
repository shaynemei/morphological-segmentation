#!/usr/bin/env python3

import re
import sys
import pickle

# Find all possible morphological segmentation pairs of up to three morphemes per word
# Morphemes are at least 2 chars
def morph_seg(words, exception_list):
    splits = []
    for word in words:
        splits_1 = [[word]]
        
        # Find 2-morpheme splits
        splits_2 = []
        freedom_2 = len(word) - 4
        for i in range(freedom_2 + 1):
            first_split = word[:2+i]
            second_split = word[2+i:]
            splits_2.append([first_split, second_split])

            # Check for connectors from exception_list and generate new splits
            if len(first_split) == 3:
                if first_split[-1] in exception_list:
                    splits_2.append([first_split[:-1], second_split])
            elif len(first_split) > 3:
                if first_split[-1] in exception_list:
                    splits_2.append([first_split[:-1], second_split])
                if first_split[-2:] in exception_list:
                    splits_2.append([first_split[:-2], second_split])
                    
        # Find 3-morpheme splits
        splits_3 = []
        freedom_3 = freedom_2 - 2
        for i in range(freedom_3 + 1):
            for j in range(i+1):
                first_split = word[:2+freedom_3-i]
                second_split = word[2+freedom_3-i:2+freedom_3-i+i+2-j]
                third_split = word[2+freedom_3-i+i+2-j:]
    
                splits_3.append([first_split, second_split, third_split])
        
                # Check for connectors from exception_list and generate new splits
                # Also check for connectors between second and third morpheme
                if len(first_split) < 3: 
                    if len(second_split) == 3:
                        if second_split[-1] in exception_list:
                            splits_3.append([first_split, second_split[:-1], third_split])
                    elif len(second_split) > 3:
                        if second_split[-1] in exception_list:
                            splits_3.append([first_split, second_split[:-1], third_split])
                            if second_split[-2:] in exception_list:
                                splits_3.append([first_split, second_split[:-2], third_split])
                elif len(first_split) == 3:
                    if first_split[-1] in exception_list:
                        splits_3.append([first_split[:-1], second_split, third_split])
                        if len(second_split) == 3:
                            if second_split[-1] in exception_list:
                                splits_3.append([first_split[:-1], second_split[:-1], third_split])
                                splits_3.append([first_split, second_split[:-1], third_split])
                        elif len(second_split) > 3:
                            if second_split[-1] in exception_list:
                                splits_3.append([first_split[:-1], second_split[:-1], third_split])
                                splits_3.append([first_split, second_split[:-1], third_split])
                                if second_split[-2:] in exception_list:
                                    splits_3.append([first_split[:-1], second_split[:-2], third_split])
                                    splits_3.append([first_split, second_split[:-2], third_split])
                    elif len(second_split) == 3:
                        if second_split[-1] in exception_list:
                            splits_3.append([first_split, second_split[:-1], third_split])
                    elif len(second_split) > 3:
                        if second_split[-1] in exception_list:
                            splits_3.append([first_split, second_split[:-1], third_split])
                            if second_split[-2:] in exception_list:
                                splits_3.append([first_split, second_split[:-2], third_split])

                elif len(first_split) > 3:
                    if first_split[-1] in exception_list:
                        splits_3.append([first_split[:-1], second_split, third_split])
                        if len(second_split) == 3:
                            if second_split[-1] in exception_list:
                                splits_3.append([first_split[:-1], second_split[:-1], third_split])
                                splits_3.append([first_split, second_split[:-1], third_split])
                        elif len(second_split) > 3:
                            if second_split[-1] in exception_list:
                                splits_3.append([first_split[:-1], second_split[:-1], third_split])
                                splits_3.append([first_split, second_split[:-1], third_split])
                                if second_split[-2:] in exception_list:
                                    splits_3.append([first_split[:-1], second_split[:-2], third_split])
                                    splits_3.append([first_split, second_split[:-2], third_split])

                        if first_split[-2:] in exception_list:
                            splits_3.append([first_split[:-2], second_split, third_split])
                            if len(second_split) == 3:
                                if second_split[-1] in exception_list:
                                    splits_3.append([first_split[:-2], second_split[:-1], third_split])
                                    splits_3.append([first_split, second_split[:-1], third_split])
                            elif len(second_split) > 3:
                                if second_split[-1] in exception_list:
                                    splits_3.append([first_split[:-2], second_split[:-1], third_split])
                                    splits_3.append([first_split, second_split[:-1], third_split])
                                    if second_split[-2:] in exception_list:
                                        splits_3.append([first_split[:-2], second_split[:-2], third_split])
                                        splits_3.append([first_split, second_split[:-2], third_split])
                    elif len(second_split) == 3:
                        if second_split[-1] in exception_list:
                            splits_3.append([first_split, second_split[:-1], third_split])
                    elif len(second_split) > 3:
                        if second_split[-1] in exception_list:
                            splits_3.append([first_split, second_split[:-1], third_split])
                            if second_split[-2:] in exception_list:
                                splits_3.append([first_split, second_split[:-2], third_split])
        splits_2.extend(splits_3)
        splits_1.extend(splits_2)
        splits.append(splits_1)
    return splits

def main():
    words = sys.stdin.readlines()
    words = [word.lower().replace("\n","") for word in words]
    exception_list = ['n', 'en', 's', 'es', 'e', '-']

    # Get all possible morph splits up to 3 per word, excluding splits with the first morph not in the data
    splits = morph_seg(words, exception_list)

    # Creat Counter object for occurences of all tokens in europarl.de
    with open('./freq_europarl', 'rb') as inputfile:
        count_data = pickle.load(inputfile)

    # Find splits with at least one morpheme with zero freq to exclude later
    zero_freq_pairs = []
    for i, word in enumerate(splits):
        for j, morph_pairs in enumerate(word):
            for k, morph in enumerate(morph_pairs):
                if count_data[morph] == 0:
                    zero_freq_pairs.append((i,j))
                    break

    # Calculate frequency score according to the metric proposed in Koehn and Knight (2003)
    for i, word in enumerate(splits):
        for j, morph_pairs in enumerate(word):
            if (i,j) in zero_freq_pairs:
                continue
            product = 1
            print(" ".join(morph_pairs) + " = ", end = "")
            for k, morph in enumerate(morph_pairs):
                freq = count_data[morph]
                print(morph + " (" + str(freq) + ") ", end = "")
                product *= freq
            score = round(product**(1/(k+1)), 1)
            print("= " + str(score))

if __name__ == "__main__":
    main()