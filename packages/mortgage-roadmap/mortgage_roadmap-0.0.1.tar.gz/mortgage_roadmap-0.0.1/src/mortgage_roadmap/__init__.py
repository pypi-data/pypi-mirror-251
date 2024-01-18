# -*- coding: utf-8 -*-
""" mortgage_calculator: 
    =============================

    Repository that calculate the mortgage roadmap

    How it work:
    -----------

    Setters:
    --------

    Examples:
    ---------
    
    Content:
    --------

"""
__author__  = "Robert Rijnbeek"
__email__   = "robert270384@gmail.com"
__version__ = "0.0.1"

# ======== IMPORTS ===========

import sympy as sp

# ======= BASE FUNCTIONS =====

def mortgage_Constant_ChargeOff_Calculator(INITIAL_DEPT, QUOTAS, APR ):
    dept = INITIAL_DEPT
    quotas = QUOTAS
    charge_off = dept / quotas 
    percentage = APR

    dictionary = []
    for i in range(quotas):
        dept += -charge_off
        interest_pay = (dept * 0.01 * percentage) / 12
        topay = charge_off + interest_pay
        row = {"dept": dept, "charge_off": charge_off, "interest_pay": interest_pay, "topay": topay }
        dictionary.append(row)

    return dictionary

def mortgage_Constant_Pay_Calculator(INITIAL_DEPT, QUOTAS, APR):

    dept = sp.Float(INITIAL_DEPT)
    percentage = APR

    cuotes = QUOTAS

    dictionary = []
    topay = sp.Symbol('apargar')
    for i in range(cuotes):
        interest_pay = (dept * 0.01 * percentage) / 12
        charge_off = topay - interest_pay
        dept += -charge_off
        row = {"dept": dept, "charge_off": charge_off, "interest_pay": interest_pay, "topay": topay }
        dictionary.append(row)

    solve = sp.solveset(dept, topay)

    answere = float(solve.inf)


    for row in dictionary:
        row["charge_off"] = row["charge_off"].subs(topay,answere)
        row["dept"] = row["dept"].subs(topay,answere)
        row["interest_pay"] = row["interest_pay"].subs(topay,answere)
        row["topay"] = row["topay"].subs(topay,answere)

    return dictionary

if __name__ == '__main__':
    
    pass
