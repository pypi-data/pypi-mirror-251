"""Tense tree implementation"""

from ulflib.util import atom, listp
from ulflib.sexpr import parse_s_expr
from ulflib.ulflib import lex_tense_p, lex_aspect_p, tensed_sent_reifier_p, adv_e_p, adv_f_p, lex_rel_p, ps_p

from ulflib.tense_tree.constants import *
from ulflib.tense_tree.preprocess import preprocess
from ulflib.tense_tree.tense_node import TenseNode

def get_mood(ulf):
  """Determine the mood of the ULF."""
  if atom(ulf):
    return MOOD_DECL
  elif ulf[-1] in ['?', '.?']:
    return MOOD_QUES
  elif ulf[-1] == '!':
    return MOOD_IMPER
  else:
    return MOOD_DECL
  

class TenseTree:
  """A tense tree.
  
  Attributes
  ----------
  root : TenseNode
    The root node of this tense tree.
  now_idx : int
    A counter for the current 'Now' episode, to be updated
    with each logical form that gets deindexed.
  ep_idx : int
    A counter for each episode variable created.
  utt_idx : int
    A counter for each utterance variable created.
  disable_speech_acts : bool
    Whether to globally set speech_act = False when deindexing.
  """

  def __init__(self, disable_speech_acts=False):
    self.reset()
    self.disable_speech_acts=disable_speech_acts


  def reset(self):
    self.now_idx = 0
    self.ep_idx = 0
    self.utt_idx = 0
    self.root = TenseNode()


  def now(self):
    """Return the current 'Now' symbol."""
    return NOW + str(self.now_idx)


  def new_now(self):
    """Create a new 'Now' symbol."""
    self.now_idx += 1
    return self.now()


  def new_ep_var(self):
    """Create a new episode variable."""
    self.ep_idx += 1
    return EP_VAR + str(self.ep_idx)
  

  def new_utt_var(self):
    """Create a new utterance variable."""
    self.utt_idx += 1
    return UTT_VAR + str(self.utt_idx)
  

  def get_emb_episode(self, emb_node):
    """Get the episode corresponding to an embedding node.
    
    This is either the last episode of the node, or the current 'Now' if the node
    is the root of the tense tree.
    """
    if emb_node is self.root:
      return self.now()
    else:
      return emb_node.last_episode()
    

  def deindex(self, ulf, speech_act=True, is_scoped=False):
    """The top-level function to de-index a (possibly unscoped) logical form.

    Parameters
    ----------
    ulf : s-expr
      An "S-expression" (possibly nested lists of strings) representing an
      unscoped logical form (ULF) formula.
    speech_act : bool, default=True
      Whether to treat the input formula as a speech act, i.e., adding top-level
      speech act episodes to the resulting formula.
    is_scoped : bool, default=False
      Whether the input formula has already been scoped.
    
    Notes
    -----
    TODO: I'm not currently sure what should be done in the case of combined tense/aspect operators,
    such as (pres perf), or even whether this is currently supported by the scoping method used in
    preprocessing ULFs.
    """
    def deindex_recur(ulf, emb_node, focus):
      assert isinstance(emb_node, TenseNode) and isinstance(focus, TenseNode)
      
      if atom(ulf):
        return ulf
      op = ulf[0]

      # 1. Tense or aspect operator
      if lex_tense_p(op) or lex_aspect_p(op):
        e = self.new_ep_var()
        e_emb = self.get_emb_episode(emb_node)

        if op == PAST:
          restrictor = [e, focus.bef(), e_emb]
          new_focus = focus.move_left()
        elif op == PRES:
          restrictor = [e, AT_ABOUT, e_emb]
          new_focus = focus
        elif op == FUTR:
          restrictor = [e, AFTER, focus.last_episode()]
          new_focus = focus.move_right()
        elif op == PERF:
          restrictor = [e, IMPINGES_ON, focus.last_episode()]
          new_focus = focus.move_down()
        # other tense/aspect operators such as 'prog' or 'cf' are not yet supported
        else:
          return [op, deindex_recur(ulf[1], emb_node, focus)]
        
        if new_focus.last_episode() and new_focus.last_episode() != e:
          restrictor = [restrictor, AND, [new_focus.last_episode(), ORIENTS, e]]

        nucleus = [deindex_recur(ulf[1], emb_node, new_focus.add_episode(e)), CH, e]
        return [EXISTS, e, restrictor, nucleus]
      
      # 2. Embedding operator
      elif tensed_sent_reifier_p(op):
        return [op, deindex_recur(ulf[1], focus, focus.move_embedded_new())]

      # 3. Temporal or frequency adverb
      elif (adv_e_p(op) or adv_f_p(op)) and listp(op):
        e = focus.last_episode()
        adv_pred = deindex_recur(op[1], emb_node, focus)
        nucleus = deindex_recur(ulf[1], emb_node, focus)
        if adv_e_p(op):
          return [[e, adv_pred], AND, nucleus]
        else:
          return [[e, adv_pred], AND, [MULT, nucleus]]

      # 4. Relativizers (e.g., that.rel)
      elif lex_rel_p(op):
        # TODO
        pass

      # 5. Sentential prepositions (e.g., before.ps)
      elif ps_p(op) and listp(op):
        e = focus.last_episode()
        ps_res = deindex_recur(op[1], emb_node, focus)
        prep = op[0][:-1]
        if ps_res[0] == EXISTS:
          _, e2, restrictor, nucleus = ps_res
          restrictor_new = restrictor + [AND, [e, prep, e2]]
          return [EXISTS, e2, restrictor_new, nucleus]

      return [deindex_recur(ulf_part, emb_node, focus) for ulf_part in ulf]

    # ===== MAIN BODY OF FUNCTION =====
    
    if isinstance(ulf, str):
      ulf = parse_s_expr(ulf)

    ulf = preprocess(ulf, is_scoped=is_scoped)
    focus = self.root

    if self.disable_speech_acts or not speech_act:
      return deindex_recur(ulf, focus, focus)

    mood = get_mood(ulf)
    u = self.new_utt_var()
    now = self.new_now()
    restrictor = [u, SAME_TIME, now]

    # The utterance episode is assumed to be just after the preceeding episode in focus
    if focus.last_episode():
      restrictor = [restrictor, AND, [u, JUST_AFTER, focus.last_episode()]]

    embedded = deindex_recur(ulf, focus, focus.add_episode(u).move_embedded_cur())

    # Form speech act logical form depending on mood of ULF
    if mood == MOOD_DECL:
      lf = [EXISTS, u, restrictor, [[SPEAKER, TELL, HEARER, [THAT, embedded]], CH, u]]
    elif mood == MOOD_QUES:
      lf = [EXISTS, u, restrictor, [[SPEAKER, ASK, HEARER, [ANS_TO, embedded]], CH, u]]
    elif mood == MOOD_IMPER:
      lf = [EXISTS, u, restrictor, [[SPEAKER, INSTRUCT, HEARER, [KA, embedded]], CH, u]]

    return lf