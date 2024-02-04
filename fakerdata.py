# from faker import Faker
# # Create a Faker instance
# fake = Faker()

# # Generate and insert 200 lines of fake data
# for _ in range(200):
#     first_name = fake.first_name()
#     last_name = fake.last_name()
#     email = fake.email()
#     date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=90)
#     is_active = fake.boolean()
#     registration_date = fake.date_this_decade()
#     phone_number = fake.phone_number()[:20]
#     address = fake.address().replace("\n", ", ")  # Address may contain line breaks

#     cursor.execute(
#         "INSERT INTO customers (first_name, last_name, email, date_of_birth, is_active, registration_date, phone_number, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
#         (first_name, last_name, email, date_of_birth, is_active, registration_date, phone_number, address)
#     )

