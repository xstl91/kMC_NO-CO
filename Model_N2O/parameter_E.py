from .constant import Surface,EV


# BEP relation: activation energy (J), slope, reaction energy (J), slope for reaction energy difference
E_act = { x:{} for x in ('form','back','trans','dis','des') }
if Surface == '100':
    E_act['form']['N2O']  = { 'NNbhb'       : (1.022*EV, 0.44,  0.884*EV, 0.48)}
    E_act['back']['N2O']  = { 'NNbhb'       : (0.138*EV, 0.04, -0.884*EV, 0.48)}
    E_act['trans']['N2O'] = { 'NNbhb-flat'  : (0.127*EV, 0.42,  0.019*EV, 0.78),
                              'flat-NNbhb'  : (0.108*EV, 0.36, -0.019*EV, 0.78),
                              'flat-NOtbt'  : (0.250*EV, 0.45,  0.158*EV, 0.76),
                              'NOtbt-flat'  : (0.092*EV, 0.31, -0.158*EV, 0.76),
                              'flat-NOtht'  : (0.354*EV, 0.48,  0.293*EV, 0.51),
                              'NOtht-flat'  : (0.061*EV, 0.03, -0.293*EV, 0.51),
                              'NNbhb-NNtbt' : (0.286*EV, 0.51,  0.215*EV, 0.72),
                              'NNtbt-NNbhb' : (0.071*EV, 0.21, -0.215*EV, 0.72),
                              'NNtbt-top'   : (0.271*EV, 0.86, -0.131*EV, 1.53),
                              'top-NNtbt'   : (0.402*EV, 0.67,  0.131*EV, 1.53),
                              'top-NOtbt'   : (0.372*EV, 0.71,  0.103*EV, 1.41),
                              'NOtbt-top'   : (0.269*EV, 0.70, -0.103*EV, 1.41),
                              'top-NOtht'   : (0.391*EV, 0.92,  0.254*EV, 1.69),
                              'NOtht-top'   : (0.137*EV, 0.77, -0.254*EV, 1.69)}
    E_act['dis']['N2O']   = { 'flat-u'      : (0.185*EV, 0.23, -1.724*EV, 0.78),
                              'flat-d'      : (0.303*EV, 0.17, -1.725*EV, 0.78),
                              'NOtbt'       : (0.074*EV, 0.10, -1.876*EV, 0.73),
                              'NOtht'       : (0.060*EV, 0.06, -2.032*EV, 0.80)}
    E_act['des']['N2O']   = { 'top'         : (0.181*EV, 0.30,  0.122*EV,-0.02)}
if Surface == '111':
    E_act['form']['N2O']  = { 'NNbftt'      : (1.580*EV, 0.49,  1.173*EV, 0.56),
                              'NNbhtt'      : (1.416*EV, 0.45,  1.060*EV, 0.59)}
    E_act['back']['N2O']  = { 'NNbftt'      : (0.407*EV, 0.08, -1.173*EV, 0.56),
                              'NNbhtt'      : (0.356*EV, 0.14, -1.060*EV, 0.59)}
    E_act['trans']['N2O'] = { 'NNbftt-NNtbt': (0.115*EV, 0.51,  0.059*EV, 1.19),
                              'NNtbt-NNbftt': (0.056*EV, 0.67, -0.059*EV, 1.19),
                              'NNbhtt-NNtbt': (0.141*EV, 0.50,  0.080*EV, 1.17),
                              'NNtbt-NNbhtt': (0.061*EV, 0.68, -0.080*EV, 1.17),
                              'NNtbt-top'   : (0.211*EV, 0.35, -0.279*EV, 0.68),
                              'top-NNtbt'   : (0.490*EV, 0.33,  0.279*EV, 0.68),
                              'top-NOtbt'   : (0.447*EV, 0.20,  0.251*EV, 0.60),
                              'NOtbt-top'   : (0.196*EV, 0.40, -0.251*EV, 0.60),
                              'NOtbt-NObft' : (0.186*EV, 0.20,  0.179*EV, 0.26),
                              'NObft-NOtbt' : (0.007*EV, 0.06, -0.179*EV, 0.26),
                              'NOtbt-NObht' : (0.203*EV, 0.27,  0.197*EV, 0.33),
                              'NObht-NOtbt' : (0.006*EV, 0.06, -0.197*EV, 0.33)}
    E_act['dis']['N2O']   = { 'NOtbt-f'     : (0.132*EV, 0.16, -2.268*EV, 1.02),
                              'NOtbt-h'     : (0.145*EV, 0.10, -2.198*EV, 0.87)}
    E_act['des']['N2O']   = { 'top'         : (0.163*EV, 0.37,  0.065*EV, 0.14)}
