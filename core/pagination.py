from typing import OrderedDict
from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):
    def contruct_dict_from_list(self, data_list: list) -> dict:
        """
        Constructs a dictionary from a list of data.
        :param data_list: list of data
        :return: dict
        """
        return {
            split_value[0]: split_value[1]
            for split_value in [value.split("=") for value in data_list]
        }

    def get_offset_from_url(self, url: str):
        if not url:
            return None
        raw_params = url.split("?")[-1]
        split_params = raw_params.split("&")
        params = self.contruct_dict_from_list(split_params)
        if "offset" in params:
            return params["offset"]
        return None

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        raw_data = response.data
        previous_offset = self.get_offset_from_url(raw_data["previous"])
        next_offset = self.get_offset_from_url(raw_data["next"])
        raw_data.update(
            {
                "previous_offset": previous_offset,
                "next_offset": next_offset,
            }
        )
        response.data = raw_data
        return response
