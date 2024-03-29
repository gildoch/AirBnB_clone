#!/usr/bin/python3
"""City.py"""
from models.base_model import BaseModel


class City(BaseModel):
    """
    The class city inherit from Basemodel
    """

    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        """
        Initializing the state with *args and **kwargs
        """
        super().__init__(self, *args, **kwargs)
