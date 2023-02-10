#program to look at downloaded text files and remove any that are empty or have less than 50 words
import os


path = "/home/player1/Desktop/RPI/ChatRPI/text/"
def main():
    files = os.listdir(path)
    for file in files:
        file = path + file
        with open(file, 'r') as f:
            lines = f.readlines()
            if len(lines) == 0:
                os.remove(file)
                continue
            words = 0
            for line in lines:
                words += len(line.split())
            if words < 100:
                os.remove(file)

#funtion to remove all special characters froms in a directory
def remove_special_characters(path):
    files = os.listdir(path)
    for file in files:
        file = path + file
        with open(file, 'r') as f:
            lines = f.readlines()
        with open(file, 'w') as



if __name__ == "__main__":
    main()
