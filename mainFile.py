from extract_tweets import extraction
from preprocessing import processing
from naive import naiveclassify

def calling():
    for counter in range(2):
        extraction()
        processing()
        naiveclassify()
        print("======================================================")
        print("=====================================================")

if __name__ == "__main__":
    calling()