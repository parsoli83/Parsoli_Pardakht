# Parsoli_Pardakht
a great alternative for Asan Pardakht (AP)

## About
parsoli pardakht is built as mimic to the famous Iranian website AP or "Asan pardakht"
this project is made as the final project for BP class teached by Dr.Goozarzi at University of Tehran

### Services
this platform is able to provide services such as:

+ getting and storing multiple cards
+ getting and storing multiple phone numbers
+ charge for phones
+ inter-system transactions

all cards are initialized with 10000 units of credit

### email verification

following the requirements of this project
Parsoli_pardakht uses email authentication for even safer logins

### password encryption

the description of this project insisted on using a password encryption method for more security
the method recommended was XOR encryption which is both an outdated method and unsecure way of data storage

alongside implementing the stated method
parsoli pardakht uses safety tools offered in the werkzeug.security package to provide safer encryptions on the users personal data to assure theyre safe and sound 
## Usage

to run the app locally type in the following commands in your terminal

```bash
git clone https://github.com/parsoli83/Parsoli_Pardakht
pip3 install -r requirements.txt
cd Parsoli_Pardakht
flask run
```

then open your browser to the said local url to visit the website


to support me please star this repository
thank you!