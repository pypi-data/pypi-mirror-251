import atexit
import datetime
import traceback
import sys

class ErrorMessenger:
    """Handler for returns ledgible error messages"""
    def __init__(self, script_name: str = "", additional_info: dict = {}) -> None:
        """
        Initializes the messenger with permanent script info
        Arguments:
            script_name (str): Name title of script. If not supplied this will simply be the script file path
            additional_info (dict): Additional info for the script
        """
        if script_name == "":
            import __main__
            self.script_name = getattr(__main__, "__file__", None)
        else:
            self.script_name = script_name
        self.additional_info = additional_info
        self._init_time = datetime.datetime.now()

        self.step_name = "ErrorMessenger initialized"
        self.step_time = self._init_time
        self.error_message = ""

        self._time_format = "%H:%M:%S, %d/%m/%Y"
        self._traceback = None

        sys.excepthook = self._save_traceback

    def _save_traceback(self, exc_type, exc, *args) -> None:
        self._traceback = (exc_type, exc)

    def update(self, step_name: str = None, error_message: str = None, verbose: bool = False) -> None:
        """
        Updates the error message to supply on script failure
        Arguments:
            step_name (str): The name of the step in the script the execution has reached
            error_message (str): A message describing what might have gone wrong
            verbose (bool): Will print the step_name if True. Default is False
        """
        self.step_name = step_name
        self.error_message = error_message
        self.step_time = datetime.datetime.now()
        if verbose:
            print(f"Step: {step_name}")
    
    def generate_error_message(self) -> str:
        """
        Generates the ledgible error message with all script info
        Returns:
            (str) The error message with info
        """
        now = datetime.datetime.now()
        t_form = lambda date: date.strftime(self._time_format)

        output = ""
        output += f"\nTime: {t_form(now)}"
        output += f"\nError in script: {self.script_name} on step: '{self.step_name}'"
        output += f"\nError message:\n\t{self.error_message}"

        if self.additional_info:
            output += f"\n\nAdditional info:"
            for key, val in self.additional_info.items():
                output += f"\n\t{key}: {val}"
        
        output += f"\n\n(ErrorMessenger was initialized at: {t_form(self._init_time)} [T: {(now - self._init_time).seconds}s]"
        output += f"\nStep began at: {t_form(self.step_time)} [T: {(now - self.step_time).seconds}s])"

        output += f"\n\nTraceback: {self._traceback[0]}"
        for detail in traceback.format_exception(self._traceback[1]):
            output += f"\n\t{detail.strip()}"
        return output
    
    def register(self, callback) -> None:
        atexit.register(lambda: callback(self.generate_error_message()))
