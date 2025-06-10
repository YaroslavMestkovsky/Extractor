from app.models import Specialist
from app.models import Deal, Contract


DEALS = {
    column.comment: column.name
    for column in Deal.__table__.columns
    if column.comment is not None
}

CONTRACTS = {
    column.comment: column.name
    for column in Contract.__table__.columns
    if column.comment is not None
}

SPECIALISTS = {
    column.comment: column.name
    for column in Specialist.__table__.columns
    if column.comment is not None
}
