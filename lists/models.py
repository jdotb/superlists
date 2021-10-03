from django.db import models

#   #   #   #   #   #   #   ##   #   #   #   #   #   #   #
# This gets our test as far as:
#
#  [...]
#  first_item(save)
"""
class Item(object):
     pass
"""

#
# edit > rerun test
#   #   #   #   #   #   #   ##   #   #   #   #   #   #   #

"""
class Item(models.Model):
    pass
"""


#   #   #   #   #   #   #   ##   #   #   #   #   #   #   #
# The above produces 'no such table: list_item (db error)
# migrations.py give ability to add/remove tables/columns based on changes to models.py
#
# makemigrations is used for this
#
# $ python manage.py makemigrations
#
# now rerun test, but use:
# $ python manage.py test lists
#
# ! AttributeError: 'Item' object has no attribute 'text'
# *
#       Note: We've gotten all the way through saving the last two Items, and checked if saved in db, but Django
#       hasn't remembered the .text attribute.
#   #   #   #   #   #   #   ##   #   #   #   #   #   #   #
class List(models.Model):
    pass

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

#   #   #   #   #   #   #   ##   #   #   #   #   #   #   #
# The above produces 'no such column: list_item.text
# This is because we've added another new field to our db, but didn't migrate.
#       * also need to add a default
# run:
#   $ python manage.py makemigrations
