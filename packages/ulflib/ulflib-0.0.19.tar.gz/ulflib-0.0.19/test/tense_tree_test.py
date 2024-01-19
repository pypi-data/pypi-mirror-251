import sys
sys.path.append("src/")

import pytest

from ulflib.util import variablep
from ulflib.tense_tree.preprocess import *
from ulflib.tense_tree import TenseTree

def equal_with_variables(ulf1, ulf2):
  var_map = {}
  def rec(x1, x2):
    if atom(x1) and atom(x2):
      if variablep(x1) and variablep(x2):
        if x1 not in var_map:
          var_map[x1] = x2
          return True
        else:
          return var_map[x1] == x2
      else:
        return x1 == x2
    elif atom(x1) or atom(x2):
      return False
    elif len(x1) != len(x2):
      return False
    else:
      return all([rec(y1, y2) for y1, y2 in zip(x1, x2)])
  return rec(ulf1, ulf2)



class TestPreprocessingUninvertAux:
  def test_1(self):
    ulf = [[['pres', 'do.aux-s'], 'john', ['go.v', ['to', ['the.d', 'store.n']]]], '?']
    ulf1 = [['john', [['pres', 'do.aux-s'], ['go.v', ['to', ['the.d', 'store.n']]]]], '?']
    assert equal_with_variables(uninvert_aux(ulf), ulf1)



class TestPreprocessingLiftSentMods:
  def test_1(self):
    ulf = ['past', ['mary', ['leave.v', 'yesterday.adv-e']]]
    ulf1 = ['past', ['yesterday.adv-e', ['mary', 'leave.v']]]
    assert equal_with_variables(lift_sent_mods(ulf), ulf1)


  def test_2(self):
    ulf = ['past', ['mary', ['leave.v', 'yesterday.adv-e', ['adv-e', ['before.p', ['k', 'noon.n']]]]]]
    ulf1 = ['past', ['yesterday.adv-e', [['adv-e', ['before.p', ['k', 'noon.n']]], ['mary', 'leave.v']]]]
    assert equal_with_variables(lift_sent_mods(ulf), ulf1)


  def test_3(self):
    ulf = ['past', ['john', ['go.v', ['to.p', ['the.d', 'bathroom.n']], 'frequently.adv-f', 'yesterday.adv-e']]]
    ulf1 = ['past', ['frequently.adv-f', ['yesterday.adv-e', ['john', ['go.v', ['to.p', ['the.d', 'bathroom.n']]]]]]]
    assert equal_with_variables(lift_sent_mods(ulf), ulf1)


  def test_4(self):
    ulf = ['past', [['the.d', ['red.a', 'block.n']], [['pasv', 'move.v'], ['adv-e', ['most.mod-a', ['adv-e', 'recent.a']]]]]]
    ulf1 = ['past', [['adv-e', ['most.mod-a', ['adv-e', 'recent.a']]], [['the.d', ['red.a', 'block.n']], ['pasv', 'move.v']]]]
    assert equal_with_variables(lift_sent_mods(ulf), ulf1)


  def test_5(self):
    ulf = ['past', ['john', 'just.adv-e', ['move.v', ['the.d', ['green.a', 'block.n']],
                                           ['before.ps', ['past', [['the.d', ['red.a', 'block.n']], [['pasv', 'move.v'],
                                                                      ['adv-e', ['most.mod-a', ['adv-e', 'recent.a']]]]]]]]]]
    ulf1 = ['past', ['just.adv-e', [['before.ps', ['past', [['adv-e', ['most.mod-a', ['adv-e', 'recent.a']]],
                                                            [['the.d', ['red.a', 'block.n']], ['pasv', 'move.v']]]]],
                                    ['john', ['move.v', ['the.d', ['green.a', 'block.n']]]]]]]
    assert equal_with_variables(lift_sent_mods(ulf), ulf1)



class TestPreprocessingExpandTemporalMods:
  def test_ever(self):
    ulf = ['past', ['ever.adv-e', ['john', ['go.v', ['to.p', ['the.d', 'store.n']]]]]]
    ulf1 = ['past', [['adv-e', 'episode.n'], ['john', ['go.v', ['to.p', ['the.d', 'store.n']]]]]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)


  def test_indexical(self):
    ulf = ['past', ['yesterday.adv-e', ['mary', 'leave.v']]]
    ulf1 = ['past', [['adv-e', ['during.p', '^yesterday']], ['mary', 'leave.v']]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)

    ulf = ['past', ['now.adv-e', ['mary', 'leave.v']]]
    ulf1 = ['past', [['adv-e', ['during.p', '^now']], ['mary', 'leave.v']]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)

    ulf = ['past', ['currently.adv-e', ['mary', 'leave.v']]]
    ulf1 = ['past', [['adv-e', ['during.p', '^now']], ['mary', 'leave.v']]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)


  def test_temporal_location(self):
    ulf = ['past', [['adv-e', ['on.p', ['k', ['last.a', 'saturday.n']]]], ['mary', 'leave.v']]]
    ulf1 = ['past', [['adv-e', ['during.p', ['the', '?t', ['?t', ['last.a', 'saturday.n']]]]], ['mary', 'leave.v']]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)

    ulf = ['past', ['just.adv-e', ['mary', 'leave.v']]]
    ulf1 = ['past', [['adv-e', ['during.p', ['the', '?t', ['?t', ['previous.a', 'episode.n']]]]], ['mary', 'leave.v']]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)

    ulf = ['past', ['initially.adv-e', ['mary', 'leave.v']]]
    ulf1 = ['past', [['adv-e', ['during.p', ['the', '?t', ['?t', ['initial.a', 'episode.n']]]]], ['mary', 'leave.v']]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)

    ulf = ['past', [['adv-e', ['before.p', ['this.d', 'wednesday.n']]],
                    [['adv-e', ['after.p', ['the.d', ['last.a', 'weekend.n']]]], ['mary', 'leave.v']]]]
    ulf1 = ['past', [['adv-e', ['before.p', ['this', '?t1', ['?t1', 'wednesday.n']]]],
                     [['adv-e', ['after.p', ['the', '?t2', ['?t2', ['last.a', 'weekend.n']]]]], ['mary', 'leave.v']]]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)

  
  def test_temporal_range(self):
    ulf = ['past', ['recently.adv-e', ['mary', 'leave.v']]]
    ulf1 = ['past', [['adv-e', ['during.p', ['some', '?t', ['?t', ['recent.a', 'episode.n']]]]], ['mary', 'leave.v']]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)

    ulf = ['past', ['before.adv-e', ['mary', 'leave.v']]]
    ulf1 = ['past', [['adv-e', ['during.p', ['some', '?t', ['?t', ['previous.a', 'episode.n']]]]], ['mary', 'leave.v']]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)

    ulf = ['past', [['adv-e', [['mod-a', ['by.p', ['1.d', 'move.n']]], 'ago.a']],
                    [['which.d', ['plur', 'block.n']], ['be.v', ['near.p', ['the.d', ['mercedes', 'block.n']]]]]]]
    ulf1 = ['past', [['adv-e', ['during.p', ['some', '?t', ['?t', [[['mod-a', ['by.p', ['1.d', 'move.n']]], 'ago.a'], 'episode.n']]]]],
                    [['which.d', ['plur', 'block.n']], ['be.v', ['near.p', ['the.d', ['mercedes', 'block.n']]]]]]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)


  def test_duration(self):
    ulf = ['past', [['adv-e', ['for.p', ['two.d', ['plur', 'hour.n']]]], ['john', 'sleep.v']]]
    ulf1 = ['past', [['adv-e', ['has-duration.p', ['k', ['2.mod-n', ['plur', 'hour.n']]]]], ['john', 'sleep.v']]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)

    ulf = ['past', [['adv-e', ['in.p', ['two.d', ['plur', 'hour.n']]]], ['john', ['run.v', ['the.d', 'race.n']]]]]
    ulf1 = ['past', [['adv-e', ['in-span-of.p', ['k', ['2.mod-n', ['plur', 'hour.n']]]]], ['john', ['run.v', ['the.d', 'race.n']]]]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)


  def test_count(self):
    ulf = ['past', ['twice.adv-f', ['john', ['see.v', ['the.d', 'movie.n']]]]]
    ulf1 = ['past', [['adv-f', ['2.mod-n', ['plur', 'episode.n']]], ['john', ['see.v', ['the.d', 'movie.n']]]]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)

    ulf = ['past', [['adv-f', ['for.p', ['three.d', ['plur', 'time.n']]]], ['mary', ['visit.v', 'paris']]]]
    ulf1 = ['past', [['adv-f', ['3.mod-n', ['plur', 'time.n']]], ['mary', ['visit.v', 'paris']]]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)

    ulf = ['past', [['adv-f', 'twice.a'], ['mary', ['visit.v', 'paris']]]]
    ulf1 = ['past', [['adv-f', ['2.mod-n', ['plur', 'episode.n']]], ['mary', ['visit.v', 'paris']]]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)


  def test_frequency(self):
    ulf = ['past', ['frequently.adv-f', ['john', ['call.v', 'mary']]]]
    ulf1 = ['past', [['adv-f', [['attr', 'frequent.a'], ['plur', 'episode.n']]], ['john', ['call.v', 'mary']]]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)

    ulf = ['past', ['rarely.adv-f', ['john', ['call.v', 'mary']]]]
    ulf1 = ['past', [['adv-f', [['attr', 'infrequent.a'], ['plur', 'episode.n']]], ['john', ['call.v', 'mary']]]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)


  def test_periodicity(self):
    ulf = ['past', [['adv-f', ['for.p', ['every.d', ['four.a', ['plur', 'hour.n']]]]], ['john', ['take.v', ['k', 'medicine.n']]]]]
    ulf1 = ['past', [['adv-f', [':l', '?s', [['?s', [['attr', 'periodic.a'], ['plur', 'episode.n']]], 'and.cc',
                                             [['period-of.f', '?s'], '=', ['k', ['4.mod-n', ['plur', 'hour.n']]]]]]],
                                             ['john', ['take.v', ['k', 'medicine.n']]]]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)


  def test_recurrence(self):
    ulf = ['pres', [['adv-f', ['for.p', ['every.d', 'saturday.n']]], ['mary', 'swim.v']]]
    ulf1 = ['pres', [['adv-f', [':l', '?s', ['all', '?t', ['?t', 'saturday.n'],
                                             ['exists', '?e', [['?e', 'member-of.p', '?s'], 'and.cc',
                                                               ['?e', 'during.p', '?t']]]]]], ['mary', 'swim.v']]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)


  # def test_temporal_relation(self):
  #   # TODO: unsure if this needs to be preprocessed
  #   ulf = ['past', [['since.ps', ['past', ['john', 'go_off.v', ['to.p', ['k', 'college.n']]]]], ['mary', 'take_care_of.v', ['the.d', 'dog.n']]]]
  #   ulf1 = ['past', [['adv-e', [':l', '?e', ['the-earliest', '?t',
  #                                            ['past', [['adv-e', ['at-time.p', '?t']], ['john', 'go_off.v', ['to.p', ['k', 'college.n']]]]],
  #                                            ['?e', 'after.p', '?t']]]],
  #                       ['mary', 'take_care_of.v', ['the.d', 'dog.n']]]]
  #   assert equal_with_variables(expand_temporal_mods(ulf), ulf1)


  def test_combinations(self):
    ulf = ['past', [['adv-e', ['in.p', ['two.d', ['plur', 'month.n']]]],
                    [['adv-f', ['for.p', ['three.d', ['plur', 'time.n']]]], ['mary', ['visit.v', 'paris']]]]]
    ulf1 = ['past', [['adv-e', ['in-span-of.p', ['k', ['2.mod-n', ['plur', 'month.n']]]]],
                    [['adv-f', ['3.mod-n', ['plur', 'time.n']]], ['mary', ['visit.v', 'paris']]]]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)

    ulf = ['past', [['adv-e', ['for.p', ['ten.d', ['plur', 'day.n']]]],
                    [['adv-f', ['for.p', ['every.d', ['four.a', ['plur', 'hour.n']]]]], ['john', ['take.v', ['k', 'medicine.n']]]]]]
    ulf1 = ['past', [['adv-e', ['has-duration.p', ['k', ['10.mod-n', ['plur', 'day.n']]]]],
                    [['adv-f', [':l', '?s', [['?s', [['attr', 'periodic.a'], ['plur', 'episode.n']]], 'and.cc',
                                             [['period-of.f', '?s'], '=', ['k', ['4.mod-n', ['plur', 'hour.n']]]]]]],
                        ['john', ['take.v', ['k', 'medicine.n']]]]]]
    assert equal_with_variables(expand_temporal_mods(ulf), ulf1)



tree = TenseTree(disable_speech_acts=True)
# ulf = ['mary', [['past', 'leave.v'], ['adv-e', ['before.p', ['this.d', 'wednesday.n']]]]]
ulf = ['past', ['frequently.adv-f', ['john', ['call.v', 'mary']]]]
print(tree.deindex(ulf))
# print(preprocess(ulf))
# print(scoping.scope(ulf))

