from .whitebox_workflows import *
# from .scripts.scripts import strip_last_return_points

__doc__ = whitebox_workflows.__doc__
if hasattr(whitebox_workflows, "__all__"):
    __all__ = whitebox_workflows.__all__

class WbEnvironment(WbEnvironmentBase):
    """The WbEnvironment class can be used to configure WbW settings (e.g. the working
directory, number of processors used, and verbose mode). It is also used to call
the various tool functions, which appear as methods of this class, and to read/write
spatial data."""
    def __init__(self, user_id: str = None):
        """Initializes a new WbEnvironment object with an optional user_id, i.e. a floating
license ID string used in WbW-Pro licenses.
        """
        WbEnvironmentBase(user_id)

    def available_functions(self) -> None:
        """This function will list all of the available functions associated with a
WbEnvironment (wbe). The functions that are accessible will depend on the 
license level (WbW or WbWPro).
        """

        # Are we running a pro license?
        pro_license = self.license_type == LicenseType.WbWPro

        # Get all the non-dunder methods of WbEnvironment
        method_list = [func for func in dir(WbEnvironment) if callable(getattr(WbEnvironment, func)) and not func.startswith("__")]

        print(f"Available Methods ({self.license_type}):")

        j = 0
        s = ''
        for i in range(len(method_list)):
            val = method_list[i]
            val_len = len(f"{j}. {val}")
            is_pro_func = whitebox_workflows.is_wbw_pro_function(val)
            
            added = True
            if not is_pro_func and j % 2 == 0:
                s += f"{j+1}. {val}{' '* (50 - val_len)}"
                j += 1
            elif not is_pro_func and j % 2 == 1:
                s += f"{j+1}. {val}"
                j += 1
            elif (is_pro_func and pro_license) and j % 2 == 0:
                s += f"{j+1}. {val}{' '* (50 - val_len)}"
                j += 1
            elif (is_pro_func and pro_license) and j % 2 == 1:
                s += f"{j+1}. {val}"
                j += 1
            else:
                added = False
                

            if added and (j % 2 == 0 or i == len(method_list)-1):
                print(s)
                s = ''


    # def strip_last_return_points(self, lidar: Lidar) -> Lidar:
    #     return strip_last_return_points(self, lidar)


