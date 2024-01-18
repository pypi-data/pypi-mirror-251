from .connect import connect_xapi as Connect

names = "Amir Ershadi"
telegram = "@amir_ershadi_2"
email = "ershadia317@gmail.com"
document = "no"
version = "0.0.1"
library = "xapi_ir"

con = "created by %s In Telegram with ID %s\n email: %s | document: %s | Library: %s | Version: %s\n\n"% (names, telegram, email, document, library, version)
print(con)