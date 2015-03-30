import jinja2

from experiment import Experiment

class DoubleAuctionExperiment(Experiment):
    def __init__(self, *args, **kwargs):
        super(DoubleAuctionExperiment, self).__init__(*args, **kwargs)
        print "Double auction experiment object instantiated"
        self.offer_count = 0
        self.buy_offers = {}
        self.sell_offers = {}

        # user data preparation area
        self.user_data = {}


    def prepare_subject_data(self, subject_id):
        self.user_data[subject_id] = {}

        self.user_data[subject_id]["working_capital"] = 10
        self.user_data[subject_id]["current_inventory"] = 5


    def prepare_stage_for_subject(self, subject_id):
        # prepare data for each subject first
        self.prepare_subject_data(subject_id)

        current_template = open("./double_auction/interface.html")
        #        template = jinja2.Template('Hello {{ name }}!')
        #       output = template.render(name='John Doe')
        template = jinja2.Template(current_template.read())
        output = template.render()



        return output

    def process_offer(self, message):
        action = message["action"]
        self.offer_count += 1
        offer_id = self.offer_count
        offer_amount = message["offer_amount"]
        user = message["user"]

        if action == "sell":
            self.sell_offers[int(offer_amount)] = {"id": offer_id, "user": user, "amount": offer_amount}
        elif action == "buy":
            self.buy_offers[int(offer_amount)] = {"id": offer_id, "user": user, "amount": offer_amount}


    def user_action_received(self, message, emit_method):
        user = message["user"]
        action = message["action"]
        print action
        self.log_action("test")

        if (action == "offer_entered"):
            # here we process the offer that came in from the participant
            #self.process_offer(message)
            # broadcast a message, this might only apply if the offer affects things
            emit_method('interface_message', {'received_action': "post_bid", 'offer_type': message["offer_type"], 'offer_id':self.offer_count, 'offer_amount': message["offer_amount"]}, broadcast=True)

