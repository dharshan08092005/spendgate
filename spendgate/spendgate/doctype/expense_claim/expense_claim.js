// Copyright (c) 2026, SD and contributors
// For license information, please see license.txt

//in hold
frappe.ui.form.on("Expense Claim", {
    setup(frm){
        frm.set_query("Budget", ()=>{
            return{
                filters:{
                    department:frm.doc.department,
                }
            }
        });
    },

	refresh(frm) {
        frm.dashboard.add_indicator("Status","gray", {"status":"Draft"});
        frm.dashboard.add_indicator("Status","orange", {"status":"Pending Approval"});
        frm.dashboard.add_indicator("Status", "green", {"status":"Approved"});
        frm.dashboard.add_indicator("Status","red", {"status":"Rejected"});
        frm.dashboard.add_indicator("Status","blue", {"status":"Reimbursed"});
        frm.dashboard.add_indicator("Status","red", {"status":"Cancelled"});

        let user = frappe.session.user
        let role = frappe.get_roles(user)
        if((role.includes("SG Department Head") || role.includes("SG Finance Manager") && frm.doc.status == "Pending Approval")){
            frm.add_custom_button("Approve", ()=>{
                frm.doc.status = "Approved"
            });
        }

        frm.add_custom_button("Reject Claim",()=>{
            let dialog = new frappe.ui.dialog({
                fields:[
                    {
                        label:"Rejection reason",
                        fieldname:"rejection_reason",
                        fieldtype:"Small Text",
                        reqd:1
                    }
                ],
                primary_action_label:"Submit",
                primary_action(values){
                    dialog.hide();
                }
            });
            dialog.show();
        });
        frm.add_custom_button("Reassign Department", ()=>{
            frppe.prompt({
                label:"Department Name",
                fieldname:"department_name",
                fieldtype:"data"
            },(values)=>{
                
                frappe.confirm("Are you sure you want to submit?", 
                    (values)=>{
                            frappe.call("spendgate.api.change_department",
                                {
                                    department_name:values.department_name,
                                    document_name:frm.doc.name
                                }
                            )
                        },
                    ()=>{

                    });
            });
        });
	},
});

frappe.ui.form.on("Expense Line",{
    amount(frm, cdt, cdn){
        // frappe.model.set_value()

        let row = frappe.get_doc(cdt, cdn);

    }
});
