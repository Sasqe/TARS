from tarsDAO import AIDAO

def main():
    # Print a message to indicate that the TARS memory is being uploaded
    print("UPLOADING TARS MEMORY")
    # Create an instance of the AIDAO class
    aidao = AIDAO()
    # Call the uploadTARS method to upload the TARS memory
    uploaded = aidao.uploadTARS()
      # Check if the upload was successful and print a message accordingly
    if (uploaded):
        print("TARS MEMORY SUCCESSFULLY UPLOADED")
    else:
        print("TARS MEMORY FAILED TO UPLOAD..")

# If the script is being run directly, call the main function
if __name__ == "__main__":
    main()
