import os


# Function to remove all files in a directory wth less than 10 words
def cleanup(path):
    files = os.listdir(path)
    for file in files:
        with open(path + file) as f:
            words = f.read().split()
            if len(words) < 10:
                os.remove(path + file)
                print("removed " + file)

# Function to remove all duplicate files in a directory using diff and rm
def remove_duplicates(path):
    files = os.listdir(path)
    for file in files:
        for file2 in files:
            if file != file2:
                if os.system("diff " + path + file + " " + path + file2 + " > /dev/null") == 0:
                    os.remove(path + file2)
                    print("removed " + file2)



path = "../text/"

if __name__ == "__main__":
    remove_duplicates(path)
    cleanup(path)
