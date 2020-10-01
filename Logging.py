import logging

# Create and configure logging
def Log():

    LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(filename = "C:\\Users\\paolo\\OneDrive\\Desktop\\Real-Estate-project\\logging.log",
                        level = logging.INFO,
                        format = LOG_FORMAT,
                        filemode = 'w')
