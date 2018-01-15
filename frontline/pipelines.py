

from frontline.db import session


class SQLAlchemyPipeline:

    def process_item(self, item, spider):
        """Save a database row.
        """
        session.add(item.row())

        try:
            session.commit()

        except Exception as e:
            session.rollback()
            print(e)

        return item
