# -*- coding: utf-8 -*-
import os

from api.collector import create_api
from api import app

api = create_api(app)

if __name__ == "__main__":
    api.run(port=8333, host='0.0.0.0', debug=True)
