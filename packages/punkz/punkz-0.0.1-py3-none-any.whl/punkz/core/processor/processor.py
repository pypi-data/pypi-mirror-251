from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Tuple
import traceback


class Processable(ABC):
    """
    Abstract class representing a processable object.
    """

    @abstractmethod
    def invoke(self, data: Any) -> Any:
        """
        Invoke the processable object.
        """
        pass

    @abstractmethod
    def __or__(self, other) -> "Routine":
        """
        Define the pipe operator for the processable object.
        """
        pass


class ProcessStatus(Enum):
    """
    Enum representing the status of a process.

    Attributes:
        GREEN (int): The process is in a green status.
        RED (int): The process is in a red status.
    """

    GREEN = 1
    RED = 0


class ProcessorInput(Processable):
    """
    Represents the input data for a processor.
    """

    def __init__(self, input_data: dict) -> Any:
        self.__data = input_data

    def get_input(self) -> Any:
        """
        Get the input data.
        """
        return self.__data

    def invoke(self, _) -> Any:
        """
        Invoke the processor.
        """
        return {"status": ProcessStatus.GREEN, "data": self.get_input()}

    def __repr__(self) -> str:
        return f"ProcessorInput | data: {self.get_input()})"

    def __or__(self, other) -> "Routine":
        return Routine(self, other)


class Processor(Processable):
    """
    A class representing a processor.

    Attributes:
        __name: The name of the processor.

    Methods:
        get_name: Get the name of the processor.
        process: Process the data.
        invoke: Invoke the processor with data.
        __or__: Create a routine with another processor.
        __repr__: Get a string representation of the processor.
    """

    def __init__(self, name: str) -> None:
        self.__name = name

    def get_name(self):
        return self.__name

    @staticmethod
    def railway(func):
        """
        Decorator function that wraps another function and handles exceptions.

        Args:
            func (function): The function to be wrapped.

        Returns:
            function: The wrapped function.

        Decorator logic:
        This decorator wraps a function with error handling logic.
        It catches any exceptions that occur during the execution
        of the wrapped function and returns a dictionary with the status and data.
        If the status is RED, it returns the original data.
        If the status is GREEN, it calls the wrapped function with
        the provided data and returns the result.
        If an exception occurs, it returns a dictionary with the status set to RED,
        and includes the exception, broken processor name, and input data.

        """

        def wrapper(*args, **kwargs):
            try:
                invoke_kwargs = kwargs["invoke_kwargs"]
                status = invoke_kwargs["status"]
                data = invoke_kwargs["data"]
                self = args[0]
                if status == ProcessStatus.RED:
                    return {"status": status, "data": data}
                return {"status": ProcessStatus.GREEN, "data": func(self, data)}
            except Exception as e:
                return {
                    "status": ProcessStatus.RED,
                    "data": {
                        "exception": e,
                        "broken_processor": self.get_name(),
                        "input_data": kwargs,
                    },
                    "traceback": traceback.format_exc(),
                }

        return wrapper

    @railway
    def process(self, data: dict) -> dict:
        """
        Process the given data and return the modified data.
        This is the method that should be overridden by subclasses.
        Here goes the logic of the processor.

        Args:
            data (dict): The input data to be processed.

        Returns:
            dict: The processed data.

        """
        return data + "_" + self.get_name()

    def invoke(self, data: dict) -> dict:
        """
        Invoke the processor with the given data.

        Args:
            data (dict): The input data for the processor.

        Returns:
            dict: The processed data.

        """
        return self.process(invoke_kwargs=data)

    def __or__(self, other) -> "Routine":
        """
        Performs the logical OR operation between two processors.
        This allows the concatenation of processors in a Routine.

        Args:
            other (Processor): The other processor to perform the OR operation with.

        Returns:
            Routine: A new Routine object representing a pipeline of the two processors.
        """
        return Routine(self, other)

    def __repr__(self) -> str:
        return f"Processor({self.get_name()})"


class Routine(Processable):
    """
    A class representing a pipeline of processors.

    Attributes:
        processors (list): A list of processors in the routine.

    Methods:
        __init__(*processors): Initializes the Routine object with a list of processors.
        __or__(other): Adds a processor to the routine using the '|' operator.
        invoke(input_data=None): Invokes the routine by sequentially applying each processor to the input data.
        __repr__(): Returns a string representation of the Routine object.
    """

    def __init__(self, *processors) -> None:
        self.processors = [*processors]

    def __or__(self, other) -> "Routine":
        self.processors.append(other)
        return self

    def invoke(self, input_data=None) -> Any:
        for processor in self.processors:
            input_data = processor.invoke(input_data)
        return input_data

    def __repr__(self) -> str:
        return f"Routine | processors: {self.processors})"


if __name__ == "__main__":

    class T(Processor):
        def __init__(self, name: str) -> None:
            super().__init__(name)

        @Processor.railway
        def process(self, data) -> Tuple:
            return data["my_data"]

    class E(Processor):
        def __init__(self, name: str) -> None:
            super().__init__(name)

        @Processor.railway
        def process(self, data) -> Tuple:
            return data * self.get_name()

    input_processor = T("T")
    processor_a = Processor("A")
    processor_b = Processor("B")
    processor_c = Processor("C")
    error_processor = E("E")

    input_ = ProcessorInput({"my_data": "my_data"})
    x = input_ | input_processor | processor_a | processor_b | processor_c
    res = x.invoke()
    print(x)
    print("\n------------------\n")
    print(res)
