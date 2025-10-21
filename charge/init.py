from ahserver.serverenv import ServerEnv
from charge.calculate import PayeeCharge
def load_charge():
	env = ServerEnv()
	env.PayeeCharge = PayeeCharge

