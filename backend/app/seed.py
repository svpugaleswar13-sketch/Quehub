"""Populate the database with 20 demo organizations, services, 25 customers, and some active bookings.

Run with:  python -m app.seed
"""
from datetime import time, date, datetime
from app.database import Base, engine, SessionLocal
from app import models
from app.security import hash_password

Base.metadata.create_all(bind=engine)


def run():
    db = SessionLocal()
    try:
        print("Clearing existing data...")
        db.query(models.Notification).delete()
        db.query(models.Booking).delete()
        db.query(models.Token).delete()
        db.query(models.Service).delete()
        db.query(models.Organization).delete()
        db.query(models.User).delete()
        db.commit()
        print("Existing data cleared.")

        # =========================
        # ORGANIZATIONS DATA
        # =========================
        orgs_data = [
            # 1
            {
                "admin_name": "Dr. Rajesh Kumar",
                "email": "apollo@queuehub.demo",
                "password": "password123",
                "org_name": "Apollo Multi Speciality Hospital",
                "domain": "Hospital",
                "address": "21, Greams Road, Chennai",
                "working_hours": "Mon-Sat, 8:00 AM - 8:00 PM",
                "services": [
                    {"name": "General Physician Consultation", "start": time(8, 0), "end": time(20, 0), "max": 50, "avg": 15},
                    {"name": "Cardiology Consultation", "start": time(8, 0), "end": time(20, 0), "max": 40, "avg": 20},
                    {"name": "Orthopedic Consultation", "start": time(8, 0), "end": time(20, 0), "max": 40, "avg": 15},
                    {"name": "Pediatrics", "start": time(8, 0), "end": time(20, 0), "max": 50, "avg": 10},
                    {"name": "Dermatology", "start": time(8, 0), "end": time(20, 0), "max": 30, "avg": 15},
                    {"name": "Blood Test", "start": time(8, 0), "end": time(20, 0), "max": 100, "avg": 5},
                    {"name": "X-Ray", "start": time(8, 0), "end": time(20, 0), "max": 60, "avg": 10},
                    {"name": "MRI Scan", "start": time(8, 0), "end": time(20, 0), "max": 20, "avg": 30},
                    {"name": "Vaccination", "start": time(8, 0), "end": time(20, 0), "max": 80, "avg": 5},
                    {"name": "Health Check-up", "start": time(8, 0), "end": time(20, 0), "max": 30, "avg": 20},
                ]
            },
            # 2
            {
                "admin_name": "Ananya Sharma",
                "email": "sbi@queuehub.demo",
                "password": "password123",
                "org_name": "State Bank of India - Anna Nagar Branch",
                "domain": "Bank",
                "address": "45, Anna Nagar West, Chennai",
                "working_hours": "Mon-Fri, 9:00 AM - 4:00 PM",
                "services": [
                    {"name": "Cash Deposit", "start": time(9, 0), "end": time(16, 0), "max": 100, "avg": 8},
                    {"name": "Cash Withdrawal", "start": time(9, 0), "end": time(16, 0), "max": 100, "avg": 5},
                    {"name": "Account Opening", "start": time(9, 0), "end": time(16, 0), "max": 30, "avg": 20},
                    {"name": "Passbook Update", "start": time(9, 0), "end": time(16, 0), "max": 150, "avg": 3},
                    {"name": "Cheque Deposit", "start": time(9, 0), "end": time(16, 0), "max": 80, "avg": 5},
                    {"name": "Demand Draft", "start": time(9, 0), "end": time(16, 0), "max": 40, "avg": 10},
                    {"name": "Loan Enquiry", "start": time(9, 0), "end": time(16, 0), "max": 30, "avg": 15},
                    {"name": "Fixed Deposit", "start": time(9, 0), "end": time(16, 0), "max": 40, "avg": 12},
                    {"name": "KYC Update", "start": time(9, 0), "end": time(16, 0), "max": 60, "avg": 10},
                    {"name": "Debit Card Services", "start": time(9, 0), "end": time(16, 0), "max": 50, "avg": 8},
                ]
            },
            # 3
            {
                "admin_name": "Vivek Menon",
                "email": "rto@queuehub.demo",
                "password": "password123",
                "org_name": "Chennai Regional Transport Office",
                "domain": "Government",
                "address": "18, Guindy Industrial Estate, Chennai",
                "working_hours": "Mon-Fri, 10:00 AM - 5:00 PM",
                "services": [
                    {"name": "Driving License Test", "start": time(10, 0), "end": time(17, 0), "max": 50, "avg": 20},
                    {"name": "Learner's License", "start": time(10, 0), "end": time(17, 0), "max": 100, "avg": 10},
                    {"name": "Driving License Renewal", "start": time(10, 0), "end": time(17, 0), "max": 80, "avg": 12},
                    {"name": "Vehicle Registration", "start": time(10, 0), "end": time(17, 0), "max": 60, "avg": 15},
                    {"name": "Transfer of Ownership", "start": time(10, 0), "end": time(17, 0), "max": 45, "avg": 15},
                    {"name": "Duplicate RC", "start": time(10, 0), "end": time(17, 0), "max": 40, "avg": 10},
                    {"name": "Road Tax Payment", "start": time(10, 0), "end": time(17, 0), "max": 120, "avg": 5},
                    {"name": "NOC Certificate", "start": time(10, 0), "end": time(17, 0), "max": 50, "avg": 10},
                    {"name": "Address Change", "start": time(10, 0), "end": time(17, 0), "max": 60, "avg": 12},
                    {"name": "Vehicle Fitness Certificate", "start": time(10, 0), "end": time(17, 0), "max": 40, "avg": 20},
                ]
            },
            # 4
            {
                "admin_name": "Priya Nair",
                "email": "srm@queuehub.demo",
                "password": "password123",
                "org_name": "SRM Student Services",
                "domain": "Education",
                "address": "SRM IST, Ramapuram, Chennai",
                "working_hours": "Mon-Sat, 9:00 AM - 5:00 PM",
                "services": [
                    {"name": "Fee Payment", "start": time(9, 0), "end": time(17, 0), "max": 150, "avg": 5},
                    {"name": "Bonafide Certificate", "start": time(9, 0), "end": time(17, 0), "max": 80, "avg": 8},
                    {"name": "ID Card Issue", "start": time(9, 0), "end": time(17, 0), "max": 60, "avg": 10},
                    {"name": "Transcript Request", "start": time(9, 0), "end": time(17, 0), "max": 40, "avg": 15},
                    {"name": "Exam Registration", "start": time(9, 0), "end": time(17, 0), "max": 100, "avg": 8},
                    {"name": "Course Registration", "start": time(9, 0), "end": time(17, 0), "max": 120, "avg": 10},
                    {"name": "Scholarship Enquiry", "start": time(9, 0), "end": time(17, 0), "max": 50, "avg": 15},
                    {"name": "Hostel Services", "start": time(9, 0), "end": time(17, 0), "max": 70, "avg": 12},
                    {"name": "Placement Office", "start": time(9, 0), "end": time(17, 0), "max": 55, "avg": 15},
                    {"name": "Academic Counselling", "start": time(9, 0), "end": time(17, 0), "max": 30, "avg": 20},
                ]
            },
            # 5
            {
                "admin_name": "Arjun Patel",
                "email": "salon@queuehub.demo",
                "password": "password123",
                "org_name": "Green Leaf Salon & Spa",
                "domain": "Salon",
                "address": "12, Velachery Main Road, Chennai",
                "working_hours": "Daily, 10:00 AM - 9:00 PM",
                "services": [
                    {"name": "Haircut", "start": time(10, 0), "end": time(21, 0), "max": 40, "avg": 25},
                    {"name": "Hair Spa", "start": time(10, 0), "end": time(21, 0), "max": 20, "avg": 45},
                    {"name": "Hair Coloring", "start": time(10, 0), "end": time(21, 0), "max": 15, "avg": 60},
                    {"name": "Beard Grooming", "start": time(10, 0), "end": time(21, 0), "max": 35, "avg": 15},
                    {"name": "Facial", "start": time(10, 0), "end": time(21, 0), "max": 25, "avg": 40},
                    {"name": "Cleanup", "start": time(10, 0), "end": time(21, 0), "max": 30, "avg": 20},
                    {"name": "Manicure", "start": time(10, 0), "end": time(21, 0), "max": 20, "avg": 30},
                    {"name": "Pedicure", "start": time(10, 0), "end": time(21, 0), "max": 20, "avg": 35},
                    {"name": "Head Massage", "start": time(10, 0), "end": time(21, 0), "max": 40, "avg": 15},
                    {"name": "Bridal Grooming", "start": time(10, 0), "end": time(21, 0), "max": 5, "avg": 120},
                ]
            },
            # 6
            {
                "admin_name": "Lakshmi Narayanan",
                "email": "hdfc@queuehub.demo",
                "password": "password123",
                "org_name": "HDFC Bank - Porur Branch",
                "domain": "Bank",
                "address": "Porur, Chennai",
                "working_hours": "Mon-Fri, 9:30 AM - 4:30 PM",
                "services": [
                    {"name": "Account Opening", "start": time(9, 30), "end": time(16, 30), "max": 40, "avg": 20},
                    {"name": "Cash Deposit", "start": time(9, 30), "end": time(16, 30), "max": 100, "avg": 8},
                    {"name": "Cash Withdrawal", "start": time(9, 30), "end": time(16, 30), "max": 100, "avg": 5},
                    {"name": "Loan Enquiry", "start": time(9, 30), "end": time(16, 30), "max": 30, "avg": 15},
                    {"name": "Credit Card Services", "start": time(9, 30), "end": time(16, 30), "max": 50, "avg": 10},
                    {"name": "KYC Update", "start": time(9, 30), "end": time(16, 30), "max": 60, "avg": 10},
                    {"name": "Fixed Deposit", "start": time(9, 30), "end": time(16, 30), "max": 45, "avg": 12},
                    {"name": "Passbook Update", "start": time(9, 30), "end": time(16, 30), "max": 120, "avg": 3},
                ]
            },
            # 7
            {
                "admin_name": "Dr. Sneha Reddy",
                "email": "dental@queuehub.demo",
                "password": "password123",
                "org_name": "Smile Care Dental Clinic",
                "domain": "Hospital",
                "address": "Velachery, Chennai",
                "working_hours": "Mon-Sat, 9:00 AM - 8:00 PM",
                "services": [
                    {"name": "Dental Check-up", "start": time(9, 0), "end": time(20, 0), "max": 40, "avg": 15},
                    {"name": "Root Canal Treatment", "start": time(9, 0), "end": time(20, 0), "max": 15, "avg": 45},
                    {"name": "Teeth Cleaning", "start": time(9, 0), "end": time(20, 0), "max": 30, "avg": 20},
                    {"name": "Teeth Whitening", "start": time(9, 0), "end": time(20, 0), "max": 20, "avg": 30},
                    {"name": "Braces Consultation", "start": time(9, 0), "end": time(20, 0), "max": 25, "avg": 15},
                    {"name": "Tooth Extraction", "start": time(9, 0), "end": time(20, 0), "max": 15, "avg": 30},
                    {"name": "Dental Filling", "start": time(9, 0), "end": time(20, 0), "max": 20, "avg": 25},
                ]
            },
            # 8
            {
                "admin_name": "Prakash Kumar",
                "email": "passport@queuehub.demo",
                "password": "password123",
                "org_name": "Regional Passport Seva Kendra",
                "domain": "Government",
                "address": "Saligramam, Chennai",
                "working_hours": "Mon-Fri, 9:30 AM - 5:00 PM",
                "services": [
                    {"name": "New Passport", "start": time(9, 30), "end": time(17, 0), "max": 60, "avg": 20},
                    {"name": "Passport Renewal", "start": time(9, 30), "end": time(17, 0), "max": 80, "avg": 15},
                    {"name": "Police Verification", "start": time(9, 30), "end": time(17, 0), "max": 100, "avg": 10},
                    {"name": "Document Verification", "start": time(9, 30), "end": time(17, 0), "max": 120, "avg": 10},
                    {"name": "Tatkal Passport", "start": time(9, 30), "end": time(17, 0), "max": 30, "avg": 20},
                    {"name": "Passport Status Enquiry", "start": time(9, 30), "end": time(17, 0), "max": 150, "avg": 5},
                ]
            },
            # 9
            {
                "admin_name": "Kavitha Iyer",
                "email": "college@queuehub.demo",
                "password": "password123",
                "org_name": "Loyola College Student Office",
                "domain": "Education",
                "address": "Nungambakkam, Chennai",
                "working_hours": "Mon-Sat, 9:00 AM - 4:30 PM",
                "services": [
                    {"name": "Admission Enquiry", "start": time(9, 0), "end": time(16, 30), "max": 80, "avg": 12},
                    {"name": "Fee Payment", "start": time(9, 0), "end": time(16, 30), "max": 150, "avg": 5},
                    {"name": "Hall Ticket Issue", "start": time(9, 0), "end": time(16, 30), "max": 100, "avg": 8},
                    {"name": "Certificate Request", "start": time(9, 0), "end": time(16, 30), "max": 60, "avg": 15},
                    {"name": "Scholarship Support", "start": time(9, 0), "end": time(16, 30), "max": 50, "avg": 15},
                    {"name": "Student Counselling", "start": time(9, 0), "end": time(16, 30), "max": 30, "avg": 20},
                ]
            },
            # 10
            {
                "admin_name": "Mohammed Arif",
                "email": "barber@queuehub.demo",
                "password": "password123",
                "org_name": "Royal Men's Salon",
                "domain": "Salon",
                "address": "Tambaram, Chennai",
                "working_hours": "Daily, 10:00 AM - 9:30 PM",
                "services": [
                    {"name": "Haircut", "start": time(10, 0), "end": time(21, 30), "max": 40, "avg": 20},
                    {"name": "Hair Wash", "start": time(10, 0), "end": time(21, 30), "max": 30, "avg": 10},
                    {"name": "Beard Trim", "start": time(10, 0), "end": time(21, 30), "max": 40, "avg": 15},
                    {"name": "Hair Styling", "start": time(10, 0), "end": time(21, 30), "max": 20, "avg": 15},
                    {"name": "Hair Spa", "start": time(10, 0), "end": time(21, 30), "max": 15, "avg": 40},
                    {"name": "Face Cleanup", "start": time(10, 0), "end": time(21, 30), "max": 25, "avg": 25},
                ]
            },
            # 11
            {
                "admin_name": "Nisha Thomas",
                "email": "eyecare@queuehub.demo",
                "password": "password123",
                "org_name": "Vision Eye Care Centre",
                "domain": "Hospital",
                "address": "Anna Nagar, Chennai",
                "working_hours": "Mon-Sat, 8:30 AM - 7:00 PM",
                "services": [
                    {"name": "Eye Check-up", "start": time(8, 30), "end": time(19, 0), "max": 50, "avg": 15},
                    {"name": "Cataract Consultation", "start": time(8, 30), "end": time(19, 0), "max": 20, "avg": 20},
                    {"name": "LASIK Consultation", "start": time(8, 30), "end": time(19, 0), "max": 15, "avg": 20},
                    {"name": "Vision Test", "start": time(8, 30), "end": time(19, 0), "max": 80, "avg": 10},
                    {"name": "Optical Services", "start": time(8, 30), "end": time(19, 0), "max": 60, "avg": 10},
                    {"name": "Retina Examination", "start": time(8, 30), "end": time(19, 0), "max": 20, "avg": 30},
                ]
            },
            # 12
            {
                "admin_name": "Ramesh Babu",
                "email": "indianbank@queuehub.demo",
                "password": "password123",
                "org_name": "Indian Bank - Chromepet Branch",
                "domain": "Bank",
                "address": "Chromepet, Chennai",
                "working_hours": "Mon-Fri, 10:00 AM - 4:00 PM",
                "services": [
                    {"name": "Cash Services", "start": time(10, 0), "end": time(16, 0), "max": 120, "avg": 6},
                    {"name": "Account Opening", "start": time(10, 0), "end": time(16, 0), "max": 30, "avg": 20},
                    {"name": "Loan Services", "start": time(10, 0), "end": time(16, 0), "max": 40, "avg": 15},
                    {"name": "Gold Loan", "start": time(10, 0), "end": time(16, 0), "max": 50, "avg": 15},
                    {"name": "Demand Draft", "start": time(10, 0), "end": time(16, 0), "max": 45, "avg": 10},
                    {"name": "ATM Card Issue", "start": time(10, 0), "end": time(16, 0), "max": 60, "avg": 8},
                ]
            },
            # 13
            {
                "admin_name": "Harini Subramanian",
                "email": "corporation@queuehub.demo",
                "password": "password123",
                "org_name": "Greater Chennai Corporation Office",
                "domain": "Government",
                "address": "Teynampet, Chennai",
                "working_hours": "Mon-Fri, 10:00 AM - 5:30 PM",
                "services": [
                    {"name": "Birth Certificate", "start": time(10, 0), "end": time(17, 30), "max": 100, "avg": 10},
                    {"name": "Death Certificate", "start": time(10, 0), "end": time(17, 30), "max": 80, "avg": 10},
                    {"name": "Property Tax", "start": time(10, 0), "end": time(17, 30), "max": 120, "avg": 8},
                    {"name": "Water Tax", "start": time(10, 0), "end": time(17, 30), "max": 100, "avg": 8},
                    {"name": "Trade License", "start": time(10, 0), "end": time(17, 30), "max": 40, "avg": 20},
                    {"name": "Public Grievance", "start": time(10, 0), "end": time(17, 30), "max": 60, "avg": 15},
                ]
            },
            # 14
            {
                "admin_name": "Suresh Kumar",
                "email": "library@queuehub.demo",
                "password": "password123",
                "org_name": "Chennai Central Public Library",
                "domain": "Education",
                "address": "Egmore, Chennai",
                "working_hours": "Mon-Sat, 9:00 AM - 6:00 PM",
                "services": [
                    {"name": "Membership Registration", "start": time(9, 0), "end": time(18, 0), "max": 50, "avg": 10},
                    {"name": "Book Borrowing", "start": time(9, 0), "end": time(18, 0), "max": 150, "avg": 4},
                    {"name": "Book Return", "start": time(9, 0), "end": time(18, 0), "max": 200, "avg": 3},
                    {"name": "Digital Library Access", "start": time(9, 0), "end": time(18, 0), "max": 40, "avg": 5},
                    {"name": "Study Hall Booking", "start": time(9, 0), "end": time(18, 0), "max": 60, "avg": 5},
                    {"name": "Reference Section", "start": time(9, 0), "end": time(18, 0), "max": 30, "avg": 10},
                ]
            },
            # 15
            {
                "admin_name": "Aishwarya Menon",
                "email": "luxurysalon@queuehub.demo",
                "password": "password123",
                "org_name": "Luxury Beauty Lounge",
                "domain": "Salon",
                "address": "Adyar, Chennai",
                "working_hours": "Daily, 9:00 AM - 8:30 PM",
                "services": [
                    {"name": "Haircut", "start": time(9, 0), "end": time(20, 30), "max": 30, "avg": 25},
                    {"name": "Hair Coloring", "start": time(9, 0), "end": time(20, 30), "max": 12, "avg": 60},
                    {"name": "Hair Smoothening", "start": time(9, 0), "end": time(20, 30), "max": 6, "avg": 120},
                    {"name": "Facial", "start": time(9, 0), "end": time(20, 30), "max": 20, "avg": 45},
                    {"name": "Waxing", "start": time(9, 0), "end": time(20, 30), "max": 25, "avg": 30},
                    {"name": "Bridal Makeup", "start": time(9, 0), "end": time(20, 30), "max": 4, "avg": 90},
                    {"name": "Spa Therapy", "start": time(9, 0), "end": time(20, 30), "max": 15, "avg": 50},
                ]
            },
            # 16
            {
                "admin_name": "Dr. Vinod Kumar",
                "email": "ortho@queuehub.demo",
                "password": "password123",
                "org_name": "Ortho Plus Clinic",
                "domain": "Hospital",
                "address": "Mogappair, Chennai",
                "working_hours": "Mon-Sat, 9:00 AM - 7:00 PM",
                "services": [
                    {"name": "Bone Consultation", "start": time(9, 0), "end": time(19, 0), "max": 40, "avg": 15},
                    {"name": "Fracture Review", "start": time(9, 0), "end": time(19, 0), "max": 25, "avg": 20},
                    {"name": "Physiotherapy", "start": time(9, 0), "end": time(19, 0), "max": 30, "avg": 30},
                    {"name": "Joint Pain Consultation", "start": time(9, 0), "end": time(19, 0), "max": 35, "avg": 15},
                    {"name": "X-Ray", "start": time(9, 0), "end": time(19, 0), "max": 60, "avg": 10},
                    {"name": "Follow-up Visit", "start": time(9, 0), "end": time(19, 0), "max": 50, "avg": 10},
                ]
            },
            # 17
            {
                "admin_name": "Preethi Raman",
                "email": "canara@queuehub.demo",
                "password": "password123",
                "org_name": "Canara Bank - T Nagar Branch",
                "domain": "Bank",
                "address": "T Nagar, Chennai",
                "working_hours": "Mon-Fri, 9:30 AM - 4:30 PM",
                "services": [
                    {"name": "Savings Account", "start": time(9, 30), "end": time(16, 30), "max": 50, "avg": 15},
                    {"name": "Current Account", "start": time(9, 30), "end": time(16, 30), "max": 30, "avg": 15},
                    {"name": "Cash Deposit", "start": time(9, 30), "end": time(16, 30), "max": 100, "avg": 8},
                    {"name": "Cash Withdrawal", "start": time(9, 30), "end": time(16, 30), "max": 100, "avg": 5},
                    {"name": "Loan Enquiry", "start": time(9, 30), "end": time(16, 30), "max": 40, "avg": 15},
                    {"name": "Locker Services", "start": time(9, 30), "end": time(16, 30), "max": 20, "avg": 15},
                ]
            },
            # 18
            {
                "admin_name": "Ashok Raj",
                "email": "eb@queuehub.demo",
                "password": "password123",
                "org_name": "TANGEDCO Electricity Office",
                "domain": "Government",
                "address": "Ashok Nagar, Chennai",
                "working_hours": "Mon-Fri, 9:30 AM - 5:30 PM",
                "services": [
                    {"name": "New Electricity Connection", "start": time(9, 30), "end": time(17, 30), "max": 40, "avg": 20},
                    {"name": "Bill Payment", "start": time(9, 30), "end": time(17, 30), "max": 200, "avg": 4},
                    {"name": "Name Transfer", "start": time(9, 30), "end": time(17, 30), "max": 30, "avg": 25},
                    {"name": "Meter Complaint", "start": time(9, 30), "end": time(17, 30), "max": 50, "avg": 15},
                    {"name": "Load Enhancement", "start": time(9, 30), "end": time(17, 30), "max": 30, "avg": 20},
                    {"name": "Service Request", "start": time(9, 30), "end": time(17, 30), "max": 80, "avg": 10},
                ]
            },
            # 19
            {
                "admin_name": "Revathi Srinivasan",
                "email": "university@queuehub.demo",
                "password": "password123",
                "org_name": "Anna University Student Services",
                "domain": "Education",
                "address": "Guindy, Chennai",
                "working_hours": "Mon-Sat, 9:00 AM - 5:00 PM",
                "services": [
                    {"name": "Transcript Request", "start": time(9, 0), "end": time(17, 0), "max": 50, "avg": 15},
                    {"name": "Degree Certificate", "start": time(9, 0), "end": time(17, 0), "max": 40, "avg": 20},
                    {"name": "Exam Registration", "start": time(9, 0), "end": time(17, 0), "max": 150, "avg": 8},
                    {"name": "Migration Certificate", "start": time(9, 0), "end": time(17, 0), "max": 60, "avg": 12},
                    {"name": "Student Support", "start": time(9, 0), "end": time(17, 0), "max": 100, "avg": 10},
                    {"name": "Academic Verification", "start": time(9, 0), "end": time(17, 0), "max": 50, "avg": 15},
                ]
            },
            # 20
            {
                "admin_name": "Joseph Daniel",
                "email": "elite@queuehub.demo",
                "password": "password123",
                "org_name": "Elite Unisex Salon",
                "domain": "Salon",
                "address": "OMR, Chennai",
                "working_hours": "Daily, 10:00 AM - 9:00 PM",
                "services": [
                    {"name": "Haircut", "start": time(10, 0), "end": time(21, 0), "max": 40, "avg": 25},
                    {"name": "Hair Spa", "start": time(10, 0), "end": time(21, 0), "max": 20, "avg": 45},
                    {"name": "Keratin Treatment", "start": time(10, 0), "end": time(21, 0), "max": 10, "avg": 90},
                    {"name": "Facial", "start": time(10, 0), "end": time(21, 0), "max": 25, "avg": 40},
                    {"name": "Beard Grooming", "start": time(10, 0), "end": time(21, 0), "max": 35, "avg": 15},
                    {"name": "Manicure", "start": time(10, 0), "end": time(21, 0), "max": 20, "avg": 30},
                    {"name": "Pedicure", "start": time(10, 0), "end": time(21, 0), "max": 20, "avg": 35},
                    {"name": "Makeup", "start": time(10, 0), "end": time(21, 0), "max": 10, "avg": 60},
                ]
            }
        ]

        # Dictionary to store created service models mapped by (org_email, service_name)
        services_dict = {}

        for o in orgs_data:
            user = models.User(
                name=o["admin_name"],
                email=o["email"],
                password_hash=hash_password(o["password"]),
                role=models.UserRole.organization,
            )
            db.add(user)
            db.flush()

            org = models.Organization(
                owner_id=user.id,
                name=o["org_name"],
                domain=o["domain"],
                address=o["address"],
                working_hours=o["working_hours"],
                rating=4.5
            )
            db.add(org)
            db.flush()

            for s in o["services"]:
                svc = models.Service(
                    organization_id=org.id,
                    name=s["name"],
                    start_time=s["start"],
                    end_time=s["end"],
                    max_tokens=s["max"],
                    average_service_time=s["avg"]
                )
                db.add(svc)
                db.flush()
                services_dict[(o["email"], s["name"])] = svc

        # =========================
        # CUSTOMERS DATA
        # =========================
        customers_data = [
            {"name": "Karthik Raj", "email": "karthik@queuehub.demo", "password": "password123"},
            {"name": "Divya Shree", "email": "divya@queuehub.demo", "password": "password123"},
            {"name": "Rahul Krishna", "email": "rahul@queuehub.demo", "password": "password123"},
            {"name": "Meena Lakshmi", "email": "meena@queuehub.demo", "password": "password123"},
            {"name": "Sanjay Kumar", "email": "sanjay@queuehub.demo", "password": "password123"},
            {"name": "Ajay Kumar", "email": "ajay@queuehub.demo", "password": "password123"},
            {"name": "Nithya Ramesh", "email": "nithya@queuehub.demo", "password": "password123"},
            {"name": "Vignesh Prabhu", "email": "vignesh@queuehub.demo", "password": "password123"},
            {"name": "Keerthana S", "email": "keerthana@queuehub.demo", "password": "password123"},
            {"name": "Arun Prakash", "email": "arun@queuehub.demo", "password": "password123"},
            {"name": "Harish Kumar", "email": "harish@queuehub.demo", "password": "password123"},
            {"name": "Priyanka Nair", "email": "priyanka@queuehub.demo", "password": "password123"},
            {"name": "Kavin Raj", "email": "kavin@queuehub.demo", "password": "password123"},
            {"name": "Sneha Iyer", "email": "sneha@queuehub.demo", "password": "password123"},
            {"name": "Rohit Sharma", "email": "rohit@queuehub.demo", "password": "password123"},
            {"name": "Meera Krishnan", "email": "meera@queuehub.demo", "password": "password123"},
            {"name": "Dinesh Kumar", "email": "dinesh@queuehub.demo", "password": "password123"},
            {"name": "Pooja Menon", "email": "pooja@queuehub.demo", "password": "password123"},
            {"name": "Bharath R", "email": "bharath@queuehub.demo", "password": "password123"},
            {"name": "Akshaya Devi", "email": "akshaya@queuehub.demo", "password": "password123"},
            {"name": "Surya Narayanan", "email": "surya@queuehub.demo", "password": "password123"},
            {"name": "Janani K", "email": "janani@queuehub.demo", "password": "password123"},
            {"name": "Naveen Raj", "email": "naveen@queuehub.demo", "password": "password123"},
            {"name": "Aarthi Balaji", "email": "aarthi@queuehub.demo", "password": "password123"},
            {"name": "Gokul Krishna", "email": "gokul@queuehub.demo", "password": "password123"},
        ]

        # Dictionary to store created customer models mapped by email
        customers_dict = {}

        for c in customers_data:
            customer = models.User(
                name=c["name"],
                email=c["email"],
                password_hash=hash_password(c["password"]),
                role=models.UserRole.customer,
            )
            db.add(customer)
            db.flush()
            customers_dict[c["email"]] = customer

        # =========================
        # SEED BOOKINGS/TOKENS DATA
        # =========================
        today = date.today()
        
        # Helper to book a token
        def create_token_booking(org_email, service_name, token_number, customer_email, token_status):
            svc = services_dict[(org_email, service_name)]
            cust = customers_dict[customer_email]
            
            token = models.Token(
                service_id=svc.id,
                date=today,
                token_number=token_number,
                customer_id=cust.id,
                customer_name=cust.name,
                status=token_status,
                is_walk_in=False,
                booking_time=datetime.utcnow()
            )
            db.add(token)
            db.flush()
            
            booking_status = models.BookingStatus.waiting
            if token_status == models.TokenStatus.completed:
                booking_status = models.BookingStatus.completed
            elif token_status == models.TokenStatus.cancelled:
                booking_status = models.BookingStatus.cancelled
                
            booking = models.Booking(
                customer_id=cust.id,
                token_id=token.id,
                estimated_time=datetime.utcnow(),
                status=booking_status
            )
            db.add(booking)
            
            notification = models.Notification(
                customer_id=cust.id,
                message=f"Token {token_number} booked for {svc.name}. Status: {token_status.value}.",
            )
            db.add(notification)

        print("Seeding demo bookings...")

        # Organization 1: Apollo Hospital -> General Physician Consultation
        create_token_booking("apollo@queuehub.demo", "General Physician Consultation", 1, "karthik@queuehub.demo", models.TokenStatus.completed)
        create_token_booking("apollo@queuehub.demo", "General Physician Consultation", 2, "divya@queuehub.demo", models.TokenStatus.serving)
        create_token_booking("apollo@queuehub.demo", "General Physician Consultation", 3, "ajay@queuehub.demo", models.TokenStatus.waiting)
        create_token_booking("apollo@queuehub.demo", "General Physician Consultation", 4, "nithya@queuehub.demo", models.TokenStatus.waiting)
        create_token_booking("apollo@queuehub.demo", "General Physician Consultation", 5, "vignesh@queuehub.demo", models.TokenStatus.waiting)

        # Organization 1: Apollo Hospital -> Pediatrics
        create_token_booking("apollo@queuehub.demo", "Pediatrics", 1, "keerthana@queuehub.demo", models.TokenStatus.serving)
        create_token_booking("apollo@queuehub.demo", "Pediatrics", 2, "arun@queuehub.demo", models.TokenStatus.waiting)

        # Organization 2: SBI Bank -> Cash Deposit
        create_token_booking("sbi@queuehub.demo", "Cash Deposit", 1, "harish@queuehub.demo", models.TokenStatus.completed)
        create_token_booking("sbi@queuehub.demo", "Cash Deposit", 2, "priyanka@queuehub.demo", models.TokenStatus.completed)
        create_token_booking("sbi@queuehub.demo", "Cash Deposit", 3, "kavin@queuehub.demo", models.TokenStatus.serving)
        create_token_booking("sbi@queuehub.demo", "Cash Deposit", 4, "sneha@queuehub.demo", models.TokenStatus.waiting)
        create_token_booking("sbi@queuehub.demo", "Cash Deposit", 5, "rohit@queuehub.demo", models.TokenStatus.waiting)

        # Organization 3: RTO Chennai -> Driving License Test
        create_token_booking("rto@queuehub.demo", "Driving License Test", 1, "meera@queuehub.demo", models.TokenStatus.serving)
        create_token_booking("rto@queuehub.demo", "Driving License Test", 2, "dinesh@queuehub.demo", models.TokenStatus.waiting)

        # Organization 5: Green Leaf Salon -> Haircut
        create_token_booking("salon@queuehub.demo", "Haircut", 1, "pooja@queuehub.demo", models.TokenStatus.serving)
        create_token_booking("salon@queuehub.demo", "Haircut", 2, "bharath@queuehub.demo", models.TokenStatus.waiting)

        # Organization 6: HDFC Bank -> Account Opening
        create_token_booking("hdfc@queuehub.demo", "Account Opening", 1, "akshaya@queuehub.demo", models.TokenStatus.serving)
        create_token_booking("hdfc@queuehub.demo", "Account Opening", 2, "surya@queuehub.demo", models.TokenStatus.waiting)

        # Organization 7: Smile Care Dental Clinic -> Teeth Cleaning
        create_token_booking("dental@queuehub.demo", "Teeth Cleaning", 1, "janani@queuehub.demo", models.TokenStatus.serving)
        create_token_booking("dental@queuehub.demo", "Teeth Cleaning", 2, "naveen@queuehub.demo", models.TokenStatus.waiting)
        create_token_booking("dental@queuehub.demo", "Teeth Cleaning", 3, "aarthi@queuehub.demo", models.TokenStatus.waiting)
        create_token_booking("dental@queuehub.demo", "Teeth Cleaning", 4, "gokul@queuehub.demo", models.TokenStatus.waiting)

        db.commit()
        print("Database successfully seeded with all 20 demo organizations, 25 customers, and active bookings!")

    finally:
        db.close()


if __name__ == "__main__":
    run()
