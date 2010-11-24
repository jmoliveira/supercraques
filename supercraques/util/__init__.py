def date_to_date_br(data=None):
    '''
    Transforma um tipo date em string no formato 'dd-mm-yyyy'
    Caso nao seja passado a data, retorna a data None.
    Ex: data_realizacao --> date(2009, 12, 25)
    * util.date_to_date_iso(data_realizacao) --> '25/12/2009'
    '''
    if data:
        return data.strftime('%d-%m-%Y')
    else:
        return None
