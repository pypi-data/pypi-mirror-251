"""Word lists and word->predicate mappings used in adverbial expansion."""

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
TIMES_OF_DAY = ['dawn', 'sunrise', 'morning', 'noon', 'afternoon', 'evening', 'sundown', 'sunset', 'dusk', 'night', 'midnight']
INDEXICAL_TIMES = ['yesterday', 'tomorrow', 'now', 'current'] + TIMES_OF_DAY + DAYS
ABSOLUTE_TIMES = ['second', 'minute', 'hour', 'day', 'month', 'year', 'decade', 'century']
NOUNS = DAYS + TIMES_OF_DAY + ABSOLUTE_TIMES + ['weekend', 'weekday']

NUMBERS = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9, 'ten':10,
           'eleven':11, 'twelve':12, 'thirteen':13, 'fourteen':14, 'fifteen':15, 'sixteen':16, 'seventeen':17,
           'eighteen':18, 'nineteen':19, 'twenty':20, 'thirty':30, 'forty':40, 'fifty':50, 'sixty':60, 'seventy':70,
           'eighty':80, 'ninety':90, 'one_hundred':100, 'hundred':100, 'thousand':1000,
           'once':1, 'twice':2, 'thrice':3,
           'one-time':1, 'two-time':2, 'three-time':3, 'four-time':4, 'five-time':5}

LOCATION_PRED_MAP = {
  'during': 'during.p', 'at': 'during.p', 'in': 'during.p', 'within': 'during.p', 'on': 'during.p',
  'before': 'before.p', 'prior_to': 'before.p', 'preceding': 'before.p', 'until': 'before.p',
  'after': 'after.p', 'following': 'after.p', 'since': 'after.p', 'from': 'after.p'
}

LOCATION_ADV_MAP = {
  'originally': 'initial.a', 'initially': 'initial.a',
  'last': 'last.a', 'finally': 'last.a',
  'just': 'previous.a',
  'first': 'first.a', 'second': 'second.a', 'third': 'third.a', 'fourth': 'fourth.a', 'fifth': 'fifth.a',
  'sixth': 'sixth.a', 'seventh': 'seventh.a', 'eight': 'eight.a', 'nineth': 'nineth.a', 'tenth': 'tenth.a'
}

LOCATION_ADJ_MAP = {
  'original': 'initial.a', 'initial': 'initial.a',
  'last': 'last.a', 'final': 'last.a',
  'just': 'previous.a',
  'first': 'first.a', 'second': 'second.a', 'third': 'third.a', 'fourth': 'fourth.a', 'fifth': 'fifth.a',
  'sixth': 'sixth.a', 'seventh': 'seventh.a', 'eight': 'eight.a', 'nineth': 'nineth.a', 'tenth': 'tenth.a'
}

RANGE_ADV_MAP = {
  'recently': 'recent.a',
  'previously': 'previous.a', 'before': 'previous.a',
  'next': 'next.a', 'later': 'next.a',
}

RANGE_ADJ_MAP = {
  'recent': 'recent.a',
  'previous': 'previous.a', 'before': 'previous.a', 'preceding': 'previous.a',
  'next': 'next.a', 'later': 'next.a', 'following': 'next.a', 'future': 'next.a',
}

DURATION_PRED_MAP = {
  'for': 'has-duration.p', 'during': 'has-duration.p',
  'in': 'in-span-of.p'
}

FREQUENCY_ADV_MAP = {
  'frequently': 'frequent.a', 'commonly': 'frequent.a', 'regularly': 'frequent.a', 'often': 'frequent.a', 'routinely': 'frequent.a',
  'infrequently': 'infrequent.a', 'rarely': 'infrequent.a', 'uncommonly': 'infrequent.a', 'irregularly.a': 'infrequent.a', 'seldom': 'infrequent.a',
  'occasionally': 'infrequent.a', 'sometimes': 'infrequent.a'
}

FREQUENCY_ADJ_MAP = {
  'frequent': 'frequent.a', 'common': 'frequent.a', 'regular': 'frequent.a', 'often': 'frequent.a', 'routine': 'frequent.a',
  'infrequent': 'infrequent.a', 'rare': 'infrequent.a', 'uncommon': 'infrequent.a', 'irregular.a': 'infrequent.a', 'seldom': 'infrequent.a',
  'occasional': 'infrequent.a', 'sometimes': 'infrequent.a'
}

FREQUENCY_DET_MAP = {
  'many': 'frequent.a', 'most': 'frequent.a',
  'some': 'infrequent.a', 'few': 'infrequent.a'
}

RECURRENCE_ADV_MAP = {
  'always': 'episode.n', 'constantly': 'episode.n'
}

RECURRENCE_ADJ_MAP = {
  'always': 'episode.n', 'constant': 'episode.n'
}

ADV_F_P = ['for', 'during', 'on', 'at']


QUAN_MAP = {
  'k': 'the',
  'the.d': 'the',
  'this.d': 'this'
}