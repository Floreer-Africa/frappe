import frappe
from frappe.website.page_renderers.template_page import TemplatePage


class PrintPage(TemplatePage):
	"""
	default path returns a printable object (based on permission)
	/Quotation/Q-0001
	"""

	def can_render(self):
		parts = self.path.split("/", 1)
		if len(parts) != 2:
			return False
		# Exactly the DocType's name: the lookup ignores case but importing its
		# controller does not, so "/dashboard/.env" raised ImportError and
		# answered 500 instead of 404 (Floreer framework#294).
		return frappe.db.get_value("DocType", parts[0], "name", cache=True) == parts[0]

	def render(self):
		parts = self.path.split("/", 1)
		frappe.form_dict.doctype = parts[0]
		frappe.form_dict.name = parts[1]
		self.set_standard_path("printview")
		return super().render()
