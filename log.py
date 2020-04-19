from time import sleep

# Note: terminal output can be improved with the termcolor module
# pip install termcolor
_termcolor_exists_ = False
try:
    from termcolor import colored
    _termcolor_exists_ = True
except ImportError:
    pass

_sleepTime_ = 0.25   # Seconds

# Logging
def log(msg="", indent=0, sleepMultiplier=1, newline=True, color=None, colorBackground=None, attrs=None):

    # color is only valid if the termcolor module is installed
    if _termcolor_exists_:
        msg = colored(msg, color=color, on_color=colorBackground, attrs=attrs)

    end = "\n" if newline else ""
    print('\t'*indent + msg, end=end)
    sleep(_sleepTime_ * sleepMultiplier)
