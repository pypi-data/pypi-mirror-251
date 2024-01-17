#https://orange3.readthedocs.io/projects/orange-development/en/latest/tutorial-settings.html
import ctypes
import os
import sys
from pathlib import Path

import Orange.data
from Orange.widgets import widget
from PyQt5 import QtGui, QtWidgets
from PyQt5 import uic
from orangewidget.utils.signals import Input, Output
from Orange.data import Table
from Orange.base import Learner, Model

class Exctract_domain(widget.OWWidget):

    name = "Extract Domain 1"
    description = "Extract the domain form a model"
    #category =
    icon = "icons/extract.png"
    priority = 3150
    keywords = "program, function"
    class Input:
        data = Input(
            "Data", Table, replaces=["in_data"], default=True
        )
        learner = Input(
            "Learner", Learner, replaces=["in_learner"], default=True
        )
        classifier = Input(
            "Classifier", Model, replaces=["in_classifier"], default=True
        )
        object = Input(
            "Object", object, replaces=["in_object"], default=False, auto_summary=False
        )

    class Outputs:
        data_from_data = Output("Domain from Data", Table, replaces=["data_from_data"])
        data_from_learner = Output("Domain from Learner", Table, replaces=["data_from_learner"])
        data_from_classifier = Output("Domain from Classifier", Table, replaces=["data_from_classifier"])
        data_from_object = Output("Domain from Object", Table, replaces=["data_from_object"])
    def __init__(self):
        # mes_variables_partagees.print_date_jc()
        # cette partie s 'execute à la cration du widget
        super().__init__()# permet d interagir avec la classe parente
        uic.loadUi('widget_designer/Extract_domain.ui', self.window)
        self.data=None
        self.learner=None
        self.classifier=None
        self.object=None
    @Input.data
    def set_data(self, data):
        self.data = data

    @Input.learner
    def set_learner(self, learner):
        self.learner = learner

    @Input.classifier
    def set_classifier(self, classifier):
        self.classifier = classifier

    @Input.object
    def set_object(self, object):
        self.object = object
    def run(self):

        if self.data != None:
            self.process(self.data,"data_from_data")
        if self.learner != None:
            self.process(self.learner,'data_from_learner')
        if self.classifier != None:
            self.process(self.classifier,'data_from_classifier')
        if self.object != None:
            self.process(self.object,'data_from_object')
    def process(self, data_to_process, output_name):
        try:
            out_domain = data_to_process.domain
            out_data = Table.from_domain(out_domain)
        except:
            print("No domain")
        listofzeros = [0] * len(out_data.domain)
        out_data = Table.from_list(out_data.domain,[listofzeros])
        if output_name == 'data_from_data':
            self.Outputs.data_from_data.send(out_data)
        if output_name == 'data_from_learner':
            self.Outputs.data_from_learner.send(out_data)
        if output_name == 'data_from_classifier':
            self.Outputs.data_from_classifier.send(out_data)
        if output_name == 'data_from_object':
            self.Outputs.data_from_object.send(out_data)
