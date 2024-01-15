import pandas, numpy, tabulate 
from scipy.stats import spearmanr
from sklearn.isotonic import IsotonicRegression as isoreg
from sklearn.cluster import KMeans as kmeans
from sklearn.ensemble import HistGradientBoostingRegressor as gbmreg


########## 01. cal_woe() ########## 

def cal_woe(x, bin):
  """
  The function applies the woe transformation to a numeric vector based on 
  the binning outcome.
  Parameters:
    x   : A numeric vector, which can be a list, numpy array, or pandas series;
    bin : An object containing the binning outcome.
  Returns:
    A list of dictionaries with three keys
  """

  _cut = sorted([_ for _ in bin['cut']] + [numpy.PINF, numpy.NINF])
  _dat = [[_1[0], _1[1], _2] for _1, _2 in zip(enumerate(x), ~numpy.isnan(x))]

  _m1 = [_[:2] for _ in _dat if _[2] == 0]
  _l1 = [_[:2] for _ in _dat if _[2] == 1]
  _l2 = [[*_1, _2] for _1, _2 in zip(_l1, numpy.searchsorted(_cut, [_[1] for _ in _l1]).tolist())]

  flatten = lambda l: [item for subl in l for item in subl]
 
  _l3 = flatten([[[*l, b['woe']] for l in _l2 if l[2] == b['bin']] for b in bin['tbl'] if b['bin'] > 0])

  if len(_m1) > 0:
    if len([_ for _ in bin['tbl'] if _['miss'] > 0]) > 0:
      _m2 = [l + [_['bin'] for _ in bin['tbl'] if _['miss'] > 0] 
               + [_['woe'] for _ in bin['tbl'] if _['miss'] > 0] for l in _m1]
    else:
      _m2 = [l + [0, 0] for l in _m1]
    _l3.extend(_m2)

  _key = ["x", "bin", "woe"]
  return(list(dict(zip(_key, _[1:])) for _ in sorted(_l3, key = lambda x: x[0])))


########## 02. summ_bin() ########## 

def summ_bin(x):
  """
  The function summarizes the outcome generated from a binning function, e.g. qtl_bin().
  Parameters:
    x: An object containing the binning outcome.
  Returns:
    A dictionary with statistics derived from the binning outcome
  """

  _freq = sum(_['freq'] for _ in x['tbl'])
  _bads = sum(_['bads'] for _ in x['tbl'])
  _miss = sum(_['miss'] for _ in x['tbl'])

  _iv = round(sum(_['iv'] for _ in x['tbl']), 4)
  _ks = round(max(_["ks"] for _ in x["tbl"]), 2)

  _br = round(_bads / _freq, 4)
  _mr = round(_miss / _freq, 4)
  return({"sample size": _freq, "bad rate": _br, "iv": _iv, "ks": _ks, "missing": _mr})


########## 03. view_bin() ########## 

def view_bin(x):
  """
  The function displays the outcome generated from a binning function, e.g. qtl_bin().
  Parameters:
    x: An object containing the binning outcome.
  Returns:
    None
  """

  tabulate.PRESERVE_WHITESPACE = True

  _sel = ["bin", "freq", "miss", "bads", "rate", "woe", "iv", "ks"]
  _tbl = [{**(lambda v: {k: v[k] for k in _sel})(_), "rule": _["rule"].ljust(45)} for _ in x["tbl"]]

  print(tabulate.tabulate(_tbl, headers = "keys", tablefmt = "github", 
                          colalign = ["center"] + ["right"] * 7 + ["center"],
                          floatfmt = (".0f", ".0f", ".0f", ".0f", ".4f", ".4f", ".4f", ".2f")))


########## 04. qcut() ##########

def qcut(x, n):
  """
  The function discretizes a numeric vector into n pieces based on quantiles.
  Parameters:
    x : A numeric vector.
    n : An integer indicating the number of categories to discretize.
  Returns:
    A list of numeric values to divide the vector x into n categories.
  """

  _q = numpy.linspace(0, 100, n, endpoint = False)[1:]
  _x = [_ for _ in x if not numpy.isnan(_)]
  return(numpy.unique(numpy.percentile(_x, _q, method = "lower")))


########## 05. manual_bin() ##########

def manual_bin(x, y, cuts):
  """
  The function discretizes the x vector and then summarizes over the y vector
  based on the discretization result.
  Parameters:
    x    : A numeric vector to discretize without missing values, 
           e.g. numpy.nan or math.nan
    y    : A numeric vector with binary values of 0/1 and with the same length 
           of x
    cuts : A list of numeric values as cut points to discretize x.
  Returns:
    A list of dictionaries for the binning outcome. 
  """

  _c = sorted([_ for _ in set(cuts)] + [numpy.NINF, numpy.PINF])
  _g = numpy.searchsorted(_c, x).tolist()

  _l1 = sorted(zip(_g, x, y), key = lambda x: x[0])
  _l2 = zip(set(_g), [[l for l in _l1 if l[0] == g] for g in set(_g)])

  return(sorted([dict(zip(["bin", "freq", "miss", "bads", "minx", "maxx"],
                          [_1, len(_2), 0,
                           sum([_[2] for _ in _2]),
                           min([_[1] for _ in _2]),
                           max([_[1] for _ in _2])])) for _1, _2 in _l2],
                key = lambda x: x["bin"]))


########## 06. miss_bin() ##########

def miss_bin(y):
  """
  The function summarizes the y vector with binary values of 0/1 and is not 
  supposed to be called directly by users.
  Parameters:
    y : A numeric vector with binary values of 0/1.
  Returns:
    A dictionary.
  """

  return({"bin": 0, "freq": len([_ for _ in y]), "miss": len([_ for _ in y]), 
          "bads": sum([_ for _ in y]), "minx": numpy.nan, "maxx": numpy.nan})


########## 07. gen_rule() ##########

def gen_rule(tbl, pts):
  """
  The function generates binning rules based on the binning outcome table and
  a list of cut points and is an utility function that is not supposed to be 
  called directly by users.
  Parameters:
    tbl : A intermediate table of the binning outcome within each binning 
          function
    pts : A list cut points for the binning
  Returns:
    A list of dictionaries with binning rules 
  """

  for _ in tbl:
    if _["bin"] == 0:
      _["rule"] = "numpy.isnan($X$)"
    elif _["bin"] == len(pts) + 1:
      if _["miss"] == 0:
        _["rule"] = "$X$ > " + str(pts[-1])
      else:
        _["rule"] = "$X$ > " + str(pts[-1]) + " or numpy.isnan($X$)"
    elif _["bin"] == 1:
      if _["miss"] == 0:
        _["rule"] = "$X$ <= " + str(pts[0])
      else:
        _["rule"] = "$X$ <= " + str(pts[0]) + " or numpy.isnan($X$)"
    else:
        _["rule"] = "$X$ > " + str(pts[_["bin"] - 2]) + " and $X$ <= " + str(pts[_["bin"] - 1])

  _sel = ["bin", "freq", "miss", "bads", "rate", "woe", "iv", "ks", "rule"]

  return([{k: _[k] for k in _sel} for _ in tbl])


########## 08. gen_woe() ##########

def gen_woe(x):
  """
  The function calculates weight of evidence and information value based on the 
  binning outcome within each binning function and is an utility function that 
  is not supposed to be called directly by users.
  Parameters:
    x : A list of dictionaries for the binning outcome.
  Returns:
    A list of dictionaries with additional keys to the input.
  """

  _freq = sum(_["freq"] for _ in x)
  _bads = sum(_["bads"] for _ in x)

  _l1 = sorted([{**_, 
                 "rate": round(_["bads"] / _["freq"], 4),
                 "woe" : round(numpy.log((_["bads"] / _bads) / ((_["freq"] - _["bads"]) / (_freq - _bads))), 4),
                 "iv"  : round((_["bads"] / _bads - (_["freq"] - _["bads"]) / (_freq - _bads)) *
                               numpy.log((_["bads"] / _bads) / ((_["freq"] - _["bads"]) / (_freq - _bads))), 4)
                } for _ in x], key = lambda _x: _x["bin"])

  cumsum = lambda x: [sum([_ for _ in x][0:(i + 1)]) for i in range(len(x))]

  _cumb = cumsum([_['bads'] / _bads for _ in _l1])
  _cumg = cumsum([(_['freq'] - _['bads']) / (_freq - _bads) for _ in _l1])
  _ks = [round(numpy.abs(_[0] - _[1]) * 100, 2) for _ in zip(_cumb, _cumg)]
  
  return([{**_1, "ks": _2} for _1, _2 in zip(_l1, _ks)])


########## 09. add_miss() ##########

def add_miss(d, l):
  """
  The function appends missing value category, if any, to the binning outcome 
  and is an utility function and is not supposed to be called directly by 
  the user.  
  Parameters:
    d : A list with lists generated by input vectors of binning functions.
    l : A list of dicts.
  Returns:
    A list of dicts.
  """

  _l = l[:]

  if len([_ for _ in d if _[2] == 0]) > 0:
    _m = miss_bin([_[1] for _ in d if _[2] == 0])
    if _m["bads"] == 0:
      for _ in ['freq', 'miss', 'bads']:
        _l[0][_]  = _l[0][_]  + _m[_]
    elif _m["freq"] == _m["bads"]:
      for _ in ['freq', 'miss', 'bads']:
        _l[-1][_]  = _l[-1][_]  + _m[_]
    else:
      _l.append(_m)

  return(_l)


########## 10. qtl_bin() ##########

def qtl_bin(x, y):
  """
  The function discretizes the x vector based on percentiles and summarizes 
  over the y vector to derive weight of evidence transformaton (WoE) and 
  information value.
  Parameters:
    x : A numeric vector to discretize. It can be a list, 1-D numpy array, or 
        pandas series.
    y : A numeric vector with binary values of 0/1 and with the same length 
        of x. It can be a list, 1-D numpy array, or pandas series.
  Returns:
    A dictionary with two keys:
      "cut" : A numeric vector with cut points applied to the x vector.
      "tbl" : A list of dictionaries summarizing the binning outcome.
  """

  _data = [_ for _ in zip(x, y, ~numpy.isnan(x))]
  _x = [_[0] for _ in _data if _[2] == 1]
  _y = [_[1] for _ in _data if _[2] == 1]

  _n = numpy.arange(2, max(3, min(50, len(numpy.unique(_x)) - 1)))
  _p = set(tuple(qcut(_x, _)) for _ in _n)

  _l1 = [[_, manual_bin(_x, _y, _)] for _ in _p]

  _l2 = [[l[0], 
          min([_["bads"] / _["freq"] for _ in l[1]]), 
          max([_["bads"] / _["freq"] for _ in l[1]]),
          spearmanr([_["bin"] for _ in l[1]], [_["bads"] / _["freq"] for _ in l[1]])[0]
         ] for l in _l1]

  _l3 = [l[0] for l in sorted(_l2, key = lambda x: -len(x[0]))
         if numpy.abs(round(l[3], 8)) == 1 and round(l[1], 8) > 0 and round(l[2], 8) < 1][0]

  _l4 = sorted(*[l[1] for l in _l1 if l[0] == _l3], key = lambda x: x["bads"] / x["freq"])
  _l5 = add_miss(_data, _l4)
  return({"cut": _l3, "tbl": gen_rule(gen_woe(_l5), _l3)})


########## 11. bad_bin() ##########

def bad_bin(x, y):
  """
  The function discretizes the x vector based on percentiles and then 
  summarizes over the y vector with y = 1 to derive the weight of evidence 
  transformaton (WoE) and information values.
  Parameters:
    x : A numeric vector to discretize. It is a list, 1-D numpy array, 
        or pandas series.
    y : A numeric vector with binary values of 0/1 and with the same length 
        of x. It is a list, 1-D numpy array, or pandas series.
  Returns:
    A dictionary with two keys:
      "cut" : A numeric vector with cut points applied to the x vector.
      "tbl" : A list of dictionaries summarizing the binning outcome.
  """

  _data = [_ for _ in zip(x, y, ~numpy.isnan(x))]
  _x = [_[0] for _ in _data if _[2] == 1]
  _y = [_[1] for _ in _data if _[2] == 1]
  _n = numpy.arange(2, max(3, min(50, len(set([_[0] for _ in _data if _[1] == 1 and _[2] == 1])) - 1)))
  _p = set(tuple(qcut([_[0] for _ in _data if _[1] == 1 and _[2] == 1], _)) for _ in _n)

  _l1 = [[_, manual_bin(_x, _y, _)] for _ in _p]

  _l2 = [[l[0], 
          min([_["bads"] / _["freq"] for _ in l[1]]), 
          max([_["bads"] / _["freq"] for _ in l[1]]),
          spearmanr([_["bin"] for _ in l[1]], [_["bads"] / _["freq"] for _ in l[1]])[0]
         ] for l in _l1]

  _l3 = [l[0] for l in sorted(_l2, key = lambda x: -len(x[0]))
         if numpy.abs(round(l[3], 8)) == 1 and round(l[1], 8) > 0 and round(l[2], 8) < 1][0]

  _l4 = sorted(*[l[1] for l in _l1 if l[0] == _l3], key = lambda x: x["bads"] / x["freq"])
  _l5 = add_miss(_data, _l4)
  return({"cut": _l3, "tbl": gen_rule(gen_woe(_l5), _l3)})


########## 12. iso_bin() ##########

def iso_bin(x, y):
  """
  The function discretizes the x vector based on the isotonic regression and 
  then summarizes over the y vector to derive the weight of evidence 
  transformaton (WoE) and information values.
  Parameters:
    x : A numeric vector to discretize. It is a list or numpy array;
    y : A numeric vector with binary values of 0/1 and with the same length 
        of x. It is a list or numpy array.
  Returns:
    A dictionary with two keys:
      "cut" : A numeric vector with cut points applied to the x vector.
      "tbl" : A list of dictionaries summarizing the binning outcome.
  """

  _data = [_ for _ in zip(x, y, ~numpy.isnan(x))]
  _x = [_[0] for _ in _data if _[2] == 1]
  _y = [_[1] for _ in _data if _[2] == 1]

  _c = True if spearmanr(_x, _y)[0] > 0 else False
  _f = isoreg(increasing = _c).fit_transform(_x, _y)

  _l1 = sorted(list(zip(_f, _x, _y)), key = lambda x: x[0])
  _l2 = [[l for l in _l1 if l[0] == f] for f in sorted(set(_f))]

  _l3 = [[*set(_[0] for _ in l),
          max(_[1] for _ in l),
          numpy.mean([_[2] for _ in l]),
          sum(_[2] for _ in l)] for l in _l2]

  _c = sorted([_[1] for _ in [l for l in _l3 if l[2] < 1 and l[2] > 0 and l[3] >= 10]])
  _p = _c[:-1] if len(_c) > 1 else _c[:]
    
  _l4 = sorted(manual_bin(_x, _y, _p), key = lambda x: x["bads"] / x["freq"])
  _l5 = add_miss(_data, _l4)
  return({"cut": _p, "tbl": gen_rule(gen_woe(_l5), _p)})


########## 13. rng_bin() ##########

def rng_bin(x, y):
  """
  The function discretizes the x vector based on the equal-width range and 
  summarizes over the y vector to derive the weight of evidence transformaton 
  (WoE) and information values.
  Parameters:
    x : A numeric vector to discretize. It is a list or numpy array; 
    y : A numeric vector with binary values of 0/1 and with the same length 
        of x. It is a list or numpy array.
  Returns:
    A dictionary with two keys:
      "cut" : A numeric vector with cut points applied to the x vector.
      "tbl" : A list of dictionaries summarizing the binning outcome.
  """

  _data = [_ for _ in zip(x, y, ~numpy.isnan(x))]
  _x = [_[0] for _ in _data if _[2] == 1]
  _y = [_[1] for _ in _data if _[2] == 1]

  _n = numpy.arange(2, max(3, min(50, len(set(_x)) - 1)))

  _m = [[numpy.median([_[0] for _ in _data if _[2] == 1 and _[1] == 1])],
        [numpy.median([_[0] for _ in _data if _[2] == 1])]]

  _p = list(set(tuple(qcut(set(_x), _)) for _ in _n)) + _m

  _l1 = [[_, manual_bin(_x, _y, _)] for _ in _p]

  _l2 = [[l[0], 
          min([_["bads"] / _["freq"] for _ in l[1]]), 
          max([_["bads"] / _["freq"] for _ in l[1]]),
          spearmanr([_["bin"] for _ in l[1]], [_["bads"] / _["freq"] for _ in l[1]])[0]
         ] for l in _l1]

  _l3 = [l[0] for l in sorted(_l2, key = lambda x: -len(x[0]))
         if numpy.abs(round(l[3], 8)) == 1 and round(l[1], 8) > 0 and round(l[2], 8) < 1][0]

  _l4 = sorted(*[l[1] for l in _l1 if l[0] == _l3], key = lambda x: x["bads"] / x["freq"])
  _l5 = add_miss(_data, _l4)
  return({"cut": _l3, "tbl": gen_rule(gen_woe(_l5), _l3)})


########## 14. kmn_bin() ##########

def kmn_bin(x, y):
  """
  The function discretizes the x vector based on the kmean clustering and then 
  summarizes over the y vector to derive the weight of evidence transformaton 
  (WoE) and information values.
  Parameters:
    x : A numeric vector to discretize. It is a list, 1-D numpy array,
        or pandas series.
    y : A numeric vector with binary values of 0/1 and with the same length 
        of x. It is a list, 1-D numpy array, or pandas series.
  Returns:
    A dictionary with two keys:
      "cut" : A numeric vector with cut points applied to the x vector.
      "tbl" : A list of dictionaries summarizing the binning outcome.
  """

  _data = [_ for _ in zip(x, y, ~numpy.isnan(x))]
  _x = [_[0] for _ in _data if _[2] == 1]
  _y = [_[1] for _ in _data if _[2] == 1]

  _n = numpy.arange(2, max(3, min(20, round(len(set(_x)) / 2, 0))))
  _m = [[numpy.median([_[0] for _ in _data if _[2] == 1 and _[1] == 1])],
        [numpy.median([_[0] for _ in _data if _[2] == 1])]]

  _c1 = [kmeans(n_clusters = int(_), random_state = 1, n_init = 'auto').fit(numpy.reshape(_x, [-1, 1])).labels_ for _ in _n]

  _c2 = [sorted(_l, key = lambda x: x[0]) for _l in [list(zip(_, _x)) for _ in _c1]]

  group = lambda x: [[_l for _l in x if _l[0] == _k] for _k in set([_[0] for _ in x])]

  upper = lambda x: sorted([max([_2[1] for _2 in _1]) for _1 in x])

  _c3 = list(set(tuple(upper(_2)[:-1]) for _2 in [group(_1) for _1 in _c2])) + _m

  _l1 = [[_, manual_bin(_x, _y, _)] for _ in _c3]

  _l2 = [[l[0], 
          min([_["bads"] / _["freq"] for _ in l[1]]), 
          max([_["bads"] / _["freq"] for _ in l[1]]),
          spearmanr([_["bin"] for _ in l[1]], [_["bads"] / _["freq"] for _ in l[1]])[0]
         ] for l in _l1]

  _l3 = [l[0] for l in sorted(_l2, key = lambda x: -len(x[0]))
         if numpy.abs(round(l[3], 8)) == 1 and round(l[1], 8) > 0 and round(l[2], 8) < 1][0]

  _l4 = sorted(*[l[1] for l in _l1 if l[0] == _l3], key = lambda x: x["bads"] / x["freq"])
  _l5 = add_miss(_data, _l4)
  return({"cut": _l3, "tbl": gen_rule(gen_woe(_l5), _l3)})


########## 15. gbm_bin() ########## 

def gbm_bin(x, y):
  """
  The function discretizes the x vector based on the gradient boosting machine 
  and then summarizes over the y vector to derive the weight of evidence 
  transformaton (WoE) and information values.
  Parameters:
    x : A numeric vector to discretize. It is a list or numpy array;
    y : A numeric vector with binary values of 0/1 and with the same length 
        of x. It is a list or numpy array.
  Returns:
    A dictionary with two keys:
      "cut" : A numeric vector with cut points applied to the x vector.
      "tbl" : A list of dictionaries summarizing the binning outcome.
  """

  _data = [_ for _ in zip(x, y, ~numpy.isnan(x))]
  _x = [_[0] for _ in _data if _[2] == 1]
  _y = [_[1] for _ in _data if _[2] == 1]

  _con = 1 if spearmanr(_x, _y)[0] > 0 else -1

  _m = gbmreg(min_samples_leaf = 10, monotonic_cst = [_con], random_state = 1,
              early_stopping = False, validation_fraction = None
             ).fit(numpy.reshape(_x, [-1, 1]), _y)
  _f = _m.predict(numpy.reshape(_x, [-1, 1]))

  _l1 = sorted(list(zip(_f, _x, _y)), key = lambda x: x[0])

  _l2 = [[l for l in _l1 if l[0] == f] for f in sorted(set(_f))]

  _l3 = [[*set(_[0] for _ in l),
          max(_[1] for _ in l),
          numpy.mean([_[2] for _ in l]),
          sum(_[2] for _ in l)] for l in _l2]

  _c = sorted([_[1] for _ in [l for l in _l3 if l[2] < 1 and l[2] > 0 and l[3] >= 10]])
  _p = _c[:-1] if len(_c) > 1 else _c[:]
    
  _l4 = sorted(manual_bin(_x, _y, _p), key = lambda x: x["bads"] / x["freq"])
  _l5 = add_miss(_data, _l4)
  return({"cut": _p, "tbl": gen_rule(gen_woe(_l5), _p)})


########## 16. pd_bin() ########## 

def pd_bin(y, xs, method = 1):
  """
  The function discretizes each vector in the pandas DataFrame, e.g. xs, based 
  on the chosen binning method. 
  Parameters:
    y     : A numeric vector with binary values of 0/1 and with the same length 
            of xs. It can be a list, 1-D numpy array, or pandas series.
    xs    : A pandas DataFrame including all numeric vectors to discretize.
    method: A integer from 1 to 6 referring to implementations below. 
            The default value is 1.
              1 - implementation of iso_bin()    2 - implementation of qtl_bin()
              3 - implementation of bad_bin()    4 - implementation of rng_bin()
              5 - implementation of gbm_bin()    6 - implementation of kmn_bin()
  Returns:
    A dictionary with two keys:
      'bin_sum': A list of binning summary
      'bin_out': A dictionary of binning outcomes for all variables in xs
  Example:
    df = pandas.DataFrame(py_mob.get_data("accepts"))
    rst = py_mob.pd_bin(df['bad'], df[['ltv', 'bureau_score', 'tot_derog']])
    rst.keys()
    # dict_keys(['bin_sum', 'bin_out'])
    for _ in rst['bin_sum']:
      print(_)
    {'variable': 'ltv', ... 'iv': 0.185, 'ks': 16.88, 'missing': 0.0002}
    {'variable': 'bureau_score', ... 'iv': 0.8354, 'ks': 35.27, 'missing': 0.054}
    {'variable': 'tot_derog', ... 'iv': 0.2151, 'ks': 18.95, 'missing': 0.0365}
  """

  methods = {1: iso_bin, 2: qtl_bin, 3: bad_bin, 4: rng_bin, 5: gbm_bin, 6: kmn_bin}

  bin_fn = methods[method]

  xnames = [_ for _ in xs.columns]

  bin_out = dict(zip(xnames, [bin_fn(xs[_], y) for _ in xnames]))

  bin_sum = [{'variable': _, **summ_bin(bin_out.get(_))} for _ in xnames]

  return({'bin_sum': bin_sum, 'bin_out': bin_out})


########## 17. pd_woe() ########## 

def pd_woe(xs, bin_out):
  """
  The function applies WoE transformaton to each vector in the pandas DataFrame
  based on the binning output from py_mob.pd_bin() function. 
  Parameters:
    xs      : A pandas DataFrame including all numeric vectors to do WoE 
              transformatons.
    bin_out : The dictionary of binning outcomes from py_mob.pd_bin(),
              e.g. pd_bin(y, xs)["bin_out"].
  Returns:
    A pandas DataFrame with identical headers as the input xs. However, values 
    of each variable have been transformed to WoE values.
  Example:
    df = pandas.DataFrame(py_mob.get_data("accepts"))
    rst = py_mob.pd_bin(df['bad'], df[['ltv', 'bureau_score', 'tot_derog']])
    out = py_mob.pd_woe(df[['ltv', 'bureau_score', 'tot_derog']], rst["bin_out"])
  """

  xnames = [_ for _ in bin_out.keys()]

  woe_out = dict([_, [w["woe"] for w in cal_woe(xs[_], bin_out.get(_))]] for _ in xnames)

  return(pandas.DataFrame(woe_out))

