"""
Test db factory
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""
import distutils.spawn
import logging
import os
import unittest
from pathlib import Path
from unittest import TestCase

import sqlalchemy.exc
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError

from hub.persistence.db_control import DBControl
from hub.persistence.repository import Repository


class Control:
  _skip_test = False
  _skip_reason = 'PostgreSQL not properly installed in host machine'

  def __init__(self):
    """
    Test
    setup
    :return: None
    """
    self._skip_test = False
    # Create test database
    dotenv_path = Path("{}/.local/etc/hub/.env".format(os.path.expanduser('~'))).resolve()
    if not dotenv_path.exists():
      self._skip_test = True
      self._skip_reason = f'.env file missing at {dotenv_path}'
      return
    dotenv_path = str(dotenv_path)
    repository = Repository(db_name='montreal_retrofit_test', app_env='TEST', dotenv_path=dotenv_path)
    engine = create_engine(repository.configuration.connection_string)
    try:
      # delete test database if it exists
      connection = engine.connect()
      connection.close()
    except ProgrammingError:
      logging.info('Database does not exist. Nothing to delete')
    except sqlalchemy.exc.OperationalError as operational_error:
      self._skip_test = True
      self._skip_reason = f'{operational_error}'
      return

    self._database = DBControl(
      db_name=repository.configuration.db_name,
      app_env='TEST',
      dotenv_path=dotenv_path)

    self._application_uuid = '60b7fc1b-f389-4254-9ffd-22a4cf32c7a3'
    self._application_id = 1
    self._user_id = 1
    self._pickle_path = 'tests_data/pickle_path.bz2'

  @property
  def database(self):
    return self._database

  @property
  def application_uuid(self):
    return self._application_uuid

  @property
  def application_id(self):
    return self._application_id

  @property
  def user_id(self):
    return self._user_id

  @property
  def skip_test(self):
    return self._skip_test

  @property
  def insel(self):
    return distutils.spawn.find_executable('insel')

  @property
  def sra(self):
    return distutils.spawn.find_executable('sra')

  @property
  def skip_insel_test(self):
    return self.insel is None

  @property
  def skip_reason(self):
    return self._skip_reason

  @property
  def message(self):
    return self._skip_reason

  @property
  def pickle_path(self):
    return self._pickle_path


control = Control()


class TestDBFactory(TestCase):
  """
TestDBFactory
"""

  @unittest.skipIf(control.skip_test, control.skip_reason)
  def test_buildings_info(self):
    request_values = {
      "buildings": [
        "01002777", "01002773", "01036804"
      ]
    }
    results = control.database.buildings_info(control.user_id, control.application_id, request_values)
    self.assertEqual(12, len(results), 'wrong number of results')
    print(results)
