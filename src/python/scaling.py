import customtkinter as ctk
import platform

#Function to get the DPI scaling factor
def get_scaling_factor():
    """Returns the DPI scaling factor for the primary monitor."""

    # This only works on windows but it wont break for other os's
    # I wanted to add this because I thought the scaling should look universally good
    # This takes the default scaling factor that is used in windows and uses it within the app.
    # Which is great when you have some users using 100% scaling and others using 250%
    # It should look great for both of them (and the same!)
    # Im putting this in its own file to help with code clairty
    # TODO: Obtain hardware level scaling from other OS's

    if platform.system() == "Windows":
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
            # Gets DPI for the monitor
            dpi = windll.user32.GetDpiForWindow(windll.user32.GetDesktopWindow())
            # 96 DPI is the default 100% scaling
            return dpi / 96
        except Exception as e:
            print(f"Could not get DPI scaling from Windows: {e}")
            return 1.0 # This is our fallback
    # On macOS and Linux, CustomTkinter's default detection is usually good enough
    # or manual setting is more common. We can just return 1.0 and let CTk handle it.
    else:
        # On other OSes, we can let CustomTkinter do its thing,
        # or we might need a different library for detection.
        # Returning 1.0 here means "don't override CTk's default".
        return 1.0 