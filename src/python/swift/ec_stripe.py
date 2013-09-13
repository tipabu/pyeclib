import math

#
# A striping-only driver for EC.  This is
# pretty much RAID 0.
#
class ECStripingDriver(object):
  def __init__(self, k, m):
    """
    Stripe an arbitrary-sized string into k fragments
    :param k: the number of data fragments to stripe
    :param m: the number of parity fragments to stripe
    :raises: ECDriverError if there is an error during encoding
    """
    self.k = k

    if m != 0:
      raise ECDriverError("This driver only supports m=0")

    self.m = m

  def encode(self, bytes):
    """
    Stripe an arbitrary-sized string into k fragments
    :param bytes: the buffer to encode
    :returns: a list of k buffers (data only)
    :raises: ECDriverError if there is an error during encoding
    """
    # Main fragment size
    fragment_size = math.ceil(len(bytes) / float(self.k))

    # Size of last fragment
    last_fragment_size = len(bytes) - (fragment_size*self.k-1)

    fragments = []
    offset = 0
    for i in range(self.k-1):
      fragments.append(bytes[offset:fragment_size])
      offset += fragment_size

    fragments.append(bytes[offset:last_fragment_size])

    return fragments
  
  def decode(self, fragment_payloads):
    """
    Convert a k-fragment data stripe into a string 
    :param fragment_payloads: fragments (in order) to convert into a string
    :returns: a string containing the original data
    :raises: ECDriverError if there is an error during decoding
    """

    if len(fragment_payloads) != self.k:
      raise ECDriverError("Decode requires %d fragments, %d fragments were given" % (len(fragment_payloads), self.k))

    ret_string = ''

    for fragment in fragment_payloads:
      ret_string += fragment 

    return ret_string
  
  def reconstruct(self, available_fragment_payloads, missing_fragment_indexes, destination_index):
    """
    We cannot reconstruct a fragment using other fragments.  This means that
    reconstruction means all fragments must be specified, otherwise we cannot
    reconstruct and must raise an error.
    :param available_fragment_payloads: available fragments (in order) 
    :param missing_fragment_indexes: indexes of missing fragments
    :returns: a string containing the original data
    :raises: ECDriverError if there is an error during reconstruction
    """
    if len(available_fragment_payloads) != self.k:
      raise ECDriverError("Reconstruction requires %d fragments, %d fragments were given" % (len(available_fragment_payloads), self.k))

    return available_fragment_payloads

  def fragments_needed(self, missing_fragment_indexes):
    """
    By definition, all missing fragment indexes are needed to reconstruct,
    so just return the list handed to this function.
    :param missing_fragment_indexes: indexes of missing fragments
    :returns: missing_fragment_indexes
    """
    return missing_fragment_indexes 

  def get_metadata(self, fragment):
    """
    This driver does not include fragment metadata, so return an empty string
    :param fragment: a fragment
    :returns: empty string
    """
    return '' 

  def verify_stripe_metadata(self, fragment_metadata_list):
    """
    This driver does not include fragment metadata, so return true
    :param fragment_metadata_list: a list of fragments
    :returns: True 
    """
    return True 
