# -*- coding: utf-8 -*-
"""The implementation for the ginkgo anki plugin."""

import json
from anki.exporting import Exporter #pylint: disable=F0401
from anki.utils import ids2str #pylint: disable=F0401
from anki.utils import splitFields #pylint: disable=F0401
from anki.hooks import addHook #pylint: disable=F0401

class GinkgoExporter(Exporter):
    """The json exporter for ginkgo."""

    key = _("Ginkgo")
    ext = ".json"

    def __init__(self, col):
        Exporter.__init__(self, col)
        self.count = -1 #initialized with an invalid state; should be set in doExport

    def doExport(self, outfile):
        """Using the database, construct a string to place in outfile representing the deck."""
        card_ids = self.cardIds()

        selection = "\n".join(["", "select guid, flds, tags from notes",
                               "where id in",
                               "(select nid from cards",
                               "where cards.id in "+ids2str(card_ids)+")"])

        notes = {}
        for note_id, flds, tags in self.col.db.execute(selection):
            notes[str(note_id)] = {"fields" : [self.escapeText(f) for f in splitFields(flds)],
                                   "tags" : [t for t in tags.split()]}

        self.count = len(notes)
        out = json.dumps(notes, sort_keys=True, indent=4, separators=(',', ': '))
        outfile.write(out.encode("utf-8"))

def add_ginkgo_exporter(exps):
    """Add GinkgoExporter to the list of possible exporters in Anki."""
    #Inner function is copypasta from anki.exporting
    def get_id(obj): #pylint: disable=C0111
        return ("%s (*%s)" % (obj.key, obj.ext), obj)

    exps.append(get_id(GinkgoExporter))

addHook("exportersList", add_ginkgo_exporter)
