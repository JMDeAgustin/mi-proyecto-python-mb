from sqlmodel import Session, select

from models.order import Order

def create_order(*, user_id: int, product_id: int,
                 quantity: int, session: Session) -> Order:
    order = Order(user_id=user_id, product_id=product_id, quantity=quantity)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

def list_orders_by_user(user_id: int, session: Session) -> list[Order]:
    return session.exec(select(Order).where(Order.user_id == user_id)).all()


def list_all_orders(session: Session) -> list[Order]:
    return session.exec(select(Order)).all()
