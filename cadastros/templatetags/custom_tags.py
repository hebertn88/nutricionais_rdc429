from django import template

register = template.Library()

def multMil(value, arg):
    return int(value * arg)

register.filter('multMil', multMil)

def qtdPerCent(value, arg):
    return (value / arg) * .1

register.filter('qtdPerCent', qtdPerCent)

def arredRotulo(value : float | int , arg : str = 'g') -> float | int :
    if value < 1:
        s_int, s_dec = splitVal(value)
        match arg:
            case 'g':
                if int(s_dec[1]) >= 5:
                    value = str(value + .1)[:3]
                    value = float(value)
                else:
                    value = str(value)[:3]
                    value = float(value)
            case 'mg':
                if int(s_dec[2]) >= 5:
                    value = str(value + .01)
                    value = float(value)

                s_int, s_dec = splitVal(value)
                if s_dec[1] == '0':
                    value = str(value)[:3]
                    value = float(value)
                else:
                    value = str(value)[:4]
                    value = float(value)
        if value == 0:
            value = int(0)
    
    if 1 <= value < 10:
        s_int, s_dec = splitVal(value)

        if int(s_dec[1]) >= 5:
            value += .1
            
        s_int, s_dec = splitVal(value)
        if s_dec[0] == '0':
            value = int(value)
        else:
            s_dec = s_dec[:2]
            value = float(s_int + '.' + s_dec)
    
    if value >= 10:
        s_int, s_dec = splitVal(value)

        if int(s_dec[0]) >= 5:
            value += 1

        value = int(value)
        
    return value

def splitVal(value : float | int ) -> str :
    if value % 1 != 0:
        si, sd = str(value).split('.')
    else:
        si = str(int(value))
        sd = '0'

    sd = sd.rjust(3,'0')
    return si, sd

register.filter('arredRotulo', arredRotulo)