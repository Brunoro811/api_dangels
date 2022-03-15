from app.errors import FieldMissingError, InvalidValueTypesError


def payload_eval(
    data: dict, optional: list = [], not_empty_string: list = [], **kwargs
) -> dict:
    """Avalia o payload em existência, opcionalidade e tipo de campo. Retorna\n
    um dicionário contendo os campos que foram informados como argumentos\n
    nomeados, ou seja, ignora os campos excedentes.
        `data` - o payload recebido
        `optional` - lista com os nomes dos campos opcionais
        `kwargs` - campos possíveis para a requisição. Seus valores\n
            correspondem ao tipo de dado permitido para aquele campo.
    Todos os campos permitidos à requisição devem ser passados como\n
    argumentos nomeados, recebendo como valor os tipo correspondente::
        payload_eval(
            data=payload,
            name=str,
            price=float,
            description=str,
            opitonal=['description'],
        )
    Exceções:
        `app.errors.FieldMissingError` - Campo obrigatório não informado.\n
    Se o campo não fornecido estiver na lista de opcionais, a exceção mão\n
    é levantada.
        `app.errors.InvalidValueTypesError` - Há campos cujo tipo não\n
    não coresponde ao informado nos argumentos nomeados.
    """

    # Verifica se um campo string possui um valor vazio e substitui por None
    # caso esse campo seja informado na lista not_nullable
    data = {
        key: value
        if type(value) != str
        else value
        if key not in not_empty_string
        else value
        if value != ""
        else None
        for key, value in data.items()
    }

    missing_keys = [
        key for key in kwargs.keys() if key not in data.keys() if key not in optional
    ]

    if set(missing_keys).difference(optional):
        msg = {"msg": f"required fields missing {missing_keys}"}
        raise FieldMissingError(description=msg)

    invalid_types_list = []
    for field_name, value_type in kwargs.items():

        if field_name in data.keys():

            if type(value_type) == list:
                invalid_types_list = []
                for element in value_type:

                    if type(data[field_name]) != element:
                        invalid_types_list.append(data[field_name])
                    else:
                        invalid_types_list = []
                        break
            elif type(data[field_name]) != value_type:
                invalid_types_list.append(data[field_name])

    if invalid_types_list:
        msg = {"msg": f"invalid keys values {invalid_types_list}"}
        raise InvalidValueTypesError(description=msg)

    return {key: data[key] for key in kwargs.keys() if key in data.keys()}
