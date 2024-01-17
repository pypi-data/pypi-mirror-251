import datetime
import typing

import pydantic


def parse_response_to_model(
    response: dict, model: typing.Type[pydantic.BaseModel]
) -> pydantic.BaseModel:
    return model(**response)


def generate_json_paths_and_values(
    data, current_path="$", separator="."
) -> dict[str, typing.Any]:
    """
    Generate a map of JSON paths to their corresponding values for nested dictionaries and lists.

    Parameters:
    - data: The input dictionary or list.
    - current_path: (Optional) The current path being processed (used in recursion).
    - separator: (Optional) The separator between keys or indices in the path.

    Returns:
    - A dictionary mapping JSON paths to their corresponding values.
    """
    paths_and_values = {}

    if isinstance(data, dict):
        for key, value in data.items():
            # Create the path for the current key
            key_path = f"{current_path}{separator}{key}"

            if isinstance(value, (dict, list)):
                # Recursively call the function for nested dictionaries or lists
                paths_and_values.update(
                    generate_json_paths_and_values(value, key_path, separator)
                )
            else:
                # If the value is neither a dictionary nor a list, add the current path and value to the dictionary
                paths_and_values[key_path] = value
    elif isinstance(data, list):
        for index, item in enumerate(data):
            # Create the path for the current index
            index_path = f"{current_path}{separator}{index}"

            if isinstance(item, (dict, list)):
                # Recursively call the function for nested dictionaries or lists
                paths_and_values.update(
                    generate_json_paths_and_values(item, index_path, separator)
                )
            else:
                # If the item is neither a dictionary nor a list, add the current path and value to the dictionary
                paths_and_values[index_path] = item

    return paths_and_values


class Lifecycle(pydantic.BaseModel):
    created_at: int
    updated_at: int
    deleted_at: typing.Union[int, None] = None

    def get_created_at_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.created_at)

    def get_updated_at_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.updated_at)

    def get_deleted_at_datetime(self) -> typing.Union[datetime.datetime, None]:
        if self.deleted_at is None:
            return None

        return datetime.datetime.fromtimestamp(self.deleted_at)
