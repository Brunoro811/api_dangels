import datetime
from app.default import data_month
from http import HTTPStatus


def normalize_month(month: str) -> str:
    """
    Esta função recebe um campo month e se for menor que 10 é acrescentado o 0 na frente. Exemplo : month = '8' returnado '08'.
    """
    return f"0{int(month)}" if int(month) < 10 else str(month)


class RangeDatesMonth:
    def __init__(self, initial: str, the_end: str) -> None:
        self.initial = initial
        self.the_end = the_end


def range_date_of_month(month: int or bool = False) -> RangeDatesMonth:
    """
    Essa função recebe a data atual e retorna o primeiro dia do mês e o último. Não considera ano bissexto.
    return ```{ "initial": str,"the_end": str }```
    """
    try:
        date_now: datetime.date = datetime.date.today()
        str_date_now = str(date_now)
        month = month if month else date_now.month
        month = normalize_month(month)

        dates_of_month = RangeDatesMonth(
            **{
                "initial": f"{str_date_now[:-5]}{month}-{data_month[month][0]}",
                "the_end": f"{str_date_now[:-5]}{month}-{data_month[month][1]}",
            }
        )

        return dates_of_month
    except KeyError as e:
        return {"error": "invalid month."}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        raise e
