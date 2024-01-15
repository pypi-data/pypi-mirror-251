import importlib

from lesscode.db.sqlalchemy.sqlalchemy_helper import SqlAlchemyHelper, result_to_json


class SQLAlchemyModelBaseService:
    __model__ = ""
    __connect_name__ = ""

    @classmethod
    def find_one(cls, _id, find_column: list = None):
        try:
            sqlalchemy = importlib.import_module("sqlalchemy")
        except ImportError:
            raise Exception(f"sqlalchemy is not exist,run:pip install sqlalchemy==1.4.36")
        filters = [cls.__model__.id == _id]
        with SqlAlchemyHelper(cls.__connect_name__).make_session() as session:
            if not find_column:
                statement = sqlalchemy.select(cls.__model__).where(*filters)
                res = session.execute(statement).scalars().first() or {}
                res = result_to_json(res)
            else:
                statement = sqlalchemy.select(*[sqlalchemy.column(_) for _ in find_column]).where(*filters)
                res = session.execute(statement).first() or {}
                res = result_to_json(res)
            return res

    @classmethod
    def find_page(cls, filter_field_list: list = None, find_column: list = None, sort_list: list = None,
                  page_num: int = 1, page_size: int = 10):
        try:
            sqlalchemy = importlib.import_module("sqlalchemy")
        except ImportError:
            raise Exception(f"sqlalchemy is not exist,run:pip install sqlalchemy==1.4.36")
        try:
            sqlalchemy_utils = importlib.import_module("lesscode_utils.sqlalchemy_utils")
        except ImportError:
            raise Exception(f"lesscode_utils is not exist,run:pip install lesscode_utils==0.0.48")

        filters = []
        if filter_field_list:
            for field in filter_field_list:
                _column = field.get('column')
                _value = field.get('value')
                _end_value = field.get('end_value')
                # ["in","like","between","not in","not like","is null","not null","not in list","eq","=","not eq","!=","gt",">","gte",">=","lt","<","lte",">="]
                _relation = field.get('relation', "in")
                _position = field.get('position', "LR")
                sqlalchemy_utils.condition_by_relation(filters, cls.__model__, _column, _relation, _value, _end_value,
                                                       _position)
        sort_list = sort_list or []
        sort_list = sqlalchemy_utils.single_model_format_order(cls.__model__, sort_list)
        result = {
            "data_list": [],
            "data_count": 0
        }
        with SqlAlchemyHelper(cls.__connect_name__).make_session() as session:
            if not find_column:
                statement = sqlalchemy.select(cls.__model__).where(*filters)
                if sort_list:
                    statement = statement.order_by(*sort_list)
                statement = statement.offset((page_num - 1) * page_size).limit(page_size)
                res = session.execute(statement).scalars().all()
            else:
                statement = sqlalchemy.select(*[sqlalchemy.column(_) for _ in find_column]).select_from(
                    cls.__model__).where(*filters)
                if sort_list:
                    statement = statement.order_by(*sort_list)
                statement = statement.offset((page_num - 1) * page_size).limit(page_size)
                res = session.execute(statement).all()
            result["data_list"] = result_to_json(res)

            total_count_statement = sqlalchemy.select(sqlalchemy.func.count()).select_from(cls.__model__).filter(
                *filters)
            total_count_res = session.execute(total_count_statement).scalar()
            result["data_count"] = total_count_res
            return result

    @classmethod
    def find_all(cls, filter_field_list: list = None, find_column: list = None, sort_list: list = None):
        try:
            sqlalchemy = importlib.import_module("sqlalchemy")
        except ImportError:
            raise Exception(f"sqlalchemy is not exist,run:pip install sqlalchemy==1.4.36")
        try:
            sqlalchemy_utils = importlib.import_module("lesscode_utils.sqlalchemy_utils")
        except ImportError:
            raise Exception(f"lesscode_utils is not exist,run:pip install lesscode_utils==0.0.48")
        filters = []
        if filter_field_list:
            for field in filter_field_list:
                _column = field.get('column')
                _value = field.get('value')
                _end_value = field.get('end_value')
                # ["in","like","between","not in","not like","is null","not null","not in list","eq","=","not eq","!=","gt",">","gte",">=","lt","<","lte",">="]
                _relation = field.get('relation', "in")
                _position = field.get('position', "LR")
                sqlalchemy_utils.condition_by_relation(filters, cls.__model__, _column, _relation, _value, _end_value,
                                                       _position)
        sort_list = sort_list or []
        sort_list = sqlalchemy_utils.single_model_format_order(cls.__model__, sort_list)
        with SqlAlchemyHelper(cls.__connect_name__).make_session() as session:
            if not find_column:
                statement = sqlalchemy.select(cls.__model__).where(*filters)
                if sort_list:
                    statement = statement.order_by(*sort_list)
                res = session.execute(statement).scalars().all()
            else:
                statement = sqlalchemy.select(*[sqlalchemy.column(_) for _ in find_column]).select_from(
                    cls.__model__).where(*filters)
                if sort_list:
                    statement = statement.order_by(*sort_list)
                res = session.execute(statement).all()
            return result_to_json(res)

    @classmethod
    def save(cls, data: dict, primary_key="id"):
        try:
            sqlalchemy = importlib.import_module("sqlalchemy")
        except ImportError:
            raise Exception(f"sqlalchemy is not exist,run:pip install sqlalchemy==1.4.36")
        with SqlAlchemyHelper(cls.__connect_name__).make_session() as session:
            statement = sqlalchemy.insert(cls.__model__).values(**data)
            res = session.execute(statement)
            last_id = res.lastrowid if primary_key not in data else data.get(primary_key)
            return last_id

    @classmethod
    def bulk_save(cls, data: list):
        try:
            sqlalchemy = importlib.import_module("sqlalchemy")
        except ImportError:
            raise Exception(f"sqlalchemy is not exist,run:pip install sqlalchemy==1.4.36")
        with SqlAlchemyHelper(cls.__connect_name__).make_session() as session:
            statement = sqlalchemy.insert(cls.__model__).values(data)
            res = session.execute(statement)
            return res.rowcount

    @classmethod
    def delete(cls, _id: str):
        try:
            sqlalchemy = importlib.import_module("sqlalchemy")
        except ImportError:
            raise Exception(f"sqlalchemy is not exist,run:pip install sqlalchemy==1.4.36")
        with SqlAlchemyHelper(cls.__connect_name__).make_session() as session:
            statement = sqlalchemy.delete(cls.__model__).where(cls.__model__.id == _id)
            res = session.execute(statement)
            return res.rowcount

    @classmethod
    def bulk_delete(cls, filter_field_list: list = None):
        try:
            sqlalchemy = importlib.import_module("sqlalchemy")
        except ImportError:
            raise Exception(f"sqlalchemy is not exist,run:pip install sqlalchemy==1.4.36")
        try:
            sqlalchemy_utils = importlib.import_module("lesscode_utils.sqlalchemy_utils")
        except ImportError:
            raise Exception(f"lesscode_utils is not exist,run:pip install lesscode_utils==0.0.48")
        filters = []
        if filter_field_list:
            for field in filter_field_list:
                _column = field.get('column')
                _value = field.get('value')
                _end_value = field.get('end_value')
                # ["in","like","between","not in","not like","is null","not null","not in list","eq","=","not eq","!=","gt",">","gte",">=","lt","<","lte",">="]
                _relation = field.get('relation', "in")
                _position = field.get('position', "LR")
                sqlalchemy_utils.condition_by_relation(filters, cls.__model__, _column, _relation, _value, _end_value,
                                                       _position)
        with SqlAlchemyHelper(cls.__connect_name__).make_session() as session:
            statement = sqlalchemy.delete(cls.__model__).where(*filters)
            res = session.execute(statement)
            return res.rowcount

    @classmethod
    def update(cls, _id: str, params: dict):
        try:
            sqlalchemy = importlib.import_module("sqlalchemy")
        except ImportError:
            raise Exception(f"sqlalchemy is not exist,run:pip install sqlalchemy==1.4.36")
        with SqlAlchemyHelper(cls.__connect_name__).make_session() as session:
            statement = sqlalchemy.update(cls.__model__).where(
                cls.__model__.id == _id).values(
                **params)
            res = session.execute(statement)
            return res.rowcount

    @classmethod
    def bulk_update(cls, data: list):
        with SqlAlchemyHelper(cls.__connect_name__).make_session() as session:
            session.bulk_update_mappings(cls.__model__, data)
