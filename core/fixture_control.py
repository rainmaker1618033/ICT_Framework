# core/fixture_control.py

from controllers.base_controller import ICTControllerBase

def close_fixture(controller: ICTControllerBase):
    controller.fixture_close()

def open_fixture(controller: ICTControllerBase):
    controller.fixture_open()
