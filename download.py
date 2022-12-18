from tarsDAO import AIDAO

def main():
     # Print a message to indicate that the TARS memory is being downloaded
    print("UPLOADING TARS MEMORY")
    aidao = AIDAO()
    downloaded = aidao.downloadTARS()
    if (downloaded == True):
        print("TARS MEMORY SUCCESSFULLY DOWNLOADED")
    else:
        print("TARS MEMORY FAILED TO DOWNLOAD..")

if __name__ == "__main__":
    main()
