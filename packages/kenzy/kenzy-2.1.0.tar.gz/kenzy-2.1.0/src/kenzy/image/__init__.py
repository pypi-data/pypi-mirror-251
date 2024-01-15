import sys
import logging 
import traceback

try:
    from kenzy.image import device

    class device(device.VideoProcessor):
        pass

except ModuleNotFoundError:
    logging.debug(str(sys.exc_info()[0]))
    logging.debug(str(traceback.format_exc()))
    logging.info("Unable to start image processor due to missing libraries")