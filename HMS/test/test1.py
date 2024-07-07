from HMS.controller.controller import Controller


status, service = Controller.add_service("visit", "Note")
print(status, service)

natcode = 1909229193
status, doc = Controller.add_doctor("farbod", "orang", f"{natcode}", "1234", "1234", "1998-04-04",
                                    "Doctor", "09122655738", "adad@gmail.com", "adafdasf",
                                    "Oncologist", "test", "sub", "exp")
day = "2024/07/07"
status, shift = Controller.add_shift(day, f"{day} 12:00:00", f"{day} 22:00:00", doc, service)

status, person = Controller.add_patient("farbod", "family", "1585577781", "123a", "123a",
                                        "1998-04-04", "Patient", "09122655738", "adad@gmail.com",
                                        "aad asdad ", "Male", "A+")

status, app1 = Controller.add_appointment(shift, person, f"{day} 12:00:00", f"{day} 13:00:00", )

print(status, app1)
