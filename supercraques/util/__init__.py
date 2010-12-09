# coding: utf-8
#!/usr/bin/env python

def date_to_date_br(data=None):
    '''
    Transforma um tipo date em string no formato 'dd-mm-yyyy'
    Caso nao seja passado a data, retorna a data None.
    Ex: data_realizacao --> date(2009, 12, 25)
    * util.date_to_date_iso(data_realizacao) --> '25/12/2009'
    '''
    if data:
        return data.strftime('%d/%m/%Y')
    else:
        return None

def datetime_to_format(dataTime=None, format="%m/%d/%Y ÁS %IH%MMIN"):
    if dataTime:
        return dataTime.strftime(format)
    else:
        return None


    

#def lfind(haystack, needle):
#    '''Finds something inside a list and returns the indexes as a iterable generator. Use list(lfind(a,b)) to get result as a list.'''
#    z=-1
#    hs = list(map(lambda x: x.lower(), haystack))
#    nd = needle.lower()
#    while 1:
#        try:
#            z = hs.index(nd, z+1)
#            yield z
#        except:
#            break