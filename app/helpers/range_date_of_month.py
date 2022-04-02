from datetime import datetime
from app.default import data_month
from http import HTTPStatus


class RangeDatesMonth:
    def __init__(self, initial: str, the_end: str) -> None:
        self.initial = initial
        self.the_end = the_end


def range_date_of_month(
    date_now: datetime = datetime.today(), month: int or bool = False
) -> RangeDatesMonth:
    """
    Essa função recebe a data atual e retorna o primeiro dia do mês e o último. Não considera ano bissexto.
    return ```{"initial": str,"the_end": str}```
    """
    try:
        if not month:
            month: str = (
                f"0{date_now.month}" if date_now.month < 10 else str(date_now.month)
            )
        str_date_now = str(date_now)
        dates_of_month = RangeDatesMonth(
            **{
                "initial": f"{str_date_now[:-2]}{data_month[month][0]}",
                "the_end": f"{str_date_now[:-2]}{data_month[month][1]}",
            }
        )
        return dates_of_month
    except KeyError as e:
        return {"error": "invalid month."}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e
