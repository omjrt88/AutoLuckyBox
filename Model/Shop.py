class User:
  def __init__(self, user='', password=''):
    self.user = user
    self.password = password

class Shop:
  def __init__(self, shop='', baseUrl='', users=[], hour=5):
    self.shop = shop
    self.baseUrl = baseUrl
    self.users = []
    self.hour = hour
    for user in users:
      self.users.append(User(**user))
