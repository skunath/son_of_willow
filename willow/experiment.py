import jinja2

class Experiment(object):
    def __init__(self):
        self.user_count = 0
        self.is_running = 0

        self.total_rounds = 3
        self.num_rounds_remaining = 3

        self.total_subjects = 2

        self.current_subjects_connected = []

        self.experiment_paused = False


        # TODO: Need this be optional?
        self.rounds_remaining = []
        self.emitter = None


    def set_emitter(self, emitter):
        if self.emitter == None:
            self.emitter = emitter

    # method to determine whether the experiment is actually running
    def is_running(self):
        return self.is_running

    def subject_connected(self, subject_id):
        self.current_subjects_connected.append(subject_id)

    def get_subjects_connected(self):
        return self.current_subjects_connected

    # method to start the experiment
    def start_experiment(self):
        # make sure to set the experiment to a running state
        self.is_running = 1
        print "the experiment has internally commenced"

    def info(self):
        print "test"

    def set_users(self):
        self.user_count += 1

    def pause_experiment(self):
        if self.experiment_paused:
            self.experiment_paused = False
        else:
            self.experiment_paused = True
        return self.experiment_paused


    def rounds_remaining(self):
        return self.num_rounds_remaining

    def current_round(self):
        return self.total_rounds


    def log_action(self, action):
        self.emitter('log_message', {'signal':'connected','data': 1}, namespace='/admin_control')

    # in some instances will we need to push down whole page updates?
    # probably should have code here for just jquery based updates.0
    def prepare_stage_for_subject(self, subject_id):
        current_template = open("./experiment_templates/stage_1_offer.html")

        #        template = jinja2.Template('Hello {{ name }}!')
        #       output = template.render(name='John Doe')
        template = jinja2.Template(current_template.read())
        output = template.render(amount_offered='17')


        name = "tester..."

        return output


    def user_action_received(self, message, emit_method):
        print "Need to be overloaded...."

