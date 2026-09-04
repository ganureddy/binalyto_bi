import frappe

def create_customer_for_student(student_name):
    """Enqueued job: create a Customer (+ auto Contact via ERPNext hook) for one Student."""
    try:
        student = frappe.get_doc("Student", student_name)
        customer_name = (student.first_name or student.title or student.name).strip()

        if frappe.db.exists("Customer", {"customer_name": customer_name}):
            return

        customer = frappe.new_doc("Customer")
        customer.customer_name = customer_name
        customer.customer_type = "Individual"
        customer.customer_group = "Individual"
        customer.territory = "India"
        customer.gst_category = "Unregistered"

        if student.student_mobile_number:
            customer.mobile_no = student.student_mobile_number
        if student.student_email_id:
            customer.email_id = student.student_email_id

        customer.insert(ignore_permissions=True)
        frappe.db.commit()
    except Exception:
        frappe.db.rollback()
        frappe.log_error(
            title=f"Customer creation failed for student {student_name}",
            message=frappe.get_traceback()
        )
