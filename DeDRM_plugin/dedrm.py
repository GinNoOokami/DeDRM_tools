import os
from sys import argv
import tempfile
import kindlekey
import k4mobidedrm


# Dictionaries and such
ignore = [
    "B005FNK020_EBOK",
    "B00DQB1G3K_EBOK",
    "B005FNK002_EBOK",
    "B00AZOHEFU_EBOK",
    "B007Z8VKSQ_EBOK"
]


def decrypt_key():
    print("Decrypting key...")
    keyfile = os.path.join(tempfile.gettempdir(), "kindlekey.k4i")
    if not kindlekey.getkey(keyfile, []):
        exit(1)
    return keyfile


def decrypt_all_books(input_path, output_path):
    if not os.path.isdir(input_path):
        raise FileExistsError("input_path must be a directory to the Kindle library")

    keyfile = decrypt_key()

    print("Scanning for books...")
    book_filenames = []
    for root, _, files in os.walk(input_path, topdown=True):
        for file in files:
            filename, ext = os.path.splitext(file)

            if ext not in [".azw", ".azw3"]:
                continue

            if filename in ignore:
                continue

            full_path = os.path.join(root, file)
            book_filenames.append(full_path)
    print(f"Found {len(book_filenames)} books.")

    if not os.path.isdir(output_path):
        try: 
            os.makedirs(output_path, exist_ok=True) 
        except OSError as error: 
            print(error)  

    failed_books = []
    print(f"Beginning to decrypt {len(book_filenames)} books...")
    for book_filename in book_filenames:
        try:
            k4mobidedrm.decryptBook(book_filename, output_path, [keyfile], [], [], [])
        except Exception as err:
            print(err)
            failed_books.append(book_filename)
    
    if failed_books:
        print(f"Failed to decrypt the following {len(failed_books)} book(s):")
        for failed in failed_books:
            print(failed)

if __name__ == "__main__":
    if len(argv) < 3:
        print('usage: dedrm.py [input_path] [output_path]')
        exit(1)

    decrypt_all_books(argv[1], argv[2])