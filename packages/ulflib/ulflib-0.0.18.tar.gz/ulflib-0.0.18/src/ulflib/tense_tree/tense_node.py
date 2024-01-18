"""Tense node implementation"""

from ulflib.tense_tree.constants import *

class TenseNode:
  """A node in a tense tree.
  
  Attributes
  ----------
  left : TenseNode
    The 'past' branch of this node.
  down : TenseNode
    The 'perfect' branch of this node.
  right : TenseNode
    The 'future' branch of this node.
  embedded : list[TenseNode]
    A list of embedded nodes.
  parent : TenseNode
    The parent of this node.
  embedding : TenseNode
    The node embedding this node.
  episodes : list[str]
    The stack of episode symbols corresponding to this node.
  past_dominated : bool
    Whether this node is part of a past-dominated branch.
  """

  def __init__(self, left=None, down=None, right=None, embedded=[], parent=None, embedding=None, episodes=[], past_dominated=False):
    self.left = left
    self.down = down
    self.right = right
    self.embedded = embedded
    self.parent = parent
    self.embedding = embedding
    self.episodes = episodes
    self.past_dominated = past_dominated

  def move_left(self):
    """Move focus to the 'left' (past tense) child, creating a new node if one doesn't exist."""
    if self.left is None:
      self.left = TenseNode(parent=self, past_dominated=True)
    return self.left
    
  def move_down(self):
    """Move focus to the 'down' (perfect tense) child, creating a new node if one doesn't exist."""
    if self.down is None:
      self.down = TenseNode(parent=self, past_dominated=self.past_dominated)
    return self.down
    
  def move_right(self):
    """Move focus to the 'right' (future tense) child, creating a new node if one doesn't exist."""
    if self.right is None:
      self.right = TenseNode(parent=self, past_dominated=self.past_dominated)
    return self.right

  def move_embedded_cur(self):
    """Move focus into an existing embedded child, creating a new node if one doesn't exist."""
    if not self.embedded:
      self.embedded.append(TenseNode(embedding=self, past_dominated=self.past_dominated))
    return self.embedded[-1]
  
  def move_embedded_new(self):
    """Move focus into a new embedded child; create a new node regardless of whether there is an existing one."""
    self.embedded.append(TenseNode(embedding=self, past_dominated=self.past_dominated))
    return self.embedded[-1]

  def move_parent(self):
    """Move focus into the parent."""
    return self.parent
  
  def move_embedding(self):
    """Move focus into the node embedding this node."""
    return self.embedding

  def add_episode(self, ep):
    """Add an episode to this node."""
    self.episodes.append(ep)
    return self
  
  def get_episodes(self):
    """Get all the episodes of this node."""
    return self.episodes
  
  def last_episode(self):
    """Get the last episode of this node."""
    return self.episodes[-1] if self.episodes else None
  
  def bef(self):
    """This is 'before' if not past-dominated, otherwise 'at-or-before'."""
    return AT_OR_BEFORE if self.past_dominated else BEFORE