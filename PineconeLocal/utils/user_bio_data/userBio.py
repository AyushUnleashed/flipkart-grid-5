class UserBioData:
    def __init__(self, name, age, gender, city, email, phone):
        self.name = name
        self.age = age
        self.gender = gender
        self.city = city
        self.email = email
        self.phone = phone

# Example usage
gwen_bio_data = UserBioData(name="gwen", age=23, gender="women", city="Mumbai", email="gwen23@xyz.com", phone="592-703-184")
john_bio_data = UserBioData(name="john", age=25, gender="men", city="Delhi", email="jhon25@abc.com", phone="286-490-137")
sneha_bio_data = UserBioData(name="Sneha", age=20, gender="women", city="Mumbai", email="sneha@example.com", phone="555-555-001")
rahul_bio_data = UserBioData(name="Rahul", age=25, gender="men", city="Delhi", email="rahul@example.com", phone="555-555-002")
neha_bio_data = UserBioData(name="Neha", age=30, gender="women", city="Bangalore", email="neha@example.com", phone="555-555-003")
amit_bio_data = UserBioData(name="Amit", age=35, gender="men", city="Chennai", email="amit@example.com", phone="555-555-004")
priya_bio_data = UserBioData(name="Priya", age=40, gender="women", city="Kolkata", email="priya@example.com", phone="555-555-005")
vikram_bio_data = UserBioData(name="Vikram", age=45, gender="men", city="Hyderabad", email="vikram@example.com", phone="555-555-006")
sapna_bio_data = UserBioData(name="Sapna", age=50, gender="women", city="Pune", email="sapna@example.com", phone="555-555-007")
rajesh_bio_data = UserBioData(name="Rajesh", age=55, gender="men", city="Ahmedabad", email="rajesh@example.com", phone="555-555-008")
kavita_bio_data = UserBioData(name="Kavita", age=60, gender="women", city="Jaipur", email="kavita@example.com", phone="555-555-009")
alok_bio_data = UserBioData(name="Alok", age=65, gender="men", city="Lucknow", email="alok@example.com", phone="555-555-010")

current_user_bio_data = gwen_bio_data
# if __name__ == "__main__":
    # print(f"{user1.name} is {user1.age} years old, {user1.gender}, living in {user1.city}.")
    # print(f"{amber.name} is {user2.age} years old, {user2.gender}, living in {user2.city}.")
