# -*- coding: utf-8 -*-

import json
from anki.exporting import Exporter #pylint: disable=F0401
from anki.utils import ids2str #pylint: disable=F0401
from anki.utils import splitFields #pylint: disable=F0401
from anki.hooks import addHook #pylint: disable=F0401

class GinkgoExporter(Exporter):

    key = _("Ginkgo")
    ext = ""

    def __init__(self, col):
        Exporter.__init__(self, col)

    def doExport(self, file):
       	cardIds = self.cardIds()
        data = []

        selection = "\n".join(["", "select guid, flds, tags from notes",
                               "where id in",
                               "(select nid from cards",
                               "where cards.id in "+ids2str(cardIds)+")"])

        notes = {}
        for id, flds, tags in self.col.db.execute(selection):
            notes[str(id)] = {"fields" : [self.escapeText(f) for f in splitFields(flds)],
                              "tags" : [t for t in tags.split()]}

        self.count = len(notes)
        out=json.dumps(notes, sort_keys=True, indent=4, separators=(',', ': '))
        file.write(out.encode("utf-8"))

def onExportersList( exps ):

    #Inner function is copypasta from anki.exporting
    def id(obj):
        return ("%s (*%s)" % (obj.key, obj.ext), obj)

    exps.append(id(GinkgoExporter))

addHook("exportersList", onExportersList)
