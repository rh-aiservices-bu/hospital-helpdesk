
# Pavilion Hospital - Standard Operating Procedures

## Document ID: PH-SOP-EQUIP-001
## Title: Medical Equipment Management & Incident Reporting
## Version: 3.1
## Date: 2026-07-21

---

### **Table of Contents**
1.  **Introduction**
    1.1. Purpose and Scope
    1.2. Definitions
    1.3. Roles and Responsibilities
2.  **General Equipment Acquisition and Deployment**
    2.1. New Equipment Request Protocol (NERP)
    2.2. Vendor Selection and Vetting
    2.3. Capital Expenditure Approval Process
    2.4. Asset Tagging and Inventory Management
    2.5. Initial Inspection and Burn-in Period
3.  **Standard Usage Protocols**
    3.1. User Authentication and Access Control
    3.2. Pre-Use Inspection Checklist (PUIC)
    3.3. Standard Sanitation Procedures Post-Use
    3.4. Battery Management for Portable Devices
4.  **Maintenance and Calibration**
    4.1. Scheduled Preventative Maintenance (PM) Roster
    4.2. Calibration Records and Standards (NIST Traceability)
    4.3. Software and Firmware Update Policy
    4.4. Unscheduled Maintenance Requests
5.  **Faulty Equipment & Incident Reporting**
    5.1. Immediate Actions for Faulty Equipment
    5.2. **Procedure for Infusion Pumps**
    5.3. Procedure for Diagnostic Imaging Equipment (X-Ray, MRI)
    5.4. Procedure for Patient Monitoring Systems
    5.5. Procedure for Surgical Equipment
6.  **Decommissioning and Disposal**
    6.1. End-of-Life (EOL) Assessment Criteria
    6.2. Data Sanitization and Removal (HIPAA Compliance)
    6.3. Safe Disposal and Recycling Procedures
7.  **Appendix**
    7.1. Contact List: Department Heads & On-Call Biomed Staff
    7.2. Form: PH-FORM-INC-001 - Equipment Incident Report
    7.3. Escalation Matrix for Critical Failures

---

### **1. Introduction**

#### **1.1. Purpose and Scope**
This document outlines the standard operating procedures (SOPs) for the lifecycle management of all medical equipment within Pavilion Hospital. This includes acquisition, deployment, usage, maintenance, incident reporting, and decommissioning. Adherence to these procedures is mandatory for all clinical and administrative staff to ensure patient safety, regulatory compliance (including FDA, TJC, and CMS), and operational efficiency. The scope covers all devices used in patient care, diagnostics, and monitoring, whether owned, leased, or rented.

#### **1.2. Definitions**
*   **Biomedical Engineering (Biomed):** The department responsible for managing, maintaining, and repairing medical equipment. Located in Wing C, Room 112.
*   **Clinical Staff:** All licensed personnel directly involved in patient care (Nurses, Doctors, Technicians, etc.).
*   **ServiceNow Portal:** The hospital's official IT service management (ITSM) platform for logging tickets and requests. Accessible at http://pavilion.service-now.com.
*   **Asset Tag:** A unique barcode label affixed to each piece of equipment for tracking and inventory.
*   **OEM:** Original Equipment Manufacturer.

#### **1.3. Roles and Responsibilities**
*   **Clinical Staff:** Responsible for correct operation, pre-use checks, and immediate reporting of equipment faults via the ServiceNow Portal.
*   **Biomedical Engineering:** Responsible for all technical maintenance, repair, calibration, and final decommissioning of equipment.
*   **Central Supply:** Responsible for managing the inventory of available and ready-for-use portable equipment, including infusion pumps and patient monitors.
*   **Unit Manager:** Responsible for ensuring their staff are trained on and compliant with these SOPs.

---
### **2. General Equipment Acquisition and Deployment**

#### **2.1. New Equipment Request Protocol (NERP)**
Any department wishing to acquire new medical equipment must initiate a New Equipment Request Protocol (NERP) form via the ServiceNow portal. The request must include a detailed clinical justification for the new equipment, expected patient benefits, required training for staff, and an estimated annual usage rate. The request will be automatically routed to the Department Head for initial review.

#### **2.2. Vendor Selection and Vetting**
Upon Department Head approval, the NERP is routed to the Procurement department and the Biomedical Engineering department simultaneously. Procurement is responsible for identifying at least three potential vendors and obtaining quotes. Biomed is responsible for conducting a technical evaluation of the proposed equipment from each vendor, assessing its compatibility with existing hospital infrastructure, long-term reliability, and the availability of OEM service and parts. No vendor may be selected without Biomed's technical approval.

#### **2.3. Capital Expenditure Approval Process**
For any equipment purchase exceeding $5,000, the NERP, along with vendor quotes and Biomed's technical assessment, must be submitted to the Capital Expenditure Review Board (CERB). The board, which convenes monthly, will assess the request based on clinical need, budgetary availability, and alignment with the hospital's strategic technology roadmap. Purchases under $5,000 may be approved directly by the Department Head if within their annual budget.

#### **2.4. Asset Tagging and Inventory Management**
Upon arrival, all new equipment must be delivered directly to the Biomedical Engineering department. Biomed will perform an initial inspection to verify the shipment matches the purchase order. They will then assign a unique Pavilion Hospital Asset Tag number and affix the physical tag to the device. The device's serial number, model, purchase date, and asset tag will be entered into the hospital's Asset Management database before the device is released.

#### **2.5. Initial Inspection and Burn-in Period**
All new critical life-support and diagnostic equipment (e.g., ventilators, defibrillators, anesthesia machines) must undergo a mandatory 72-hour "burn-in" period within the Biomed lab. During this time, the device is run continuously under simulated conditions to detect any early hardware failures. Following a successful burn-in, a full calibration and safety check is performed. Only then will the equipment be cleared for clinical deployment.

---
### **3. Standard Usage Protocols**

#### **3.1. User Authentication and Access Control**
Many advanced medical devices require user login for accountability and to ensure operation is restricted to trained personnel. Access is provisioned based on roles defined in the hospital's Active Directory system. Staff must not share login credentials. All user activity on these devices is logged and subject to audit.

#### **3.2. Pre-Use Inspection Checklist (PUIC)**
Before connecting any equipment to a patient, the responsible clinical staff member must perform a Pre-Use Inspection Checklist (PUIC). While specific checklists exist for complex devices, the universal minimum checklist is as follows:
1.  Visually inspect for physical damage (cracked casing, frayed cables).
2.  Verify power status (plugged in, adequate battery charge).
3.  Confirm all necessary probes, sensors, and disposables are present and not expired.
4.  Perform a system self-test if available on the device.
5.  Ensure the device is clean and has a "Ready for Use" tag from Central Supply or Biomed.
Any failures during the PUIC must be reported immediately as per Section 5.

#### **3.3. Standard Sanitation Procedures Post-Use**
All medical equipment must be cleaned and disinfected between patients according to the procedures outlined in the hospital's Infection Control manual (DOC ID: PH-INF-CTRL-004). Use only hospital-approved disinfectant wipes. Do not immerse equipment in liquid. Pay special attention to high-touch surfaces such as keypads and handles.

#### **3.4. Battery Management for Portable Devices**
To maximize the lifespan and availability of battery-powered portable devices, staff must adhere to the "plug-when-not-in-use" policy. Whenever a portable device (e.g., infusion pump, mobile monitor) is not in active use, it should be returned to its designated charging station. Do not leave devices unplugged on countertops. For devices with swappable batteries, ensure a fresh battery is inserted and the depleted one is placed in the charging cradle.

---
### **4. Maintenance and Calibration**

#### **4.1. Scheduled Preventative Maintenance (PM) Roster**
Biomedical Engineering maintains a master PM roster for all medical equipment. PM is typically performed quarterly, semi-annually, or annually depending on the device type and OEM recommendations. Biomed technicians will coordinate with Unit Managers to temporarily remove equipment from service for PM. A "PM in Progress" tag will be placed on the device slot.

#### **4.2. Calibration Records and Standards (NIST Traceability)**
All calibrations must be performed using test equipment that is certified and traceable to the National Institute of Standards and Technology (NIST). Calibration records, including the "as found" and "as left" readings, must be digitally logged in the asset's record in the Asset Management database. Calibration stickers indicating the date performed and the next due date must be affixed to the device.

#### **4.3. Software and Firmware Update Policy**
All software and firmware updates for medical devices are managed exclusively by the Biomedical Engineering department. Unsolicited updates from vendors must be refused. Biomed will test all patches in a sandbox environment to ensure they do not adversely affect device functionality or network connectivity. Critical security patches will be deployed on an accelerated timeline.

#### **4.4. Unscheduled Maintenance Requests**
For non-critical issues (e.g., cosmetic damage, intermittent non-fatal errors), clinical staff should file a Level 4 "General Maintenance Request" ticket in the ServiceNow portal. Biomed will address these requests during normal business hours, typically within 48-72 hours.

---
### **5. Faulty Equipment & Incident Reporting**

#### **5.1. Immediate Actions for Faulty Equipment**
If any piece of medical equipment is observed to be malfunctioning, damaged, or producing an error, clinical staff must take the following immediate actions:
1.  Safely remove the device from patient use.
2.  If applicable, provide an alternative device to ensure continuity of care.
3.  Attach a "FAULTY - DO NOT USE" tag to the device, clearly marking the date, your name, and a brief description of the issue.
4.  Follow the specific reporting procedure for the device type as outlined in the following sections. Never leave a potentially faulty device in a clean supply room.

#### **5.2. Procedure for Infusion Pumps**
This section details the required steps for handling malfunctioning infusion pumps, including but not limited to Alaris syringe drivers and Medfusion volumetric pumps.

*   **General Infusion Pump Failure:**
    1.  Remove the device from service and tag it as faulty.
    2.  File a Level 3 ticket in ServiceNow under "Medical Devices > Infusion Pump General Failure."
    3.  Clean the unit and send it to Biomedical Engineering via the designated utility room bin.

*   **Specific Case: Alaris Infusion Pump Error Code 525**
    *   **Problem:** Error code 525 on an Alaris infusion pump indicates a critical channel communication failure. The device must be removed from service immediately as it poses a significant risk of medication delivery error.
    *   **Reporting and Replacement:** The attending nurse or clinical staff must **file a Level 2 ticket in the ServiceNow portal under the category "Medical Devices > Infusion Pump Failure."** In the ticket, specify the device model (Alaris), the unique asset tag number, and the error code (525). This ensures proper tracking and priority.
    *   **Contact Person:** For an immediate replacement unit, **contact the Central Supply department** at extension 4450. They will dispatch a ready-for-use unit to your floor. Do NOT contact Biomedical Engineering for an immediate replacement; their role is repair, not immediate dispatch.
    *   **Handling the Faulty Unit:** After filing the ticket and securing a replacement, the faulty Alaris pump should be cleaned according to standard sanitation procedures and **sent to the Biomedical Engineering department.** Place the tagged unit in the designated "Biomedical Outgoing" bin, which is typically located in the floor's main utility room next to the clean supply closet.

#### **5.3. Procedure for Diagnostic Imaging Equipment**
For any fault with fixed imaging equipment like an MRI or CT scanner, an immediate Level 1 "Critical System Down" ticket must be filed in ServiceNow. This action automatically pages the on-call Radiology technician and the Biomedical Engineering imaging specialist. Do not attempt to reset the system.

#### **5.4. Procedure for Patient Monitoring Systems**
This section outlines a similar process to infusion pumps, differentiating between central station failures (critical, Level 1 ticket) and individual bedside monitor issues (high priority, Level 2 ticket).

#### **5.5. Procedure for Surgical Equipment**
Any fault discovered during pre-op checks requires an immediate verbal report to the lead surgeon and OR nurse manager, in addition to a Level 2 ServiceNow ticket. The device must be replaced, and the fault must be documented in the surgical safety checklist records.

---
### **6. Decommissioning and Disposal**

#### **6.1. End-of-Life (EOL) Assessment Criteria**
Equipment is flagged for EOL assessment based on several factors: age (exceeding OEM-recommended service life), frequency of repairs, unavailability of replacement parts, or if it no longer meets current clinical standards. The Biomedical Engineering department head makes the final determination.

#### **6.2. Data Sanitization and Removal (HIPAA Compliance)**
Before any device with data storage capabilities is disposed of, it must undergo a rigorous data sanitization process. All patient health information (PHI) must be permanently destroyed. This involves either cryptographic erasure or physical destruction of the storage media, compliant with HIPAA Security Rule standards. A certificate of data destruction must be logged in the asset's record.

#### **6.3. Safe Disposal and Recycling Procedures**
Pavilion Hospital is committed to environmentally responsible disposal. All electronic equipment must be disposed of through a certified e-waste recycling vendor. Devices containing hazardous materials must be handled according to federal and state environmental regulations. The Asset Management team coordinates with the approved vendor for pickup and disposal.

---
### **7. Appendix**

#### **7.1. Contact List**
*   Head of Biomedical Engineering: Dr. Anya Sharma, x5100
*   Director of Central Supply: Mr. Kenji Tanaka, x4400
*   On-Call Biomed Pager (Critical Failures Only): 555-100-PAGE
*   ServiceNow Help Desk: xHELP (x4357)

#### **7.2. Form: PH-FORM-INC-001 - Equipment Incident Report**
*(A placeholder for a detailed form including fields for patient information (if involved), device details, description of event, immediate actions taken, and staff signatures.)*

#### **7.3. Escalation Matrix for Critical Failures**
*   **Level 1 (System Down):** Auto-page to on-call specialist, Director of Nursing, and Hospital Administrator.
*   **Level 2 (High Priority):** Auto-notification to Department Head and relevant service manager.
*   **Level 3 (Medium Priority):** Standard notification to service queue.
*   **Level 4 (Low Priority):** General service queue.

