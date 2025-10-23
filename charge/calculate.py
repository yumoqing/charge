from appPublic.log import debug, exception
from ahserver.serverenv import ServerEnv
from sqlor.dbpools import DBPools

class PayeeCharge:
	def __init__(self, resourceid, ctid):
		self.resourceid = resourceid
		self.ctid = ctid
		
	async def get_ct_specs(self, sor):
		sql = """select a.charge_type_spec_mode as spec_type, b.* 
from charge_type a, charge_type_spec b
where a.id = ${ctid} 
	and a.id = b.ctid"""
		ctspecs = await sor.sqlExe(sql, {'ctid': self.ctid})
		return ctspecs

	async def get_payee_charge_rules(self, sor, payee):
		pcrs = await sor.R('payee_charge_rule', {
			'resourceid': self.resourceid,
			'ctid': self.ctid,
			'payeeid': payee
		})
		return pcrs

	def get_spec_by_ctsid(self, ctsid, ctspecs):
		for spec in ctspecs:
			if ctsid == spec.id:
				return spec
		return None

	async def calculate_charge(self, sor, payeeids, data):
		ctspecs = await self.get_ct_specs(sor)
		charges = {}
		for payeeid in payeeids:
			charge_arr = []
			pcrs = await self.get_payee_charge_rule(sor, payeeid)
			for pcr in pcrs:
				spec = self.get_spec_by_ctsid(pcr.ctsid, ctspecs)
				if spec is None:
					continue
				charge = pcr.copy()
				d = data.get(spec.spec_name)
				if d is None:
					continue
				cnt = data.get(spec.count_name, 1)
				if spec_mode == 'spec_name':
					if d == pci.spec_value:
						pci.amount = pcr.charge_amount * cnt
				elif spec_mode == 'spec_amount':
					if pcr.charge_unit is None or pcr.charge_unit == 0:
						pci.charge_unit = 1
					charge.amount = d * pcr.charge_amount / pcr.charge_unit
				else:
					continue
				charge_arr.append(charge)
			charges[payeeid] = charge_arr
		return charges

