"""
This is sample code to tell how to use sawsi framework.
You could delete this file after know how to use this framework.
"""
from ..dao import sample_user_dao
from ..model.sample_user import User
from ..view_model import sample_user_vm


def login(email:str, password:str):
    return {
        'session_id': '<SESSION_ID>'
    }


def get_me(session_id:str):
    # Get Data Model from DAO
    user:User = sample_user_dao.get_user_by_session(session_id)
    # Transform to view model
    user_view_model:dict = sample_user_vm.make(user)
    return {
        'user': user_view_model
    }
