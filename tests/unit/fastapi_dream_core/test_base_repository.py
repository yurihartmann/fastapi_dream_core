import unittest

from sqlmodel import create_engine, SQLModel, Session

from tests.resources.user_model import UserModel
from tests.resources.user_repository import UserRepository


class TestBaseRepository(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(engine)
        self.session = Session(engine)
        self.user_repository = UserRepository(session=self.session)

    def __create_user_boo(self):
        self.session.add(UserModel(name='boo'))
        self.session.commit()

    async def test_get_one_by_filters_with_filters(self):
        # Arrange
        self.__create_user_boo()

        # Act
        result = await self.user_repository.get_one_by_filters({
            'name': 'boo'
        })

        # Assert
        self.assertIsNotNone(result)
        self.assertIsInstance(result, UserModel)
        self.assertEqual(result.name, 'boo')

    async def test_get_one_by_filters_with_filters_wrongs(self):
        # Arrange
        self.__create_user_boo()

        # Act
        result = await self.user_repository.get_one_by_filters({
            'name': 'boo',
            'alo': ''
        })

        # Assert
        self.assertIsNotNone(result)
        self.assertIsInstance(result, UserModel)
        self.assertEqual(result.name, 'boo')

    async def test_get_one_by_filters_without_data_and_without_filters(self):
        # Arrange

        # Act
        result = await self.user_repository.get_one_by_filters()

        # Assert
        self.assertIsNone(result)
