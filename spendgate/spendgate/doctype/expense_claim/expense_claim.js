// Copyright (c) 2026, SD and contributors
// For license information, please see license.txt

frappe.ui.form.on("Expense Claim", {
    setup(frm){
        frm.set_query("budget", ()=>{
            return{
                query:"spendgate.api.filter_budgets",
                filters:{
                    department:frm.doc.department,
                }
            }
        });
    },

	refresh(frm) {
        let colors = {
            "Draft":"gray",
            "Pending Approval":"orange",
            "Approved":"green",
            "Rejected":"red",
            "Reimbursed":"blue",
            "Cancelled":"red"
        }
        frm.dashboard.add_indicator(frm.doc.status, colors[frm.doc.status]);

        let user = frappe.user.has_role["SG Finance Manager"]


        if((frappe.user.has_role("SG Department Head") || frappe.user.has_role("SG Finance Manager") && frm.doc.status == "Pending Approval")){
            frm.add_custom_button("Approve", ()=>{
                frm.doc.status = "Approved";
                frm.set_value({
                    status:"Approved",
                    approved_by:frappe.session.user
                });
                frm.save();
                frm.reload_doc();
            });
        

            frm.add_custom_button("Reject Claim",()=>{
                let dialog = new frappe.ui.Dialog({
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
                frappe.prompt({
                    label:"Department Name",
                    fieldname:"department_name",
                    fieldtype:"Link",
                    options:"Department"
                },(values)=>{ 
                    frappe.confirm("Are you sure you want to submit?", 
                        ()=>{   
                            frappe.call({
                                method: "spendgate.api.change_department",
                                args: {
                                    department_name:values.department_name,
                                    document_name:frm.doc.name
                                },
                                callback: (r)=>{
                                    frm.trigger("department_name")
                                }
                            })
                        },
                        ()=>{
                            //cancell process
                            frappe.msgprint("Process Cancelled")
                        });

                });
                "Reassign Department",
                "Reassign"
            });
            }
    },
});

frappe.ui.form.on("Expense Line",{

    amount(frm, cdt, cdn){

        let total_budget = 0;
        frm.doc.item_lines.forEach((row)=>{
            total_budget += row.amount;
        });
    }
});
