""" The RenderingAdjustments class contains all functionality related to
adjusting value like volume, bass, treble. """

from __future__ import print_function
import sys


class RenderingAdjustments(object):
    """ The RenderingAdjustments class contains all functionality related to
    adjusting value like volume, bass, treble. """

    def __init__(self, soco):
        self.soco = soco

    @staticmethod
    def err(message):
        """ print an error message """
        print(message, file=sys.stderr)

    def volume(self, operator):
        """ Adjust the volume up or down with a factor from -100 to 100 """
        value = self.control(operator, self.soco.volume, range(-100, 100))
        if value:
            self.soco.volume = value
        return self.soco.volume

    def bass(self, operator):
        """ Adjust the bass up or down with a factor from -20 to 20 """
        value = self.control(operator, self.soco.bass, range(-20, 20))
        if value:
            self.soco.bass = value
        return self.soco.bass

    def treble(self, operator):
        """ Adjust the treble up or down with a factor from -20 to 20 """
        value = self.control(operator, self.soco.treble, range(-20, +20))
        if value:
            self.soco.treble = value
        return self.soco.treble

    def control(self, operator, property, range):
        factor = self.get_factor(operator)
        if not factor:
            return False

        if not operator[0] in ['+','-']:
            self.err("Valid operators are + and -")
            return False

        updated_value = self.get_updated_value(int(property), operator[0], factor)
        if not updated_value in range:
            factor = 1
            updated_value = self.get_updated_value(int(property), operator[0], factor)

        return updated_value

    @staticmethod
    def get_updated_value(property, operator, factor):
        return eval("%d %s %d" % (property, operator, factor))

    def get_factor(self, operator):
        """ get the factor to adjust the volume, bass, treble... with """
        factor = 1
        if len(operator) > 1:
            try:
                factor = int(operator[1:])
            except ValueError:
                self.err("Adjustment factor for has to be a int.")
                return
        return factor
