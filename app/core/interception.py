from sqlalchemy import event
from sqlalchemy.orm import Session


class Interception:
    @staticmethod
    @event.listens_for(Session, "before_update")
    def before_update(session, instance):
        print("before_update")
        print(instance)

    @staticmethod
    @event.listens_for(Session, "before_insert")
    def before_insert(session, instance):
        print("before_insert")
        print(instance)

    @staticmethod
    @event.listens_for(Session, "before_attach")
    def before_attach(session, instance):
        print("before_attach")
        print(instance)
