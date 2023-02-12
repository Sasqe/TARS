from tarsDAO import AIDAO

def main():
     # Print a message to indicate that the TARS memory is being downloaded
    print("INITIALIZING DATABASE CONNECTION...")
    # Instantiate AIDAO class
    aidao = AIDAO()
    print("DOWNLOADING TARS MEMORY")
     # Make a call to the downloadTARS method to download TARS's memory
    downloaded = aidao.downloadTARS()
     # Check if TARS'S memory was downloaded
    if (downloaded):
        print("TARS MEMORY SUCCESSFULLY DOWNLOADED")
    else:
        print("TARS MEMORY FAILED TO DOWNLOAD..")
    return downloaded
# If the script is being run directly, call the main function
if __name__ == "__main__":
    main()
