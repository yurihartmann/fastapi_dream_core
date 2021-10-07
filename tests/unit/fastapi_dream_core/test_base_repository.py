import unittest

from sqlmodel import create_engine, SQLModel, Session

from fastapi_dream_core import Params, PaginationResult
from tests.resources.user.user_model import UserModel, CreateUserSchema, UpdateUserSchema
from tests.resources.user.user_repository import UserRepository


class TestBaseRepository(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(engine)
        self.session = Session(engine)
        self.user_repository = UserRepository(session=self.session)

    def __create_user_boo(self) -> UserModel:
        new_obj = UserModel(name='boo')
        self.session.add(new_obj)
        self.session.commit()
        self.session.refresh(new_obj)
        return new_obj

    def __create_user_foo(self):
        self.session.add(UserModel(name='foo'))
        self.session.commit()

    def __create_user(self, name):
        self.session.add(UserModel(name=name))
        self.session.commit()

    async def test_get_one_by_filters_with_filters(self):
        # Arrange
        self.__create_user_boo()
        self.__create_user_foo()

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
        self.__create_user_foo()

        # Act
        result = await self.user_repository.get_one_by_filters({
            'name': 'boo',
            'wrong_field': ''
        })

        # Assert
        self.assertIsNotNone(result)
        self.assertIsInstance(result, UserModel)
        self.assertEqual(result.name, 'boo')

    async def test_get_one_by_filters_with_filters_wrong_type(self):
        # Arrange
        self.__create_user_boo()
        self.__create_user_foo()

        # Act and Assert
        with self.assertRaises(ValueError):
            await self.user_repository.get_one_by_filters(filters=['boo'])

    async def test_get_one_by_filters_without_data_and_without_filters(self):
        # Arrange

        # Act
        result = await self.user_repository.get_one_by_filters()

        # Assert
        self.assertIsNone(result)

    async def test_find_by_filters_paginated_first_page(self):
        # Arrange
        for _ in range(15):
            self.__create_user_boo()
            self.__create_user_foo()

        # Act
        result = await self.user_repository.find_by_filters_paginated(
            filters={
                'name': 'boo',
                'wrong_field': ''
            },
            params=Params(size=10)
        )

        # Assert
        self.assertIsInstance(result, PaginationResult)
        self.assertEqual(10, len(result.items))
        self.assertEqual(15, result.count)

    async def test_find_by_filters_paginated_second_page(self):
        # Arrange
        for _ in range(15):
            self.__create_user_boo()
            self.__create_user_foo()

        # Act
        result = await self.user_repository.find_by_filters_paginated(
            filters={
                'name': 'boo',
                'wrong_field': ''
            },
            params=Params(size=10, page=2)
        )

        # Assert
        self.assertIsInstance(result, PaginationResult)
        self.assertEqual(5, len(result.items))
        self.assertEqual(15, result.count)

    async def test_find_by_filters_paginated_with_desc(self):
        # Arrange
        for _ in range(15):
            self.__create_user_boo()

        for _ in range(15):
            self.__create_user_foo()

        # Act
        result = await self.user_repository.find_by_filters_paginated(
            filters={
                'name': 'boo',
                'wrong_field': ''
            },
            params=Params(size=10, page=1),
            desc=True
        )

        # Assert
        self.assertIsInstance(result, PaginationResult)
        self.assertEqual(10, len(result.items))
        self.assertEqual(15, result.items[0].id)

    async def test_find_by_filters_paginated_sending_invalid_params(self):
        # Arrange
        for _ in range(15):
            self.__create_user_boo()

        # Act and Assert
        with self.assertRaises(ValueError):
            await self.user_repository.find_by_filters_paginated(
                filters={
                    'name': 'boo',
                    'wrong_field': ''
                },
                params=None
            )

    async def test_find_all_by_filters(self):
        # Arrange
        for _ in range(15):
            self.__create_user_boo()

        # Act
        result = await self.user_repository.find_all_by_filters(
            filters={
                'name': 'boo',
                'wrong_field': ''
            }
        )

        # Assert
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], UserModel)
        self.assertEqual(result[0].name, 'boo')
        self.assertEqual(result[0].id, 1)

    async def test_find_all_by_filters_with_desc(self):
        # Arrange
        for _ in range(15):
            self.__create_user_boo()

        # Act
        result = await self.user_repository.find_all_by_filters(
            filters={
                'name': 'boo',
                'wrong_field': ''
            },
            desc=True
        )

        # Assert
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], UserModel)
        self.assertEqual(result[0].name, 'boo')
        self.assertEqual(result[0].id, 15)

    async def test_count_by_filters(self):
        # Arrange
        for _ in range(15):
            self.__create_user_boo()
            self.__create_user_foo()

        # Act
        result = await self.user_repository.count_by_filters(
            filters={
                'name': 'boo',
                'wrong_field': ''
            }
        )

        # Assert
        self.assertIsInstance(result, int)
        self.assertEqual(15, result)

    async def test_create(self):
        # Arrange
        create_user_schema = CreateUserSchema(
            name='test', age=18
        )

        # Act
        result = await self.user_repository.create(
            obj_in=create_user_schema
        )

        # Assert
        self.assertIsInstance(result, UserModel)
        self.assertEqual('test', result.name)
        self.assertEqual(18, result.age)

    async def test_update_with_obj(self):
        # Arrange
        db_user = self.__create_user_boo()
        user_update_schema = UpdateUserSchema(name='new name', age=30)

        # Act
        result = await self.user_repository.update(
            db_obj=db_user,
            obj_in=user_update_schema
        )

        # Assert
        self.assertIsInstance(result, UserModel)
        self.assertEqual('new name', result.name)
        self.assertEqual(30, result.age)

    async def test_update_with_dict(self):
        # Arrange
        db_user = self.__create_user_boo()

        # Act
        result = await self.user_repository.update(
            db_obj=db_user,
            obj_in={
                'name': 'boo2',
                'wrong_field': 1212
            }
        )

        # Assert
        self.assertIsInstance(result, UserModel)
        self.assertEqual('boo2', result.name)

    async def test_delete(self):
        # Arrange
        db_user = self.__create_user_boo()
        id_user = db_user.id

        # Act
        await self.user_repository.delete(
            obj=db_user
        )

        # Assert
        self.assertEqual(0, await self.user_repository.count_by_filters(filters={'id': id_user}))
