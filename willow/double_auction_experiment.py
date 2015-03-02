import jinja2

from experiment import Experiment

class DoubleAuctionExperiment(Experiment):
    def __init__(self, *args, **kwargs):
        super(DoubleAuctionExperiment, self).__init__(*args, **kwargs)
        print "Double auction experiment object instantiated"


    def prepare_stage_for_subject(self, subject_id):
        current_template = open("./double_auction/interface.html")

        #        template = jinja2.Template('Hello {{ name }}!')
        #       output = template.render(name='John Doe')
        template = jinja2.Template(current_template.read())
        output = template.render()


        return output
