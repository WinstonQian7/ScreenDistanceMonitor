from win10toast import ToastNotifier
import time

# #############################################################################
# ###### Stand alone program ########
# ###################################
if __name__ == "__main__":
    # Example
    toaster = ToastNotifier()
    toaster.show_toast(
        "Eyedistance Monitor",
        "Too close to screen!", icon_path=None,
        duration=10,threaded=False)
 
    # Wait for threaded notification to finish
    while toaster.notification_active(): time.sleep(0.1)