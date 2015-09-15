#!/usr/bin/env Python

""" The music library support for socos """

from __future__ import print_function


class MusicLibrary(object):
    """ Class that implements music library support for socos """

    def tracks(self, sonos, *args):
        """ Get available tracks of a device / groups """
        return self._search_and_play(sonos, 'tracks', *args)

    def playlists(self, sonos, *args):
        """ Get available playlists of a device / groups """
        return self._search_and_play(sonos, 'playlists', *args)

    def sonos_playlists(self, sonos, *args):
        """ Get available sonos playlists of a device / groups """
        return self._search_and_play(sonos, 'sonos_playlists', *args)

    def albums(self, sonos, *args):
        """ Get available albums of a device / groups """
        return self._search_and_play(sonos, 'albums', *args)

    def artists(self, sonos, *args):
        """ Get available artists of a device / groups """
        return self._search_and_play(sonos, 'artists', *args)

    def _search_and_play(self, sonos, data_type, *args):
        if len(args) < 1:
            items = sonos.music_library.get_music_library_information(
                search_type=data_type)
        else:
            items = sonos.music_library.get_music_library_information(
                search_type=data_type, search_term=args[0])

        if len(args) < 2:
            for string in self._print_results(data_type, items):
                yield string
        else:
            yield self._play(sonos, data_type, items, *args)

    @staticmethod
    def _play(sonos, data_type, results, *args):
        action, number = args[1:]

        if action not in ['add', 'replace']:
            message = "'Action must be one of 'add' or 'replace'"
            raise ValueError(message)

        try:
            number = int(number) - 1
        except ValueError:
            raise ValueError('Play number must parseable as integer')
        if number not in range(len(results)):
            if len(results) == 0:
                message = 'No results to play from'
            elif len(results) == 1:
                message = 'Play number can only be 1'
            else:
                message = 'Play number has to be within the range 1 to {}'.\
                    format(len(results))
            raise ValueError(message)
        item = results[number]
        out = "Added {} to queue: '{}'"
        if action == 'replace':
            sonos.clear_queue()
            out = "Queue replaced with {}: '{}'"
        sonos.add_to_queue(item)
        title = item.title
        if hasattr(title, 'decode'):
            title = title.encode('utf-8')
        return out.format(data_type, title)

    @staticmethod
    def _print_results(data_type, results):
        """ Print the results out nicely. """
        print_patterns = {
            'tracks': '{title} on {album} by {creator}',
            'albums': '{title} by {creator}',
            'artists': '{title}',
            'playlists': '{title}',
            'sonos_playlists': '{title}'
        }

        index_length = len(str(len(results)))
        for index, item in enumerate(results):
            item_dict = item.to_dict()
            for key, value in item_dict.items():
                if hasattr(value, 'decode'):
                    item_dict[key] = value.encode('utf-8')
            number = '({{: >{}}}) '.format(index_length).format(index + 1)
            yield number + print_patterns[data_type].format(**item_dict)
