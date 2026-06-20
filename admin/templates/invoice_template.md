# INVOICE

**Invoice Number:** {{ INVOICE_NUMBER }}  
**Issue Date:** {{ ISSUE_DATE }}  
**Due Date:** {{ DUE_DATE }}  

---

### Billed To:
**Client:** {{ CLIENT_NAME }}  
**Address:** {{ CLIENT_ADDRESS }}  
**Contact:** {{ CLIENT_EMAIL }}  

### From:
**Consultant:** {{ CONSULTANT_NAME }}  
**Address:** {{ CONSULTANT_ADDRESS }}  
**Email:** {{ CONSULTANT_EMAIL }}  
**Phone:** {{ CONSULTANT_PHONE }}  

---

## Billing Summary

| Description | Qty / Hours | Unit Price / Rate | Total |
| :--- | :---: | :---: | :---: |
| {{ ITEM_1_DESC }} | {{ ITEM_1_QTY }} | {{ ITEM_1_RATE }} | {{ ITEM_1_TOTAL }} |
| {{ ITEM_2_DESC }} | {{ ITEM_2_QTY }} | {{ ITEM_2_RATE }} | {{ ITEM_2_TOTAL }} |
| {{ ITEM_3_DESC }} | {{ ITEM_3_QTY }} | {{ ITEM_3_RATE }} | {{ ITEM_3_TOTAL }} |

**Total Due: {{ TOTAL_DUE }}**

---

## Payment Instructions
Please send payments via bank transfer to the following account:

* **Bank Name:** {{ BANK_NAME }}
* **Account Name:** {{ BANK_ACCOUNT_NAME }}
* **Account Number (IBAN):** {{ BANK_ACCOUNT_NUMBER }}
* **Sort Code (BIC):** {{ BANK_SORT_CODE }}
* **Payment Reference:** Please use invoice number `{{ INVOICE_NUMBER }}` as your payment reference.

*If you have any questions about this invoice, please contact {{ CONSULTANT_EMAIL }}.*

Thank you for your business!
