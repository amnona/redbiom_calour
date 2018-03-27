from logging import getLogger

from calour.database import Database

logger = getLogger(__name__)


class Phenotype(Database):
    '''redbiom calour interface
    '''
    def __init__(self, exp=None):
        '''Called every time a database interface is created (e.g. when creating a plot, etc.)
        Can put here obtaining the database api address, handshake, etc.

        Note: the methods variable tells calour what things can be done with this database. can include:
            'get' if database interface supports get_seq_annotation_strings()
                This means the database returns a list of strings describing the selcted feature.
                used for the interavtive heatmap display when clicking a feature.
            'annotate' if database interface supports add_annotation()
                This means the user can click the "annotate" button to add selected sequences to the database. The GUI is fully
                provided by the database module.
            'enrichment' if database interface supports get_feature_terms()
                This means the database supports statistical tests to identify interesting properties about a group of features.
                Used for example in the "erichment" button in the heatmap.
        In minimum, the database should support the 'get' method.

        Parameters
        ----------
        exp: calour.Experiment
            the calour Experiment this database is associated with.
            useful if you want to store data obtained from the database in the experiment to prevent multiple database queries
            about the same data. In that case, can store the data in exp.exp_metadata['__redbiom_XXX']
        '''
        super().__init__(exp=exp, database_name='redbiom', methods=['get'])
        logger.debug('redbiom calour database interface initialized')

    def get_seq_annotation_strings(self, feature):
        '''Get nice string summaries of annotations for a given sequence

        Parameters
        ----------
        feature : str
            the DNA sequence to query the database about

        Returns
        -------
        shortdesc : list of (dict,str) (annotationdetails, annotationsummary)
            a list of:
                annotationdetails : dict containing at least the following:
                    'seqid' : str
                        the feature annotated (i.e. the sequence string)
                    'annotationtype : str
                        indicates the color for the list. we should improve this part in calour. currently set to "redbiom"
                        and the list entry will be colored black
                    ADDITIONAL ITEMS:
                        for internal database interface use.
                        (for example details the database can use for the show_annotation_info() function called when an item in the list
                        is double clicked in the heatmap GUI)
                annotationsummary : str
                    a short summary of the annotation. Displayed in the heatmap gui in the listbox.
        '''
        shortdesc = []
        # add to shortdesc all information about this feature from the database.
        return shortdesc

    def show_annotation_info(self, annotation):
        '''Show info about the annotation (can open an browser window or a python gui - whatever you prefer)
        Called when double clicking an annotation from the heatmap gui.
        annotation is the dict part returned from get_seq_annotation_strings().

        Parameters
        ----------
        annotation : dict
            should contain 'feature'
        '''
        # this is an example from the phenodb calour interface
        # should overwrite!
        journal_base = 'http://ijs.microbiologyresearch.org/content/journal/ijsem/'
        new = 2
        seq = annotation['feature']
        data = self.phenotype_data[seq]

        if 'article doi' in data:
            address = journal_base + data['article doi']
        else:
            logger.warn('no doi for phenotype database - cannot open link')
            return
        webbrowser.open(address, new=new)
