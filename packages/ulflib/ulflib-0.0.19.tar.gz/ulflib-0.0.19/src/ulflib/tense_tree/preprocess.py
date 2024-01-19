"""Functions for preprocessing ULFs."""

from functools import reduce

from transduction import tt
from memoization import cached

from ulflib.util import atom, append, cons, flatten_singletons, listp, apply_all, new_var, variables_in
from ulflib.ulflib import (direct_sent_mod_stop_p, arg_sent_mod_stop_p, sent_mod_stop_p, sent_mod_p, ps_p, make_all_explicit, lower_all,
                            split_by_suffix, apply_substitution_macros,
                            lex_adv_e_p, adv_e_p, lex_adv_f_p, adv_f_p, lex_number_p, pp_p, lex_pronoun_p, lex_det_p, adj_p, lex_adjective_p,
                            lex_mod_n_p, mod_a_p)
from ulflib import scoping
from ulflib.tense_tree.temporal_lex import *

# ``````````````````````````````````````
# TT Temporal Adverb LF Patterns
# ``````````````````````````````````````


@cached
def number_p(x):
  return lex_number_p(x) or x in NUMBERS

@cached
def to_number(x):
  return int(x) if lex_number_p(x) else NUMBERS[x]

@cached
def adv_e_pp(x):
  return adv_e_p(x) and listp(x) and len(x) == 2 and pp_p(x[1])

@cached
def adv_e_adj(x):
  return adv_e_p(x) and listp(x) and len(x) == 2 and adj_p(x[1])

@cached
def adv_f_pp(x):
  return adv_f_p(x) and listp(x) and len(x) == 2 and pp_p(x[1])

@cached
def adv_f_adj(x):
  return adv_f_p(x) and listp(x) and len(x) == 2 and adj_p(x[1])


@cached
def ever_adv(x, oldvars):
  if x == 'ever.adv-e':
    return ['adv-e', 'episode.n'], []
  else:
    return None, []


@cached
def indexical_adv(x, oldvars):
  """Yesterday, now, etc."""
  ret = None
  newvars = []
  if x == 'currently.adv-e' or x == ['adv-e', 'current.a']:
    ret = ['adv-e', ['during.p', '^now']]
  elif lex_adv_e_p(x):
    word, _ = split_by_suffix(x)
    if word in INDEXICAL_TIMES:
      ret = ['adv-e', ['during.p', '^'+word]]
  return ret, newvars


@cached
def temp_location_adv(x, oldvars):
  """On Friday, during last weekend, etc."""
  ret = None
  newvars = []
  if lex_adv_e_p(x):
    word, _ = split_by_suffix(x)
    if word in LOCATION_ADV_MAP:
      adj = LOCATION_ADV_MAP[word]
      var = new_var(oldvars, base='?t')
      ret = ['adv-e', ['during.p', ['the', var, [var, [adj, 'episode.n']]]]]
      newvars = [var]
  elif adv_e_adj(x):
    if lex_adjective_p(x[1]):
      lex_adj, _ = split_by_suffix(x[1])
      if lex_adj in LOCATION_ADJ_MAP:
        adj = LOCATION_ADJ_MAP[lex_adj]
        ret = ['adv-e', ['during.p', ['the', var, [var, [adj, 'episode.n']]]]]
        newvars = [var]
  elif adv_e_pp(x):
    pp = x[1]
    lex_prep, _ = split_by_suffix(pp[0])
    termp = pp[1]
    if lex_prep in LOCATION_PRED_MAP:
      pred = LOCATION_PRED_MAP[lex_prep]
      # Indexical term, e.g. During Friday
      if atom(termp):
        lex_term, _ = split_by_suffix(termp)
        if termp in INDEXICAL_TIMES or (lex_pronoun_p(termp) and lex_term in INDEXICAL_TIMES):
          ret = ['adv-e', [pred, '^'+lex_term]]
      # Noun phrase, e.g. During {the} last weekend
      else:
        det, np = termp
        if det in QUAN_MAP:
          quan = QUAN_MAP[det]
          var = new_var(oldvars, base='?t')
          ret = ['adv-e', [pred, [quan, var, [var, np]]]]
          newvars = [var]
  return ret, newvars


@cached
def temp_range_adv(x, oldvars):
  """Recently, before, next, etc."""
  ret = None
  newvars = []
  if lex_adv_e_p(x):
    word, _ = split_by_suffix(x)
    if word in RANGE_ADV_MAP:
      adj = RANGE_ADV_MAP[word]
      var = new_var(oldvars, base='?t')
      ret = ['adv-e', ['during.p', ['some', var, [var, [adj, 'episode.n']]]]]
      newvars = [var]
  elif adv_e_adj(x):
    if lex_adjective_p(x[1]):
      lex_adj, _ = split_by_suffix(x[1])
      if lex_adj in RANGE_ADJ_MAP:
        adj = RANGE_ADJ_MAP[lex_adj]
        var = new_var(oldvars, base='?t')
        ret = ['adv-e', ['during.p', ['some', var, [var, [adj, 'episode.n']]]]]
        newvars = [var]
    elif listp(x[1]) and mod_a_p(x[1][0]) and x[1][1] == 'ago.a':
      adj = x[1]
      var = new_var(oldvars, base='?t')
      ret = ['adv-e', ['during.p', ['some', var, [var, [adj, 'episode.n']]]]]
      newvars = [var]
  return ret, newvars


@cached
def duration_adv(x, oldvars):
  """For two hours, for three days, in three days, etc."""
  ret = None
  newvars = []
  if adv_e_pp(x):
    pp = x[1]
    lex_prep, _ = split_by_suffix(pp[0])
    termp = pp[1]
    if lex_prep in DURATION_PRED_MAP and listp(termp):
      pred = DURATION_PRED_MAP[lex_prep]
      det, np = termp
      if lex_det_p(det):
        lex_det, _ = split_by_suffix(det)
        if number_p(lex_det):
          ret = ['adv-e', [pred, ['k', [str(to_number(lex_det))+'.mod-n', np]]]]
  return ret, newvars


@cached
def count_adv(x, oldvars):
  """Twice, {for} three times, etc."""
  ret = None
  newvars = []
  if lex_adv_f_p(x):
    word, _ = split_by_suffix(x)
    if number_p(word):
      ret = ['adv-f', [str(to_number(word))+'.mod-n', ['plur', 'episode.n']]]
  elif adv_f_adj(x):
    if lex_adjective_p(x[1]):
      lex_adj, _ = split_by_suffix(x[1])
      if number_p(lex_adj):
        ret = ['adv-f', [str(to_number(lex_adj))+'.mod-n', ['plur', 'episode.n']]]
  elif adv_f_pp(x):
    pp = x[1]
    lex_prep, _ = split_by_suffix(pp[0])
    termp = pp[1]
    if lex_prep in ADV_F_P and listp(termp):
      det, np = termp
      if lex_det_p(det):
        lex_det, _ = split_by_suffix(det)
        if number_p(lex_det):
          ret = ['adv-f', [str(to_number(lex_det))+'.mod-n', np]]
  return ret, newvars


@cached
def frequency_adv(x, oldvars):
  """Frequently, {for} many times, rarely, usually, etc."""
  ret = None
  newvars = []
  if lex_adv_f_p(x):
    word, _ = split_by_suffix(x)
    if word in FREQUENCY_ADV_MAP:
      adj = FREQUENCY_ADV_MAP[word]
      var = new_var(oldvars, base='?t')
      ret = ['adv-f', [['attr', adj], ['plur', 'episode.n']]]
  elif adv_f_adj(x):
    if lex_adjective_p(x[1]):
      lex_adj, _ = split_by_suffix(x[1])
      if lex_adj in FREQUENCY_ADJ_MAP:
        adj = FREQUENCY_ADJ_MAP[lex_adj]
        ret = ['adv-f', [['attr', adj], ['plur', 'episode.n']]]
  elif adv_f_pp(x):
    pp = x[1]
    lex_prep, _ = split_by_suffix(pp[0])
    termp = pp[1]
    if lex_prep in ADV_F_P and listp(termp):
      det, np = termp
      if lex_det_p(det):
        lex_det, _ = split_by_suffix(det)
        if lex_det in FREQUENCY_DET_MAP:
          adj = FREQUENCY_DET_MAP[lex_det]
          ret = ['adv-f', [['attr', adj], ['plur', 'episode.n']]]
  return ret, newvars


@cached
def periodicity_adv(x, oldvars):
  """{For} every four hours, etc."""
  ret = None
  newvars = []
  if adv_f_pp(x):
    pp = x[1]
    lex_prep, _ = split_by_suffix(pp[0])
    termp = pp[1]
    if lex_prep in ADV_F_P and listp(termp):
      det, np = termp
      if lex_det_p(det):
        lex_det, _ = split_by_suffix(det)
        if lex_det in ['every', 'each']:
          var = new_var(oldvars, base='?s')
          if listp(np) and len(np) == 2 and (lex_adjective_p(np[0]) or lex_mod_n_p(np[0])) and number_p(split_by_suffix(np[0])[0]):
            mod = str(to_number(split_by_suffix(np[0])[0])) + '.mod-n'
            ret = ['adv-f', [':l', var, [[var, [['attr', 'periodic.a'], ['plur', 'episode.n']]], 'and.cc',
                                         [['period-of.f', '?s'], '=', ['k', [mod, np[1]]]]]]]
            newvars = [var]
  return ret, newvars


@cached
def recurrence_adv(x, oldvars):
  """{For} every Saturday, always, etc."""
  ret = None
  newvars = []
  if lex_adv_f_p(x):
    word, _ = split_by_suffix(x)
    if word in RECURRENCE_ADV_MAP:
      np = RECURRENCE_ADV_MAP[word]
      var_s = new_var(oldvars, base='?s')
      var_t = new_var(oldvars+[var_s], base='?t')
      var_e = new_var(oldvars+[var_s, var_t], base='?e')
      ret = ['adv-f', [':l', var_s, ['all', var_t, [var_t, np],
                                      ['exists', var_e, [[var_e, 'member-of.p', var_s], 'and.cc',
                                                        [var_e, 'during.p', var_t]]]]]]
  elif adv_f_adj(x):
    if lex_adjective_p(x[1]):
      lex_adj, _ = split_by_suffix(x[1])
      if lex_adj in RECURRENCE_ADJ_MAP:
        np = RECURRENCE_ADJ_MAP[lex_adj]
        var_s = new_var(oldvars, base='?s')
        var_t = new_var(oldvars+[var_s], base='?t')
        var_e = new_var(oldvars+[var_s, var_t], base='?e')
        ret = ['adv-f', [':l', var_s, ['all', var_t, [var_t, np],
                                        ['exists', var_e, [[var_e, 'member-of.p', var_s], 'and.cc',
                                                          [var_e, 'during.p', var_t]]]]]]
  elif adv_f_pp(x):
    pp = x[1]
    lex_prep, _ = split_by_suffix(pp[0])
    termp = pp[1]
    if lex_prep in ADV_F_P and listp(termp):
      det, np = termp
      if lex_det_p(det):
        lex_det, _ = split_by_suffix(det)
        if lex_det in ['every', 'each']:
          var_s = new_var(oldvars, base='?s')
          var_t = new_var(oldvars+[var_s], base='?t')
          var_e = new_var(oldvars+[var_s, var_t], base='?e')
          ret = ['adv-f', [':l', var_s, ['all', var_t, [var_t, np],
                                         ['exists', var_e, [[var_e, 'member-of.p', var_s], 'and.cc',
                                                            [var_e, 'during.p', var_t]]]]]]
          newvars = [var_s, var_t, var_e]
  return ret, newvars


ADV_E_MAPS = [ever_adv, indexical_adv, temp_location_adv, temp_range_adv, duration_adv]
ADV_F_MAPS = [count_adv, frequency_adv, periodicity_adv, recurrence_adv]


TEMPORAL_ADV_PREDS = [

]

for pred in TEMPORAL_ADV_PREDS:
  tt.register_pred(pred, include_neg=True)



# ``````````````````````````````````````
# Main Preprocessing Functions
# ``````````````````````````````````````



def uninvert_aux(ulf):
  """Uninvert any auxiliary verb + NP construction.
  
  E.g., ``((pres verb.aux-s) |A| ...)`` -> ``(|A| ((pres verb.aux-s) ...))``
  """
  return tt.apply_rules([(
    ['!tensed-aux-p', '!term-p', '+expr'],
    ['2', ['1', '3']])],
  ulf)


def lift_sent_mods(ulf):
  """Lift any sentential modifiers to the appropriate non-floating level, preventing lifting through particular lift-stopping operators."""
  def add_mods(expr, mods):
    mods = handle_sentential_mods(mods)
    return reduce(lambda x,y: [y,x], mods[::-1], expr)
  
  def split_mods(form):
    nomod = [x for x in form if not sent_mod_p(x)]
    mods = [x for x in form if sent_mod_p(x)]
    return nomod, mods
  
  def handle_sentential_mods(mods):
    return [[m[0], lift_sent_mods(m[1])] if ps_p(m) else m for m in mods]
  
  def rec(form):
    # Base case
    if atom(form):
      return form, []
    # Simple recursive case (no lift-stopping and no sent mods)
    # Recurse and return the removed ULFs together and append modifier lists
    elif not sent_mod_stop_p(form[0]) and not any([sent_mod_p(x) for x in form]):
      recres = [rec(x) for x in form]
      newulf = [r[0] for r in recres]
      allmods = append([r[1] for r in recres])
      return newulf, allmods
    # Simple-ish recursive case (no lift-stopping but has modifiers)
    # Recurse and remove current modifiers
    elif not sent_mod_stop_p(form[0]):
      nomod, mods = split_mods(form)
      reculf, recmods = rec(nomod)
      return reculf, mods+recmods
    # Direct lift-stopping
    elif direct_sent_mod_stop_p(form[0]):
      nomod, mods = split_mods(form)
      recres = [rec(x) for x in nomod]
      newulf = [r[0] for r in recres]
      allmods = mods + append([r[1] for r in recres])
      if len(newulf) != 2:
        raise Exception('All direct not stopping operators must have a single argument: ' + str(newulf))
      return [newulf[0], add_mods(newulf[1], allmods)], []
    # Argument lift-stopping
    # NB: sentential mods not in the arguments are lifted
    else:
      nomod, mods = split_mods(form)
      recres = [rec(x) for x in nomod]
      modadded_args = [add_mods(argres[0], argres[1]) for argres in recres[1:]]
      return cons(form[0], modadded_args), mods
  
  # Main function body
  # Recurse and add in any stray modifiers
  newulf, mods = rec(ulf)
  return flatten_singletons(add_mods(newulf, mods))


def expand_temporal_mods(ulf):
  """Expand any temporal modifiers to the full logical form.
  
  E.g., ``twice.adv-f`` -> ``(adv-f (for.p (k (two.a (plur episode.n)))))``
  """
  def rec(x, vars):
    if adv_e_p(x):
      new, newvars = apply_all((x, vars), ADV_E_MAPS, return_size=2)
      newvars = [] if newvars is None else newvars
      return (x,vars) if new is None else (new,vars+newvars)
    elif adv_f_p(x):
      new, newvars = apply_all((x, vars), ADV_F_MAPS, return_size=2)
      newvars = [] if newvars is None else newvars
      return (x,vars) if new is None else (new,vars+newvars)
    elif atom(x):
      return (x,vars)
    else:
      ret = []
      for y in x:
        part, partvars = rec(y, vars)
        ret.append(part)
        vars += partvars
      return (ret,vars)
  ret, _ = rec(ulf, variables_in(ulf))
  return ret


def preprocess(ulf, is_scoped=False):
  """Preprocess a ulf, including scoping tense operators (if necessary) and lifting/expanding temporal modifiers."""
  ulf = make_all_explicit(lower_all(ulf))
  ulf = apply_substitution_macros(ulf)
  ulf = uninvert_aux(ulf)
  if not is_scoped:
    ulf = scoping.scope(ulf, types=['tense'])
  return expand_temporal_mods(lift_sent_mods(ulf))